FROM resin/rpi-raspbian:jessie
RUN apt-get update
RUN apt-get install wget deluge-common rsync openssh-client -y && \
    wget https://bootstrap.pypa.io/get-pip.py && \
    python get-pip.py && \
    pip install sh
RUN apt-get install -y sshpass

ADD deluge_download.py /opt/
RUN chmod +x /opt/deluge_download.py

ADD run_repeatedly.sh /opt/
RUN chmod +x /opt/run_repeatedly.sh

VOLUME ["/data"]

CMD ["/opt/run_repeatedly.sh", "/opt/deluge_download.py", "600"]
