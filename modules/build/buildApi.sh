#! /bin/bash

cd ..
printf "\nBuilding ENV for API\n"
docker image build --target api -f apiDockerfile -t scheduleapi .

printf "\nDeploying API\n"
docker run \
    -it \
    --network=host \
    scheduleapi