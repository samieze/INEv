#!/bin/bash
set -x

cat config-local >> ~/.ssh/config
cp ./sm22-repro ~/.ssh/sm22-repro
chmod og-rwx ~/.ssh/sm22-repro
