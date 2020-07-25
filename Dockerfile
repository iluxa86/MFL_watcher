FROM python:3.8-slim
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
CMD bin/start.sh