Your project should be structured as a package:
```
PyPI/
├── src/
│   └── benchmark/
│       ├── __init__.py (imports from benchmark)
│       └── benchmark.py (your original code)
├── benchmark.py (original demo file, can run standalone)
├── pyproject.toml
└── README.md
```

1. Ensure your project has a pyproject.toml with [project] metadata and a [build-system] section.
2. Build sdist + wheel (creates dist/): uv build --no-sources
       Creates a dist/ folder with a .whl (WHEEL) for pip and uv to install
       and a .tar.gz package (like a ZIP) with the source code
3. Create a PyPI API token
4. Publish to PyPI (use an API token): uv publish --token "$PYPI_TOKEN"

If PyPI complains about your project name, check for something similar here:
https://pypi.org/project/<canonical-name>/
https://pypi.org/simple/<canonical-name>/

Note: If you want to upload to TestPyPI first, then to PyPI once it looks right:
```
[[tool.uv.index]]
name = "testpypi"
url = "https://test.pypi.org/simple/"
publish-url = "https://test.pypi.org/legacy/"
explicit = true
```

```
uv publish --index testpypi --token "$TESTPYPI_TOKEN"
```


Think about adding a GitHub page and adding docs to ReadTheDocs.com



