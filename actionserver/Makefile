build:
	 docker build --no-cache  -t airtel-nigeria-action .

run:
	 docker run -d -p 1013:5055  --name airtel-nigeria-action airtel-nigeria-action

remove: 
	 docker rm -f airtel-nigeria-action


rebuild:        
	 docker build --no-cache  -t airtel-nigeria-action .
	 docker rm -f airtel-nigeria-action
	 docker run -p 1013:5055 -d  --name airtel-nigeria-action airtel-nigeria-action
