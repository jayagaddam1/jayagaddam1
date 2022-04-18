build:
	sudo docker build --no-cache  -t airtel-nigeria-action .

run:
	sudo docker run -d -p 1013:5055  --name airtel-nigeria-action airtel-nigeria-action

remove: 
	sudo docker rm -f airtel-nigeria-action


rebuild:        
	sudo docker build --no-cache  -t airtel-nigeria-action .
	sudo docker rm -f airtel-nigeria-action
	sudo docker run -p 1013:5055 -d  --name airtel-nigeria-action airtel-nigeria-action
