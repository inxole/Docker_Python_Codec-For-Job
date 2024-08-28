FROM mcr.microsoft.com/devcontainers/typescript-node:20-bookworm
RUN apt-get update && apt-get install -y \
  vim \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

WORKDIR /app/frontend

RUN pnpm install

ENTRYPOINT ["/bin/bash"]

