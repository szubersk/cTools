#!/bin/sh

set -exuo pipefail

if ! mountpoint -q /tmp; then
  mount -t tmpfs tmpfs /tmp
fi

if ! mountpoint -q /var/lib/rancher; then
  mount -t tmpfs tmpfs /var/lib/rancher
fi

exec /sbin/init
