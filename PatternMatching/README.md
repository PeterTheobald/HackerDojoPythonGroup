View this demo in a jupyter lab notebook, a more up to date version of Jupyter Notebooks.  
  
We open a terminal shell. Make a new directory for "Pattern-Matching". Pattern Matching requires Python v 3.10 or better, so let's make sure uv is using a modern enough Python for us. Remember with uv we can just tell it what version of Python we need and uv will take care of installing whatever Python or packages we need.  

The quick version:
```
$ uv run python -m jupyterlab
```

The more in-depth version:
  
```
$ pwd # What folder are we in?
/home/peter/projects/hacker-dojo-python-group/PatternMatching

$ ls -a # Do we have a .venv and a pyproject.toml?

$ # No there isn't. uv will look for a .venv in a parent directory.
$ uv run python -c "import os,sys; print(os.environ.get('VIRTUAL_ENV') or sys.prefix)"` # Which .venv is uv using? 
/home/peter/projects/hacker-dojo-python-group/.venv

$ uv run which python; uv run python --version  # show what Python uv is using
/home/peter/projects/hacker-dojo-python-group/.venv/bin/python
Python 3.13.2

$ # Python 3.13 is good enough for us. We are going to install jupyterlab. We are ok installing it in the shared hacker-dojo projects .venv.
$ uv run python -m jupyterlab # Start Juptyer Lab notebook to open THIS notebook we are looking at.

$ # If we wanted to separate Pattern-Matching from the rest of the hacker-dojo demos, we could create our own .venv here in this directory: uv init --bare; uv venv; uv add jupyterlab
