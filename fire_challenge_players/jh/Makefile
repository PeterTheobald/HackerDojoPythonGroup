
all:
	@echo Here are some valid "make" targets. && echo
	@egrep '^[a-z-]*:' Makefile | awk '{print $$1}' | tr -d :

ACTIVATE := echo && source ../.venv/bin/activate
PYTHONPATH := .:..:../../fire_challenge

../.venv:
	cd .. && uv sync

test: ../.venv
	$(ACTIVATE) && python -m unittest tests/*_test.py

lint: ../.venv
	$(ACTIVATE) && black . && isort . && ruff check
	$(ACTIVATE) && pyright

lint-fire: ../.venv
	$(ACTIVATE) && cd .. && black -S . && isort . # && ruff check
	$(ACTIVATE) && cd ../fire_challenge && black -S . && isort .
	git diff -w

STRICT := --strict

# example_player.py and others need refactoring before `mypy` can be used.
lint-mypy:
	$(ACTIVATE) && mypy $(STRICT) .

universal:
	$(ACTIVATE) && cd .. && python Sam_Universal.py
