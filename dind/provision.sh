#!/bin/sh

set -exuo pipefail

startTime=$(date +%s)

DOCKER_CHANNEL=stable
DOCKER_VERSION=19.03.8
PYTHON_VERSION=3.8

(wget -O docker.tgz "https://download.docker.com/linux/static/${DOCKER_CHANNEL}/x86_64/docker-${DOCKER_VERSION}.tgz" && \
  tar --extract --file docker.tgz --strip-components 1 --directory /usr/local/bin/ && rm -f docker.tgz) &
(apk add --no-cache python3=~${PYTHON_VERSION} iptables ca-certificates && python3 -m pip install -U pip tox) &

addgroup --system docker
adduser --system -G docker docker

wait

mkdir -p /etc/docker /var/lib/docker
mv /tmp/daemon.json /etc/docker/daemon.json

echo Provisioning took $(( $(date +%s) - ${startTime} )) seconds
