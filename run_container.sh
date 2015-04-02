set -e
docker build -t deluge_download .
docker run --rm -it \
       -v $DELUGE_DOWNLOAD_DIR:/data \
       -v $HOME/.ssh:/root/.ssh \
       -e DELUGE_HOST=$DELUGE_HOST \
       -e DELUGE_USER=$DELUGE_USER \
       -e DELUGE_PASS=$DELUGE_PASS \
       deluge_download $1
