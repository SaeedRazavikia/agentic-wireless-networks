# Editable figures

Each `.tikz` file is a native drawing or plot fragment; the matching `.tex` file compiles that figure alone. No embedded PDF or raster image is used by these sources.

- Load `common.tex` in a parent preamble.
- `data/` contains plotting values and their original provenance record.
- `rendered/` contains canonical PDF previews and four PNG illustrations used in [`Extended Experiments`](../../extended_experiments.md).

From the repository root, run `python scripts/reproduce.py --tikz --previews` to compile every standalone wrapper and render the four Markdown illustrations at 160 dpi in an isolated build directory. `--previews` alone converts the existing canonical PDFs using Poppler's `pdftoppm`. To compile one figure directly, change to this directory and run `pdflatex <figure-name>.tex`. See [`reproduction.md`](../../docs/reproduction.md) for dependencies and validation records.

The upstream README referred to `research_v50/build_manuscript.py`; that file was not supplied. See `../../docs/provenance.md` for the source mapping and the historical-data limitation of the validity-outcome figure.

The active drawing sources were synchronized with the updated manuscript on 29 September 2026. The manuscript uses the native TikZ figures; the separate Python/PGF scripts retain alternative layouts of the same frozen results. Mean task-delay limits are distinct from acquisition deadlines, and the legacy maximin comparison rows are explicitly unguarded. See `../../docs/manuscript_alignment.md` and its JSON manifest for the manuscript version and source hashes.

Use these canonical sources and previews directly; duplicate top-level native PDF aliases and the duplicate goal/evidence wrapper are no longer distributed.
