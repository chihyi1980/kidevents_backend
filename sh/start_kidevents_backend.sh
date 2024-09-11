sudo docker rm kidevents-backend
sudo docker run --name kidevents-backend --network my-network -p 5000:5000 -d kidevents-backend:latest