# Editable figures

Each `.tikz` file is a native drawing or plot fragment; the matching `.tex` file compiles that figure alone. No embedded PDF or raster image is used by these sources.

- Load `common.tex` in a parent preamble.
- `data/` contains plotting values and their original provenance record.
- `rendered/` contains the supplied PDF previews.

From the repository root, run `python scripts/reproduce.py --tikz` to compile every standalone wrapper in an isolated build directory. To compile one figure directly, change to this directory and run `pdflatex <figure-name>.tex`.

The upstream README referred to `research_v50/build_manuscript.py`; that file was not supplied. See `../../docs/provenance.md` for the source mapping and the historical-data limitation of the validity-outcome figure.
