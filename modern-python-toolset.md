# The Modern Python Toolset

A collection of tools that are so much better than their predecessors they should replace them. Everyone should use these tools as part of their development process.

- uv (environment manager, better than pyenv pip pipenv poetry conda etc)
- pyright (or maybe mypy, for type checking)
- ruff (linting and formatting, better than pylint, black, flake8, isort)
- pytest (unit testing, better than unittest)
- pydantic (data validation that leverages type hints)
- pyproject.toml (for project organization, better than setup.py, setup.cfg)
- sqlalchemy (abstraction for database calls)
- github actions (to define automatic continuous deployment (CI/CD))
- pre-commit (framework to automate steps before commiting code)
- typer (command line arguments that leverages type hints)


## uv
(environment manager)
- 10x-100x FASTER. Replaces pip, pyenv, pipenv, pipx, poetry, conda, etc. Works with pyproject.toml
- Generates and updates pyproject.toml and uv.lock lockfile (versions) and .venv
uv init; uv init myproject; uv init --lib mylibrary; uv init --package mypackage
uv add httpx; uv add 'httpx>0.1.5'
uv run
uv python install (eg: uv python install 3.6 3.9 3.12)
  uv run --python 3.12
  uv python pin 3.12
  uv venv --python 3.12
uv lock (not needed, uv run will do it automatically)
uv sync (not needed, uv run will do it automatically)
uv venv (create venv); source .venv/bin/activate
uv pip install, uv pip sync requirements.txt (not needed, use uv add)
uv add --script main.py "requests<3" "rich" (isolated scripts); uv run main.py
uv tool install (install command line tools like `ruff`); uv tool list
uv tool run (aka uvx, eg: `uvx ruff`)

## pyright
(or maybe mypy, for type checking)

## ruff
(linting and formatting, better than pylint, black, flake8, isort)
ruff check
ruff check --fix
ruff format

## pytest
(unit testing, better than unittest)
test/test_sample.py:
```
import my_code
def test_test1():
  # val=call mycode with test data
  assert(val==5)
```

## pydantic
- data validation & serialization, integrates well with dataclasses, type hints (mypy/pyright), SQLAlchemy and FastAPI
```
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str = 'John Doe'
    signup_ts: Optional[datetime] = None
    friends: List[int] = []
```
https://docs.pydantic.dev/latest/#why-use-pydantic

## pyproject.toml
(for project organization, better than setup.py, setup.cfg)
```
[project]
name = "spam-eggs"
version = "2020.0.0"
dependencies = [
  "httpx",
  "gidgethub[httpx]>4.0.0",
  "django>2.1; os_name != 'nt'",
  "django>2.0; os_name == 'nt'",
]
requires-python = ">= 3.8"
```

## sqlalchemy
(abstraction for database calls)
- abstract different dialects of sql
- Core: schema, command-oriented
- ORM (Object Relational Mapper) classes <-> tables: domain, state-oriented
- Core vs ORM: You choose how much abstraction is done for you

## Alembic

## github actions
- to define automatic continuous deployment (CI/CD)
- build, test & deploy
- on PUSH, run series of tests and commands to test package & deploy

## pre-commit
- framework to automate steps before commiting code
- like github actions, can run tests and formatters but locally every time you commit

## typer
(command line arguments that leverages type hints)

## Others...
There are many other excellent modern libraries and frameworks that have made development a delight compare to 'the old way', but none that have definitely overthrown what came before to make it on this list. Some notable ones are:

- For web backends: FastAPI for Rest APIs; Flask or Django for more 'batteries included' backends.
- HTMX for web frontends: Easy way to generate dynamic front ends without much Javascript coding. Very opinionated and different than a traditional React or Vue front-end.
- Polar instead of Panda for data management. Polar has a better interface, but Panda is compatible with more related libraries.
