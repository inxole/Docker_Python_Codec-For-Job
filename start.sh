#!/bin/bash

rm -rf ./frontend/node_modules
rm -rf ./frontend/.pnpm-store

docker compose -f ./frontend/compose.yaml up -d --build
docker compose -f ./backend/compose.yaml up -d --build

