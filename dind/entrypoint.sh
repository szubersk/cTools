#!/bin/sh

set -exuo pipefail

if ! mountpoint -q /var/lib/docker; then
  mount -t tmpfs tmpfs /var/lib/docker
fi

exec /usr/local/bin/dockerd --config-file /etc/docker/daemon.json
