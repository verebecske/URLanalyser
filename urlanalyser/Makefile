run:
	python main.py

setup:
	pip install -r requirements.txt

test:
	python -m unittest discover -s . -p 'test_*.py'   

clean:
	find . -name __pycache__ -type d -exec rm -rf {} \;
	find . -name .pytest_cache -type d -exec rm -rf {} \;

lint:
	python -m black .
	python -m pylint --fail-under=7 *.py
	python -m autoflake --check --quiet -r -v .

.PHONY: run clean setup test lint