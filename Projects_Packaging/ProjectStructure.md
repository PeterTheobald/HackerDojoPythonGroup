# Python Project Structure

## Consistent project structure

- reduces complexity
- helps other developers understand your code
- helps IDEs and tools (linters, CI/CD, test runners etc) work with your code

```
my_app/
├── src/
│   └── my_app/
├── tests/
├── docs/
├── pyproject.toml
├── README.md
├── .gitignore
└── LICENSE
```

*Note: Take a look at [Cookiecutter](https://cookiecutter.readthedocs.io/en/1.7.2/README.html) for easy to install template projects.*
## src/

When testing you will want to "install" your program, just like you will on your production host. If you don't hide your program under `src/` then Python will `import my_app` from the source code copy, not the installed copy. This may let tests pass on your development machine but not in production. Hiding your source code under `src/` will catch packaging errors by testing the installed version.

Test with
``` bash
pip install -e .
pytest
```

What does `pip install -e .` do? It installs your project (in your `.venv`) using links to the source code not copies of the code. This way edits are always reflecting in the installed copy for testing.

## \_\_init\_\_.py

Your project may have many modules and subdirectories, but only expose the public ones to users of your project.

``` python
# src/my_package/__init__.py
from .core import Engine, run_task

__all__ = ["Engine", "run_task"]
```

``` python
# user can do this:
from my_package import Engine
```

``` python
# user can't do this:
from my_package.core import _internal_helper  # discouraged or not visible
```

## pyproject.toml

Defines all project metadata, including requirements and build tools.

``` toml
[project]
name = "my_app"
version = "0.4.2"
dependencies = ["requests>=2.32", "rich"]

[tool.setuptools.package-data]
"my_app" = ["py.typed"]
```

*Notes:
- If you are using `uv`, 'dependencies' replaces `requirements.txt`
- `pyproject.toml` replaces the older `setup.py` and `setup.cfg`
- You can still use `pyproject.toml` side by side with `requirements.txt` and/or `setup.py` if you need to... but `pyproject.toml` is the future.
- `pyproject.toml` lists your loose dependencies, that as a developer you want certain versions or better of certain modules and libraries. But for more deterministic testing `uv` keeps a `uv.lock` file that records the *exact* version of each module or library installed while testing your app. This `uv.lock` will be deployed with your app to insure it runs with the same *exact* versions in production. If you aren't using `uv` the older equivalent is `pip-compile pyproject.toml` (a separate tool).

## tests/

Keep the same directory structure under `tests/` as under `src/`. Put tests for each source file using `pytest` (or the older `unittest`).
So if you have `src/my_app/core/engine.py` you should also have a test `tests/core/test_engine.py`. `pytest` automatically finds all files named `test_`.

Use parameterized input values to be clear what edge-cases you are testing:
``` python
# tests/core/test_engine.py
@pytest.mark.parametrize("bad_input", ["", None, 0])
def test_engine_invalid(bad_input):
    with pytest.raises(ValueError):
        Engine(bad_input)
```

## docs/

Keep docs here - A users guide for people using your app, and a developers guide for people contributing, forking or troubleshooting your app. Use the tool `Sphinx` or `MkDocs` to turn your Markdown docs into nicely formatted static websites, PDF files, and linux man pages.

## .venv/

Your specific version of Python and all of your dependency modules will be installed here. If you are using `uv` it will create this for you, automatically install modules in it and automatically use it. Otherwise you need to create it manually with `python -m venv .venv` , manually activate it `source .venv/bin/activate` and manually install your dependencies in it before running your program with `pip install .` (for pyproject.toml) or `pip install -r requirements.txt` (for requirements.txt)

If you are using `uv` and other people on your team are using other tools like `pip` or you use tools like an IDE or CI/CD that doesn't understand `uv`, you can use `uv pip install` or `uv sync` to force it to install everything needed in `.venv` where the older tools will see them. Otherwise `uv` will just install things when you run the app.

## .gitignore

List all files that are temporary or sensitive or local-only that should never be checked into Git or GitHub. Here is a good sample `.gitignore`

```
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Virtual environments
.venv/
env/
venv/

# Distribution / packaging
build/
dist/
*.egg-info/
.eggs/

# Installer logs
pip-log.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.cache
.pytest_cache/

# IDEs and editors
.vscode/
.idea/
*.swp

# Jupyter notebooks checkpoints
.ipynb_checkpoints/

# MyPy / static analysis
.mypy_cache/
.dmypy.json
.pyre/

# Sphinx documentation
docs/_build/

# Environment variables IMPORTANT to not publish secrets
.env
.env.*

# OS-specific
.DS_Store
Thumbs.db
```


## Linting and formatting tools

Linting tools check your code with a detailed eye for errors, bad practices and code that "smells bad" because it is a bad practice that could lead to errors. Formatting tools reformat your code to have a standard format so all team members (and future developers) will have an easier time quickly reading your code.

Don't rely on running linters and formatters by hand. Add them to your IDE and/or CI/CD or Git pre-commit so they run automatically when appropriate.

Put your configuration for linting and formatting tools inside your `pyproject.toml` file. I prefer `ruff`:

``` toml
# pyproject.toml ─ Ruff configuration
[tool.ruff]
line-length = 88
target-version = "py311"

# Enable rule families
select = [
  "E",   # pycodestyle errors
  "W",   # pycodestyle warnings
  "F",   # pyflakes
  "I",   # import sorting (isort)
  "B",   # bugbear
  "N",   # pep8-naming
  "UP",  # pyupgrade
]

# Rules to ignore globally
ignore = ["E203", "E501"]

# Paths Ruff should skip
exclude = ["build", "dist", ".venv", "docs/_build"]

[tool.ruff.lint]
fix = true          # auto-apply safe fixes
show-fixes = true   # display applied fixes in output

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
skip-magic-trailing-comma = false

```

But others may be using older tools like `black` `isort` and/or `flake8`
``` toml
[tool.black]
line-length = 88

[tool.isort]
profile = "black"

[tool.flake8]
max-line-length = 88
extend-ignore = ["E203", "W503"]
```

And here's how to set up a git pre-commit to run format and lint every time you commit:

``` yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.4          # Use the latest tagged release
    hooks:
      - id: ruff-format  # runs the formatter (like black)
      - id: ruff
        args: [--fix]    # omit --fix if you only want linting
        # optional: restrict to certain paths
        # files: \.(py|pyi)$

```

``` bash
pre-commit install        # sets up the Git hook
pre-commit run --all-files
```

**Type annotations:**

Use type annotations throughout your code to help the type checker and linters to more thoroughly find errors in your code. Currently the best type checkers are: `mypy` and `pyright`.  These are separate tools that run like the linter and formatter and should be configured to run from your IDE and when you commit code. The developers of `ruff` are working on a new faster better type checker named `ty`. 

## Packaging and distribution

Python apps are generally distributed as 'wheels' or 'tarballs' (two different formats). These make files that can be installed using `uv` `pip` or `conda`. You can also upload your app to `PyPl` (Python Package Library) to make it easy to find and install.

You indicate how to build your project in the `build-system` section of your `pyproject.toml`. There are many different build systems to choose from.

``` toml
[build-system]
requires = ["setuptools>=67.0", "wheel"]
build-backend = "setuptools.build_meta"
```

**Creating a build package:**

``` bash
pip install build
python -m build
```

This creates:
- A **source distribution** (`.tar.gz`) — portable but slow to install
- A **wheel** (`.whl`) — pre-built, fast install
These appear in the `dist/` directory.

**Uploading to PyPI with `twine`**

Install twine:
``` bash
pip install twine
twine upload dist/*
```
You'll be prompted for your PyPI credentials or can use an API token.

**Versioning:**

Keep a single source of truth for your version in `src/my_package/__init__.py` :
``` python
__version__ = "0.1.0"
```
Every time you commit a new version, update this, or use a tool like `setuptools_scm` or `bump2version` to automatically bump the version number.



