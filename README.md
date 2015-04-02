# Deluge Download

Dockerized python script which connects to a deluge daemon and uses rsync to download labeled torrents. Also performs a git pull before running so updates can be automatically applied.

Can run as an upstart job using:

/etc/init/deluge_download.conf
```
description "Deluge download container"
author "Me"
start on filesystem and started docker
stop on runlevel [!2345]
env DELUGE_DOWNLOAD_DIR=
env DELUGE_HOST=
env DELUGE_USER=
env DELUGE_PASS=
respawn
script
  /opt/deluge_download/run_container.sh
end script
```
