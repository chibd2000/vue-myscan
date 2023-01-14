#!/bin/bash
docker cp my.cnf myscan_mysql:/etc/my.cnf
docker-compose restart