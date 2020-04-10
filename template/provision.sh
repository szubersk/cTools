#!/bin/sh

set -exuo pipefail

startTime=$(date +%s)

echo Provision container here

echo Provisioning took $(( $(date +%s) - ${startTime} )) seconds
