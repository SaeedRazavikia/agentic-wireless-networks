# Editable figures

Each .tikz file is a native drawing or plot fragment, and the matching .tex file compiles that figure alone. The papers input the fragments directly. There are no embedded PDF or raster figure images in these sources.

- Load common.tex in the parent preamble.
- data/ contains exact plotting data and source provenance.
- rendered/ contains optional PDF previews, not required paper inputs.

From this directory, run `pdflatex <figure-name>.tex` to compile one figure. From the project root, run `python research_v50/build_manuscript.py` to compile the figures and both papers with synchronized references.

See the project README.md for the figure-number mapping and the documented historical-data limitation for the validity-outcome chart.
