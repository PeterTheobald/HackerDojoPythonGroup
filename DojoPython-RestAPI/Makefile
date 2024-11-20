.PHONY: run install clean

run:
	uvicorn main:app --reload --log-level debug

install:
	pip install -r requirements.txt

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -f discussion_board.db
