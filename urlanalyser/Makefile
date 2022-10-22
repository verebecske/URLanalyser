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
	black .
	pylint --fail-under=7 *.py
	autoflake --check --quiet -r -v .

curl:
	curl 'http://127.0.0.1:5000/check?url=napszemuveg.be'

.PHONY: run clean setup test lint curl