#!/usr/bin/env bash
#
# ensure-curl.sh — make sure `curl` is available on macOS / Linux.
# Detects the platform package manager and installs curl if missing.
# Safe to run repeatedly: exits 0 immediately when curl already exists.

set -eu

if command -v curl >/dev/null 2>&1; then
  echo "curl already installed: $(command -v curl)"
  exit 0
fi

echo "curl not found. Attempting to install..."

run() {
  if [ "$(id -u)" -eq 0 ]; then
    "$@"
  elif command -v sudo >/dev/null 2>&1; then
    sudo "$@"
  else
    echo "Need root to install. Re-run as root or install sudo, then retry." >&2
    return 1
  fi
}

if command -v brew >/dev/null 2>&1; then
  brew install curl
elif command -v apt-get >/dev/null 2>&1; then
  run apt-get update && run apt-get install -y curl
elif command -v dnf >/dev/null 2>&1; then
  run dnf install -y curl
elif command -v yum >/dev/null 2>&1; then
  run yum install -y curl
elif command -v pacman >/dev/null 2>&1; then
  run pacman -Sy --noconfirm curl
elif command -v apk >/dev/null 2>&1; then
  run apk add --no-cache curl
elif command -v zypper >/dev/null 2>&1; then
  run zypper install -y curl
else
  echo "No supported package manager found. Install curl manually: https://curl.se/download.html" >&2
  exit 1
fi

if command -v curl >/dev/null 2>&1; then
  echo "curl installed: $(command -v curl)"
else
  echo "curl installation failed. Install manually: https://curl.se/download.html" >&2
  exit 1
fi
