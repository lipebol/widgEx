### Never send your "passwords" in Production ###
FROM node:lts-slim AS base-build

RUN \
    apt update && apt upgrade -y \
    && apt install clevis -y \
    && rm -rf /var/lib/apt/lists/*


# === DEV ===
FROM base-build AS dev
WORKDIR /home/node/servEx
