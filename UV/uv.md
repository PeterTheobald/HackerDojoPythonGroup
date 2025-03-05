# Using UV for Python environment management

UV is a Python environment management program written in Rust that boasts 100x speed improvement over previous tools like VitualEnv, Venv, pip, pipenv, Poetry, Conda, PyEnv.

It not only manages your installed Python libraries, it even manages multiple versions of Python itself (like PyEnv does).

I found it a bit confusing initially reading the uv docs. I realized the confusion came from the ability to use uv in two different ways: in a completely new, very fast and easy way we will call here "native uv", and in a way that is very compatible with pre-existing tools like pip and venv we will call here "manual uv"

## Installing uv

We can install uv on a brand new system with no other dependencies (no Python, no pip, etc)

#### On macOS and Linux

`curl -LsSf https://astral.sh/uv/install.sh | sh`
#### On Windows

`powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`

Or we can install uv on a system that already has Python and pip:
`pip install uv`
Note: Don't install `uv` inside an activated venv. Be sure to `deactivate` first. You want `uv` available from anywhere on your system

## What can uv manage?

uv can manage a few different things:
- Python versions (eg: 3.9, 3.11)
- Python libraries (import *library*)
- Stand alone executable **tools** like ruff, black, etc.
- Stand alone Python scripts (single source file)
- Python projects (bigger Python programs with more than one source file)

## uv the native way

### Scripts

`uv run example.py`
- creates an on-demand temporary .venv and installs the python and libraries the script needs from cache if it has them or from the internet otherwise

Add requirements as inline comments in the script source code
`uv add --script example.py requests rich`
```
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "requests",
#     "rich",
# ]
# ///
```

What if you have tested your script and want to make sure the **exact** same versions of the libraries you tested with are always used? Not just requests >= 2 but requests 2.17.3? You *lock* the requirements:
`uv lock --script example.py`
This creates a `example.py.lock` file with the exact versions of everything that will be respected by `uv run` and other uv commands.

Many more options, like don't use any versions later than a certain date, etc.
Test my script with a different version of python:
`uv run --python 3.13 example.py`

Note: On Windows if your program extension is `.pyw` it will run it as a GUI program without a command window. Useful for programs using tkinter, wxwidgets, or QT that open their own graphical windows.

### Projects

`uv init myproject`
Creates a directory myproject with a README.md, a pyproject.toml, a main.py a .python-version, a .venv, and a uv.lock
or `uv init` in the current directory.

pyproject.toml:
```
[project]
name = "project"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = ["jax; sys_platform == 'linux'"]
```

In a project your dependencies don't go in inline comments, they go in the pyproject.toml. You can edit it manually, or use:
`uv add requests`
`uv remove requests`
`uv add 'requests==2.31.0'`
`uv lock --upgrade-package requests`

To run your project just use `uv run` and uv will make sure all the right libraries and python version is install in your `.venv`
`uv run example.py`
Note: to run something under flask you would use:
`uv run -- flask run -p 3000`
When you run your project it will automatically create your uv.lock file with your exact versions.

### Build a distribution (source or binary wheel)
`uv build`
It puts everything in the `dist/` folder
You can actually automate publishing your package to PyPI with:
`uv publish --token my_id_token`

### Running tools
uv can manage executable tools that aren't necessarily written in Python, eg: Ruff,
`uvx ruff check`
This will run ruff without installing it in your system (but very fast). It is exactly the same as `uv tool run ruff`
Or you can install it if it's something you will run often:
`uv tool install ruff`
`uv tool install 'httpie>0.1.0'`
`uv tool upgrade --all`
Specify which Python version:
`uvx --python 3.10 ruff`
`uvx tool install --python 3.10 ruff`

## Integrations
The uv docs have instructions on using uv with Docker, Jupyter, and many others.

## uv the manual way

You can still work with the same old workflow you are used to instead of allowing uv to do everything automatically (but why would you?).

`uv pip install library`
`uv lock`
`uv export --format requirements-txt`


