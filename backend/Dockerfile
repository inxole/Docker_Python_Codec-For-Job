FROM mcr.microsoft.com/devcontainers/python:3.12-bookworm

# Instal system packages
RUN apt-get update && apt-get install -y \
  vim \
  inkscape \
  potrace \
  libgl1 \
  && rm -rf /var/lib/apt/lists/*

# Install python package
RUN pip install --no-cache-dir \
  fastapi \
  "uvicorn[standard]" \
  PyPDF2 \
  argparse \
  PyMuPDF \
  python-multipart \
  opencv-python \
  svgwrite \
  matplotlib \
  pandas \
  openpyxl \
  opencv-python \
  opencv-contrib-python \
  && rm -rf /root/.cache
