docker rm -f $(docker ps -aq)

cd flask 
docker build -f ./flask.Dockerfile -t flaskcondis:latest .

docker network rm condis-dev

docker network create --attachable condis-dev

docker-compose build 
