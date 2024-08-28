#!/bin/bash

docker compose -f ./frontend/compose.yaml down -v
docker compose -f ./backend/compose.yaml down -v

