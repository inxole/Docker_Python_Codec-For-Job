FROM mcr.microsoft.com/devcontainers/python:3.12-bookworm

# Instal system packages
RUN apt-get update && apt-get install -y \
  vim \
  inkscape \
  potrace \
#  build-essential \
#  libagg-dev \
#  libpotrace-dev \
#  pkg-config \
  && rm -rf /var/lib/apt/lists/*

# Install python package
RUN pip install --no-cache-dir \
  fastapi \
  "uvicorn[standard]" \
  PyPDF2 \
  argparse \
  PyMuPDF \
  && rm -rf /root/.cache

# Install autotrace
# RUN wget https://github.com/autotrace/autotrace/releases/download/travis-20200219.65/autotrace_0.40.0-20200219_all.deb \
#   && dpkg -i autotrace_0.40.0-20200219_all.deb \
#   && rm autotrace_0.40.0-20200219_all.deb

EXPOSE 8000 
