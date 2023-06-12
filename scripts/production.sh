#!/bin/bash

# if old instance exists, stop it
cd ..
if [ -d "Pieski-UW" ]; then
    cd Pieski-UW
    docker compose down
    cd ..
fi


# remove old files
rm -rf Pieski-UW

# clone repo
git clone --branch main https://github.com/Pieski-Uw/Pieski-UW

# build docker images
cd Pieski-UW
docker compose up --build -d
cd ..