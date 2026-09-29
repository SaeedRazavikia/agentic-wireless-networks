"""Regression checks for fresh, readable reproduction products (no TeX required)."""
from __future__ import annotations

import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest.mock import patch

from PIL import Image
from pypdf import PdfWriter

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'reproduce.py'
SPEC = importlib.util.spec_from_file_location('reproduce', SCRIPT)
reproduce = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = reproduce
SPEC.loader.exec_module(reproduce)


class ReproductionValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.output = self.root / 'build'
        self.output.mkdir()
        self.logs = self.output / 'logs'
        self.logs.mkdir()
        self.fixture_pdf = self.root / 'valid.pdf'
        writer = PdfWriter()
        writer.add_blank_page(width=72, height=72)
        writer.write(self.fixture_pdf)
        self.fixture_png = self.root / 'valid.png'
        Image.new('RGB', (4, 4), 'white').save(self.fixture_png)
        self.products = (self.output / 'figure.pdf', self.output / 'figure.png')

    def task(self, source, products=None, name='fixture'):
        return reproduce.BuildTask(name, (sys.executable, '-c', source), self.output,
                                   self.products if products is None else products)

    def run_task(self, task):
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            return reproduce.run_task(task, self.output, self.logs)

    def copy_products(self):
        return ("from pathlib import Path\n"
                f"Path('figure.pdf').write_bytes(Path({str(self.fixture_pdf)!r}).read_bytes())\n"
                f"Path('figure.png').write_bytes(Path({str(self.fixture_png)!r}).read_bytes())\n")

    def test_zero_exit_without_products_fails(self):
        result = self.run_task(self.task('pass'))
        self.assertEqual(result['exit_code'], 0)
        self.assertFalse(result['success'])
        self.assertFalse(result['validation']['passed'])
        self.assertEqual(len(result['validation']['outputs']), 2)
        self.assertTrue(all('FileNotFoundError' in item['error']
                            for item in result['validation']['outputs']))

    def test_stale_products_cannot_satisfy_a_noop_producer(self):
        for target, source in zip(self.products, (self.fixture_pdf, self.fixture_png)):
            target.write_bytes(source.read_bytes())
        result = self.run_task(self.task('pass'))
        self.assertFalse(result['success'])
        self.assertEqual(result['removed_existing_outputs'], ['figure.pdf', 'figure.png'])
        self.assertTrue(all(not path.exists() for path in self.products))

    def test_valid_products_are_parsed_and_recorded(self):
        result = self.run_task(self.task(self.copy_products()))
        self.assertTrue(result['success'])
        pdf, png = result['validation']['outputs']
        self.assertEqual(pdf['pages'], 1)
        self.assertEqual(png['size'], [4, 4])
        self.assertTrue(all(item['bytes'] > 0 for item in (pdf, png)))
        self.assertIn('Output validation:', (self.logs / 'fixture.log').read_text())

    def test_truncated_zero_exit_products_fail(self):
        source = self.copy_products() + (
            "for name in ('figure.pdf', 'figure.png'):\n"
            "    path = Path(name)\n"
            "    path.write_bytes(path.read_bytes()[:30])\n")
        result = self.run_task(self.task(source))
        self.assertEqual(result['exit_code'], 0)
        self.assertFalse(result['success'])
        self.assertTrue(all(not item['valid'] for item in result['validation']['outputs']))
        # Pillow can decode an image with the final IEND CRC partly missing.
        # The runner must also reject these less obvious truncations.
        for count in (1, 4):
            with self.subTest(missing_png_tail_bytes=count):
                source = (self.copy_products() + "path = Path('figure.png')\n"
                          f"path.write_bytes(path.read_bytes()[:-{count}])\n")
                result = self.run_task(self.task(source))
                self.assertEqual(result['exit_code'], 0)
                self.assertFalse(result['success'])
                self.assertTrue(result['validation']['outputs'][0]['valid'])
                self.assertFalse(result['validation']['outputs'][1]['valid'])

    def test_unreadable_pdf_with_header_and_eof_still_fails(self):
        source = "from pathlib import Path; Path('figure.pdf').write_bytes(b'%PDF-1.4\\nnot a PDF\\n%%EOF\\n')"
        result = self.run_task(self.task(source, (self.products[0],)))
        self.assertEqual(result['exit_code'], 0)
        self.assertFalse(result['success'])
        self.assertIn('error', result['validation']['outputs'][0])

    def test_nonzero_producer_fails_even_with_valid_products(self):
        result = self.run_task(self.task(self.copy_products() + 'raise SystemExit(3)'))
        self.assertEqual(result['exit_code'], 3)
        self.assertTrue(result['validation']['passed'])
        self.assertFalse(result['success'])

    def test_expected_paths_cover_every_task(self):
        tikz = self.output / 'figures' / 'tikz'
        tikz.mkdir(parents=True)
        for name in ('common', 'first', 'second'):
            (tikz / (name + '.tex')).write_text('fixture')
        tasks = reproduce.build_tasks(self.output, python=True, pgf=True, tikz=True,
                                      previews=True, pdflatex='pdflatex', pdftoppm='pdftoppm')
        actual = {task.name: [path.relative_to(self.output).as_posix() for path in task.outputs]
                  for task in tasks}
        self.assertEqual(actual, {
            'figure_overview': ['figures/joint_service_overview.pdf', 'figures/joint_service_overview.png'],
            'plot_figures': [f'figures/{name}.{extension}'
                            for name in ('joint_exclusion_geometry', 'wireless_confidence_trace',
                                         'certification_costs', 'execution_stopping_costs')
                            for extension in ('pdf', 'png')],
            'tikz_first': ['figures/tikz/first.pdf'],
            'tikz_second': ['figures/tikz/second.pdf'],
            **{'preview_' + name: ['figures/tikz/rendered/' + name + '.png']
               for name in ('validity_completion_outcomes', 'v37_cost_comparisons',
                            'v37_promise_reservations', 'v42_deadline_instrumentation_frontier')},
        })
        # Combined builds must render the newly compiled PDFs, not bundled copies.
        for task in tasks[-4:]:
            name = task.name.removeprefix('preview_')
            self.assertEqual(Path(task.command[-2]), tikz / (name + '.pdf'))
        standalone = reproduce.build_tasks(self.output, python=False, pgf=False, tikz=False,
                                            previews=True, pdflatex=None, pdftoppm='pdftoppm')
        for task in standalone:
            name = task.name.removeprefix('preview_')
            self.assertEqual(Path(task.command[-2]), tikz / 'rendered' / (name + '.pdf'))

    def test_main_rejects_copied_prebuilt_assets_and_records_validation(self):
        source_root = self.root / 'source'
        figures = source_root / 'figures'
        figures.mkdir(parents=True)
        (figures / 'figure_overview.py').write_text('pass\n')
        (figures / 'joint_service_overview.pdf').write_bytes(self.fixture_pdf.read_bytes())
        (figures / 'joint_service_overview.png').write_bytes(self.fixture_png.read_bytes())
        with patch.object(reproduce, 'ROOT', source_root), \
                patch.object(sys, 'argv', [str(SCRIPT), '--python', '--output', str(self.output)]), \
                redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            status = reproduce.main()
        self.assertEqual(status, 1)
        results = json.loads((self.output / 'build_results.json').read_text())
        self.assertEqual(len(results), 1)
        self.assertTrue(all(result['exit_code'] == 0 and not result['success'] for result in results))
        self.assertTrue(all(len(result['removed_existing_outputs']) == 2 for result in results))
        self.assertTrue((figures / 'joint_service_overview.pdf').exists())


if __name__ == '__main__':
    unittest.main()
