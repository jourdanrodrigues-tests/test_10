#!/usr/bin/env bash

docker exec -it hellofresh_db psql -U postgres -c 'drop database hellofresh_test;'
