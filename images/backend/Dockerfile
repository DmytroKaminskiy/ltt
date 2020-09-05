FROM python:3.8.5-slim

WORKDIR /home/ubuntu/projects/ltt
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
ENV PYTHONBREAKPOINT=ipdb.set_trace

COPY requirements.txt /tmp/requirements.txt

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt
