docker rm -f $(docker ps -a | grep "flaskcondis:prod" | awk '{print $1}')

docker build -f ./flask.Dockerfile -t flaskcondis:prod .

docker network rm condis-prod

docker network create --attachable condis-prod

docker-compose -f docker-compose-prod.yml build 