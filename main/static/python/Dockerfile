FROM ubuntu:latest
COPY runcontainer.py /
RUN apt-get update && apt-get install -y python3 && apt-get install -y default-jre && apt-get install -y default-jdk
RUN mkdir /testing
RUN mkdir /input
CMD ["timeout", "10s", "python3", "./runcontainer.py"]
