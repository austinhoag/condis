docker rm -f $(docker ps -a | grep "testweb" | awk '{print $1}')

docker build -f ./flask.Dockerfile -t flaskcondis:latest .

docker network rm condis-test

docker network create --attachable condis-test

docker-compose -f docker-compose-test.yml build 