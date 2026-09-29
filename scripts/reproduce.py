#!/usr/bin/env python3
"""Rebuild supplied presentations without modifying their source assets.

This utility does not simulate measurements or reconstruct missing trial records.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class BuildTask:
    name: str
    command: tuple[str, ...]
    cwd: Path
    outputs: tuple[Path, ...]


def build_tasks(output: Path, *, python: bool, pgf: bool, tikz: bool,
                previews: bool, pdflatex: str | None,
                pdftoppm: str | None) -> list[BuildTask]:
    """Declare every expected product before executing any producer."""
    tasks = []
    figures = output / 'figures'
    if python:
        tasks.append(BuildTask('figure_overview',
                               (sys.executable, str(figures / 'figure_overview.py')),
                               output, tuple(figures / ('joint_service_overview' + suffix)
                                             for suffix in ('.pdf', '.png'))))
    if pgf:
        products = ('joint_exclusion_geometry', 'wireless_confidence_trace',
                    'certification_costs', 'execution_stopping_costs')
        tasks.append(BuildTask('plot_figures', (sys.executable, str(figures / 'plot_figures.py')),
                               output, tuple(figures / (product + suffix)
                                             for product in products for suffix in ('.pdf', '.png'))))
    if tikz:
        if pdflatex is None:
            raise ValueError('pdflatex is required for TeX tasks.')
        options = (pdflatex, '-interaction=nonstopmode', '-halt-on-error')
        for source in sorted((figures / 'tikz').glob('*.tex')):
            if source.name != 'common.tex':
                tasks.append(BuildTask('tikz_' + source.stem, options + (source.name,),
                                       source.parent, (source.with_suffix('.pdf'),)))
    if previews:
        if pdftoppm is None:
            raise ValueError('pdftoppm is required for PNG previews.')
        rendered = figures / 'tikz' / 'rendered'
        source_dir = figures / 'tikz' if tikz else rendered
        for name in ('validity_completion_outcomes', 'v37_cost_comparisons',
                     'v37_promise_reservations', 'v42_deadline_instrumentation_frontier'):
            tasks.append(BuildTask('preview_' + name,
                                   (pdftoppm, '-png', '-singlefile', '-r', '160',
                                    str(source_dir / (name + '.pdf')), str(rendered / name)),
                                   output, (rendered / (name + '.png'),)))
    return tasks


def validate_output(path: Path, output: Path) -> dict:
    """Read complete PDFs/PNGs, rejecting missing, empty, or damaged products."""
    result = {'path': path.relative_to(output).as_posix(), 'valid': False}
    try:
        result['bytes'] = path.stat().st_size
        if not result['bytes']:
            raise ValueError('Output is empty.')
        if path.suffix.lower() == '.pdf':
            with path.open('rb') as stream:
                if stream.read(5) != b'%PDF-':
                    raise ValueError('Missing PDF header.')
                stream.seek(max(0, result['bytes'] - 1024))
                if not stream.read().rstrip().endswith(b'%%EOF'):
                    raise ValueError('Missing final PDF EOF marker; output may be truncated.')
                stream.seek(0)
                reader = PdfReader(stream, strict=True)
                result['pages'] = len(reader.pages)
                if not result['pages']:
                    raise ValueError('PDF has no pages.')
                for page in reader.pages:
                    if page.mediabox.width <= 0 or page.mediabox.height <= 0:
                        raise ValueError('PDF page has invalid dimensions.')
                    contents = page.get_contents()
                    if contents is not None:
                        # Parse and decode every page stream, rather than only its header.
                        contents.get_data()
                        _ = contents.operations
        elif path.suffix.lower() == '.png':
            with path.open('rb') as stream:
                stream.seek(max(0, result['bytes'] - 12))
                if stream.read() != b'\x00\x00\x00\x00IEND\xaeB\x60\x82':
                    raise ValueError('Missing complete final PNG IEND chunk; output may be truncated.')
            with Image.open(path) as picture:
                if picture.format != 'PNG':
                    raise ValueError('Output is not a PNG image.')
                picture.verify()
            with Image.open(path) as picture:
                picture.load()
                result['size'] = list(picture.size)
        else:
            raise ValueError(f'Unsupported output format: {path.suffix}')
        result['valid'] = True
    except Exception as exc:
        # Parsing libraries expose several exception types; retain the failure in
        # the build manifest and continue checking the remaining expected files.
        result['error'] = f'{type(exc).__name__}: {exc}'
    return result


def run_task(task: BuildTask, output: Path, logs: Path) -> dict:
    print(f'Running {task.name}', flush=True)
    result = {'task': task.name, 'exit_code': None, 'log': f'logs/{task.name}.log',
              'removed_existing_outputs': []}
    log = ''
    try:
        # Supplied figures and previous runs may already contain valid products.
        # Delete only this task's products so a no-op producer cannot pass.
        for path in task.outputs:
            if path.exists() or path.is_symlink():
                path.unlink()
                result['removed_existing_outputs'].append(path.relative_to(output).as_posix())
        proc = subprocess.run(task.command, cwd=task.cwd, capture_output=True, text=True)
        result['exit_code'] = proc.returncode
        log = proc.stdout + proc.stderr
    except OSError as exc:
        log = f'{type(exc).__name__}: {exc}\n'
        result['execution_error'] = log.strip()
    validation = [validate_output(path, output) for path in task.outputs]
    result['validation'] = {'passed': all(item['valid'] for item in validation),
                            'outputs': validation}
    result['success'] = result['exit_code'] == 0 and result['validation']['passed']
    log += '\nOutput validation:\n' + json.dumps(result['validation'], indent=2) + '\n'
    (logs / f'{task.name}.log').write_text(log, encoding='utf-8')
    if not result['success']:
        print(f'  Failed; see {logs / (task.name + ".log")}', file=sys.stderr)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--python', action='store_true', help='render the overview with Matplotlib')
    parser.add_argument('--pgf', action='store_true', help='render four legacy PGF plots; requires pdflatex and pdftoppm')
    parser.add_argument('--tikz', action='store_true', help='compile all native TikZ figures; requires pdflatex')
    parser.add_argument('--previews', action='store_true', help='render four native plot previews; requires pdftoppm')
    parser.add_argument('--output', type=Path, default=ROOT / 'build' / 'reproduction')
    args = parser.parse_args()
    if not any((args.python, args.pgf, args.tikz, args.previews)):
        args.python = True
    output = args.output.resolve()
    if output == ROOT or ROOT.is_relative_to(output) or output.is_relative_to(ROOT / 'figures') or output.is_relative_to(ROOT / 'docs'):
        parser.error('Choose a build/output directory distinct from the repository sources.')
    pdflatex = shutil.which('pdflatex')
    pdftoppm = shutil.which('pdftoppm')
    if (args.pgf or args.tikz) and pdflatex is None:
        parser.error('pdflatex is required for the requested tasks.')
    if (args.pgf or args.previews) and pdftoppm is None:
        parser.error('pdftoppm is required for PNG previews.')
    output.mkdir(parents=True, exist_ok=True)
    shutil.copytree(ROOT / 'figures', output / 'figures', dirs_exist_ok=True)
    logs = output / 'logs'
    logs.mkdir(exist_ok=True)
    if args.pgf:
        script = output / 'figures' / 'plot_figures.py'
        # The supplied script fixes the Poppler path to /usr/bin. Adapt only this
        # build copy to the executable discovered on the current system.
        script.write_text(script.read_text().replace("'/usr/bin/pdftoppm'", repr(pdftoppm)))
    if args.previews:
        (output / 'figures' / 'tikz' / 'rendered').mkdir(parents=True, exist_ok=True)
    tasks = build_tasks(output, python=args.python, pgf=args.pgf, tikz=args.tikz,
                        previews=args.previews, pdflatex=pdflatex, pdftoppm=pdftoppm)
    results = [run_task(task, output, logs) for task in tasks]
    (output / 'build_results.json').write_text(json.dumps(results, indent=2) + '\n')
    failed = sum(not result['success'] for result in results)
    print(f'{len(results) - failed}/{len(results)} build tasks succeeded. Outputs: {output}')
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
