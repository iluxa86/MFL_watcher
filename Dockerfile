FROM ubuntu:20.04
COPY . /app
WORKDIR /app
RUN apt-get update && apt-get install -y python3-pip && apt-get install bash
RUN pip3 install -r requirements.txt
CMD bin/docker_start.sh