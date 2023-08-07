#!/usr/bin/env bash
# Pre remove script for the UI .rpm to clean up the symlinks from the installer

set -e

unlink /usr/bin/dogechia || true
unlink /usr/bin/doge-chia || true
