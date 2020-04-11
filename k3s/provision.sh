#!/bin/sh

set -exuo pipefail

startTime=$(date +%s)

echo Provision container here

export INSTALL_K3S_VERSION='v1.17.4%2Bk3s1'

apk add --no-cache openrc
(wget -O - https://get.k3s.io | INSTALL_K3S_SKIP_START=true sh -)

mkdir -p /var/lib/rancher

sed -i '/command_args="server/ c\command_args="server --no-deploy traefik,local-storage \' /etc/init.d/k3s
rc-update add k3s default

echo Provisioning took $(( $(date +%s) - ${startTime} )) seconds
