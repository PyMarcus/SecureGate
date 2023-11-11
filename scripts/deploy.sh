#!/bin/bash

docker stop $(docker ps -a -q)
docker image rm -f secure_gate-rpc_server
docker compose up -d --build
