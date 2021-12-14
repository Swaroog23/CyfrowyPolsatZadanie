# syntax=docker/dockerfile:1
FROM python:3.9.7
ENV PYTHONUNBUFFERED=1
WORKDIR /Provider
COPY . ./Provider
RUN pip install -r Provider/requirements.txt
CMD python3 Provider/main.py