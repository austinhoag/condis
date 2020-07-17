docker rm -f $(docker ps -a | grep "flaskcondis" | awk '{print $1}')

docker build -f ./flask.Dockerfile -t flaskcondis:latest .

docker network rm condis-dev

docker network create --attachable condis-dev

docker-compose build 