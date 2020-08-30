docker rm -f $(docker ps -a | grep "testweb" | awk '{print $1}')

docker build -f ./flask.Dockerfile -t flaskcondis:test .

# docker-compose -f docker-compose-test.yml build 