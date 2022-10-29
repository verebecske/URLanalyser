run:
	sudo docker-compose build
	sudo docker-compose up -d   
	sudo docker ps -a
sd:
	systemctl start docker.service 

.PHONY: run, sd