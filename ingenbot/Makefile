run:
	sudo docker build . -t ingenbot
	sudo docker run --rm -it ingenbot

lint:
	black .
	pylint --fail-under=7 *.py
	autoflake --check --quiet -r -v .


.PHONY: run build lint