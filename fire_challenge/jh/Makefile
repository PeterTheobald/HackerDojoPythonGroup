
all:
	@echo Here are some valid "make" targets. && echo
	@egrep '^[a-z]*:' Makefile | awk '{print $$1}' | tr -d :

ACTIVATE := echo && source ../.venv/bin/activate

../.venv:
	cd .. && uv sync

test: ../.venv
	$(ACTIVATE) && python -m unittest tests/*_test.py

STRICT := --strict

lint:
	$(ACTIVATE) && ruff check
	$(ACTIVATE) && pyright        tests
	$(ACTIVATE) && mypy $(STRICT) tests
