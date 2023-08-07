#!/usr/bin/env bash
# Post install script for the UI .deb to place symlinks in places to allow the CLI to work similarly in both versions

set -e

ln -s /opt/dogechia/resources/app.asar.unpacked/daemon/dogechia /usr/bin/dogechia || true
ln -s /opt/dogechia/doge-chia /usr/bin/doge-chia || true
