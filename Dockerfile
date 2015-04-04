FROM resin/rpi-raspbian:jessie
RUN apt-get update
RUN apt-get install wget deluge-common rsync openssh-client git -y && \
    wget https://bootstrap.pypa.io/get-pip.py && \
    python get-pip.py && \
    pip install sh

WORKDIR /opt

ADD deluge_download.py ./
ADD container_entrypoint.sh ./
RUN chmod +x container_entrypoint.sh

VOLUME ["/data"]
VOLUME ["/root/.ssh"]

CMD ["./container_entrypoint.sh"]
