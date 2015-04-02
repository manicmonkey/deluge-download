#!/usr/bin/env python
 
from deluge.ui.client import client
from twisted.internet import reactor, defer
from sh import rsync # import rsync to be used as a method call
import time
import os
 
# Set up the logger to print out errors
from deluge.log import setupLogger
setupLogger(level='info')
 
import logging
import logging.handlers
 
log = logging.getLogger('DownloadScript')
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
#handler.ident = 'TorrentDownload' python 3.3+
log.addHandler(handler)
 
log.info("Starting... %s", time.strftime("%H:%M:%S %d/%m/%Y"))
 
# Constants
shared_dir='/data'
partial_dir=shared_dir+'/partial'
complete_dir=shared_dir+'/complete'
 
# Pull in environment
deluge_host=os.environ['DELUGE_HOST']
deluge_username=os.environ['DELUGE_USER']
deluge_password=os.environ['DELUGE_PASS']
 
@defer.inlineCallbacks
def process_torrents():
 
    client_connected = False
 
    try:
        yield client.connect(host=deluge_host, username=deluge_username, password=deluge_password)
        client_connected = True
        log.info("Connected to deluge")
        torrents = yield client.core.get_torrents_status({}, ['name','label','progress','save_path','state','files'])
 
        downloads = [{
               'id' : id,
               'location' : torrent['save_path'] + '/' + torrent['name'],
               'label' : torrent['label']
            } for id, torrent in torrents.iteritems() if torrent['progress'] == 100 and torrent['label'].startswith('download')]
 
        log.info('List of torrents to download: %s', downloads)
 
        for torrent in downloads:
            log.info('Downloading torrent: %s', torrent)
 
            remote_location = torrent['location'].replace(' ', '\ ').replace('(', '\(').replace(')', '\)').replace('&', '\&').replace('[', '\[').replace(']', '\]').replace('\'', '\\\'')
            save_location = complete_dir + '/' + torrent['label']
 
            log.info('Remote location: %s', remote_location)
            log.info('Save location: %s', save_location)
 
            result = rsync("-h", "-r", "-T", partial_dir, "--partial", "--progress", "root@little.duckdns.org:" + remote_location, save_location)#, _out="/home/james/download_rsync.log")
            log.info('Got rsync result: %s', result)
            if (result.exit_code == 0):
                log.info('Remove label from torrent: %s', torrent)
                yield client.label.set_torrent(torrent['id'], 'No Label')
 
    except Exception as err:
        log.exception("Error downloading torrent")
 
    finally:
        if client_connected:
            log.info('Disconnecting deluge client')
            yield client.disconnect()
        log.info('Stopping reactor')
        reactor.stop()
 
process_torrents()
# Run the twisted main loop to make everything go
reactor.run()
