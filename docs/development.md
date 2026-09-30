# Work with the repository

Clone the companion repository using your GitHub account:

```bash
git clone https://github.com/SaeedRazavikia/agentic-wireless-networks.git
cd agentic-wireless-networks
python -m pip install -r requirements.txt
python scripts/scalar_frontier.py verify
```

Edit [`extended_experiments.md`](../extended_experiments.md) directly to update the experimental documentation. See [`reproduction.md`](reproduction.md) for figure and PNG-preview commands. Generated `build/` outputs are ignored by Git. Preserve the original files under `docs/source/` and the supplied data provenance; identify newly generated experiments separately from the historical results.

The manuscript links directly to this GitHub repository. The optional BibTeX entry in `docs/repository_citation.bib` is available for readers who cite the repository separately; keep its author, title, and URL metadata consistent with `CITATION.cff`.
