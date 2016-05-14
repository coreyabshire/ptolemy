#!/usr/bin/env bash

# script config params (likely to be relocated)
DB_USER_NAME=claudiusptolemy
DATABASE_NAME=claudiusptolemy

# create the database
# TODO: move variables to central location
sudo -u postgres sh -c "echo \"CREATE ROLE $DB_USER_NAME WITH LOGIN ENCRYPTED PASSWORD 'changeme'\" | psql -U postgres"
sudo -u postgres createdb -O $DB_USER_NAME $DATABASE_NAME
sudo -u postgres psql -c "CREATE EXTENSION postgis; CREATE EXTENSION postgis_topology;" $DATABASE_NAME

