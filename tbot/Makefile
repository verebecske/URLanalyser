run:
	sudo docker build . -t ingenbot
	sudo docker run --rm -it ingenbot

lint:
	python -m black .
	python -m pylint --fail-under=7 *.py
	python -m autoflake --check --quiet -r -v .


.PHONY: run build lint