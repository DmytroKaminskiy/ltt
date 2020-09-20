FROM python:3.8.5-slim

RUN apt -y update && apt install -y \
    libffi-dev \
    libfreetype6-dev \
    libfribidi-dev \
    libharfbuzz-dev \
    libjpeg-turbo-progs \
    libjpeg62-turbo-dev \
    liblcms2-dev \
    libopenjp2-7-dev \
    libtiff5-dev \
    libwebp-dev \
    zlib1g-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/projects/ltt
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
ENV PYTHONBREAKPOINT=ipdb.set_trace

COPY requirements.txt /tmp/requirements.txt

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt
