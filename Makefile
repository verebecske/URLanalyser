run:
	sudo docker-compose build
	sudo docker-compose up -d   
	sudo docker ps -a

.PHONY: run