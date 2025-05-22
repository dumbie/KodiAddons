#!/bin/bash
#UTF-8 / EOL LF

docker rm -vf $(docker ps -aq)
docker rmi -f $(docker images -aq)
docker volume prune -f
docker system prune -a -f
docker image prune -a -f

rm -rf /var/lib/docker/
mkdir /var/lib/docker/

rm -rf /storage/.kodi/userdata/addon_data/service.system.docker/docker/
mkdir /storage/.kodi/userdata/addon_data/service.system.docker/docker/