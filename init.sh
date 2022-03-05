#!/usr/bin/env bash

## make sure requirements are up to date
pip freeze > requirements.txt

## -d will not keep docker up and running in the terminal but keep it running as a background process
docker-compose up -d --build

##allow postgres to setup
sleep 30

## create the database
docker-compose exec web python database_setup.py create_db

#seed the database
docker-compose exec web python database_setup.py seed_db
