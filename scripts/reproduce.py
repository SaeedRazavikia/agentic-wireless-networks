#!/usr/bin/env python3
"""Rebuild supplied presentations without modifying their source assets.

This utility does not simulate measurements or reconstruct missing trial records.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--python', action='store_true', help='render architecture and overview with Matplotlib')
    parser.add_argument('--pgf', action='store_true', help='render four legacy PGF plots; requires pdflatex and pdftoppm')
    parser.add_argument('--tikz', action='store_true', help='compile all native TikZ figures; requires pdflatex')
    parser.add_argument('--protocol', action='store_true', help='compile the standalone extended protocol twice')
    parser.add_argument('--output', type=Path, default=ROOT / 'build' / 'reproduction')
    args = parser.parse_args()
    if not any((args.python, args.pgf, args.tikz, args.protocol)):
        args.python = True
    output = args.output.resolve()
    if output == ROOT or ROOT.is_relative_to(output) or output.is_relative_to(ROOT / 'figures') or output.is_relative_to(ROOT / 'docs'):
        parser.error('Choose a build/output directory distinct from the repository sources.')
    pdflatex = shutil.which('pdflatex')
    pdftoppm = shutil.which('pdftoppm')
    if (args.pgf or args.tikz or args.protocol) and pdflatex is None:
        parser.error('pdflatex is required for the requested tasks.')
    if args.pgf and pdftoppm is None:
        parser.error('pdftoppm is required for PNG previews of the PGF plots.')
    output.mkdir(parents=True, exist_ok=True)
    shutil.copytree(ROOT / 'figures', output / 'figures', dirs_exist_ok=True)
    logs = output / 'logs'
    logs.mkdir(exist_ok=True)
    results = []

    def run(name: str, command: list[str], cwd: Path) -> None:
        print(f'Running {name}', flush=True)
        proc = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
        (logs / f'{name}.log').write_text(proc.stdout + proc.stderr)
        results.append({'task': name, 'exit_code': proc.returncode, 'log': f'logs/{name}.log'})
        if proc.returncode:
            print(f'  Failed; see {logs / (name + ".log")}', file=sys.stderr)

    if args.python:
        for script in ('agent_architecture.py', 'figure_overview.py'):
            run(script.removesuffix('.py'), [sys.executable, str(output / 'figures' / script)], output)
    if args.pgf:
        script = output / 'figures' / 'plot_figures.py'
        # The supplied script fixes the Poppler path to /usr/bin. Adapt only this
        # build copy to the executable discovered on the current system.
        script.write_text(script.read_text().replace("'/usr/bin/pdftoppm'", repr(pdftoppm)))
        run('plot_figures', [sys.executable, str(script)], output)
    if args.tikz:
        for source in sorted((output / 'figures' / 'tikz').glob('*.tex')):
            if source.name == 'common.tex':
                continue
            run('tikz_' + source.stem, [pdflatex, '-interaction=nonstopmode', '-halt-on-error', source.name], source.parent)
    if args.protocol:
        shutil.copytree(ROOT / 'docs', output / 'docs', dirs_exist_ok=True)
        shutil.copy2(ROOT / 'extended_experiments.tex', output / 'extended_experiments.tex')
        for index in (1, 2):
            run(f'protocol_pass_{index}', [pdflatex, '-interaction=nonstopmode', '-halt-on-error', 'extended_experiments.tex'], output)
    (output / 'build_results.json').write_text(json.dumps(results, indent=2) + '\n')
    failed = sum(result['exit_code'] != 0 for result in results)
    print(f'{len(results) - failed}/{len(results)} build tasks succeeded. Outputs: {output}')
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
