#!/bin/bash

docker compose -f ./frontend/docker-compose.yaml down -v
docker compose -f ./backend/docker-compose.yaml down -v

