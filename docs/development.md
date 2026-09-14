# Work with the repository

Clone the companion repository using your GitHub account:

```bash
git clone https://github.com/SaeedRazavikia/agentic-wireless-networks.git
cd agentic-wireless-networks
python -m pip install -r requirements.txt
python scripts/scalar_frontier.py verify
```

See `docs/reproduction.md` for all figure and document build commands. Generated `build/` outputs are ignored by Git. Preserve the original files under `docs/source/` and the supplied data provenance; identify newly generated experiments separately from the historical results.

The manuscript cites this repository using the `razavikia2026code` entry in `docs/repository_citation.bib`. Keep author, title, and URL metadata consistent with `CITATION.cff`.
