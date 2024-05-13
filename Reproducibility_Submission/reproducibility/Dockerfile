# Use Ubuntu 22.04 LTS as the base image
FROM ubuntu:20.04

#Copy files
WORKDIR /root
COPY ./local_experiments local_experiments

#Install some packages that help with interactive use
RUN apt-get -y update && apt-get -y install vim python3 python3-pip zip unzip curl bash-completion python-is-python3

#install java
RUN curl -s "https://get.sdkman.io" | bash
SHELL ["/bin/bash", "-c"]
RUN source /root/.sdkman/bin/sdkman-init.sh &&\
  sdk install java 11.0.20-tem &&\
  sdk install maven 3.9.0 &&\ 
  pip3 install -r local_experiments/requirements.txt
WORKDIR /root/local_experiments
