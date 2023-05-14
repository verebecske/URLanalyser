build:
	sudo docker compose build

run:
	sudo docker compose up
	sudo docker ps -a

docker:
	systemctl start docker.service 

clean:
	find . -name __pycache__ -type d -exec rm -rf {} \;
	find . -name .pytest_cache -type d -exec rm -rf {} \;

lint:
	python -m black .
	python -m autoflake --check --quiet -r -v .

version:
	@echo 1.2

.PHONY: run, docker, clean, build, lint, version
