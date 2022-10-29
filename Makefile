run:
	sudo docker-compose build
	sudo docker-compose up -d   
	sudo docker ps -a
sd:
	systemctl start docker.service 

clean:
	find . -name __pycache__ -type d -exec rm -rf {} \;
	find . -name .pytest_cache -type d -exec rm -rf {} \;

.PHONY: run, sd, clean