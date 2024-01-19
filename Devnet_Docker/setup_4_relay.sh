cd mev-boost-relay

# docker build .
# docker build -f Dockerfile_redis -t relay_redis .
# docker build -f Dockerfile_housekeeper -t relay_housekeeper .
# docker build -f Dockerfile_api -t relay_api .
# docker build -f Dockerfile_website -t relay_website .

docker compose up -d