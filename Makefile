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

.PHONY: run, docker, clean, build
