set -e
docker build -t deluge_download .

: ${DELUGE_DOWNLOAD_DIR:?"Need to set environment variable DELUGE_DOWNLOAD_DIR"}
: ${DELUGE_HOST:?"Need to set environment variable DELUGE_HOST"}
: ${DELUGE_USER:?"Need to set environment variable DELUGE_USER"}
: ${DELUGE_PASS:?"Need to set environment variable DELUGE_PASS"}
: ${RSYNC_USER:?"Need to set environment variable RSYNC_USER"}
: ${RSYNC_PASS:?"Need to set environment variable RSYNC_PASS"}

docker run -d \
       --restart=on-failure:2 \
       -v $DELUGE_DOWNLOAD_DIR:/data \
       -e RSYNC_USER=$RSYNC_USER \
       -e RSYNC_PASS=$RSYNC_PASS \
       -e DELUGE_HOST=$DELUGE_HOST \
       -e DELUGE_USER=$DELUGE_USER \
       -e DELUGE_PASS=$DELUGE_PASS \
       --name deluge_download \
       deluge_download
