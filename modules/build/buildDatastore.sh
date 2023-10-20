#! /bin/bash

printf "Deploying Arango\n"
docker run \
    -it \
    -p 8528:8529 \
    -e ARANGO_ROOT_PASSWORD=root \
    -e ARANGO_USERNAME=root \
    -e ARANGO_PASSWORD=root \
    --network=host  \
    arangodb/arangodb:latest
