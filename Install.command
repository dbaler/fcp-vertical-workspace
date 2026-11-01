#!/bin/zsh
# Installs the Vertical workspace into Final Cut Pro.
cd "$(dirname "$0")"
DEST=~/Library/Application\ Support/Final\ Cut\ Pro/Workspaces
mkdir -p "$DEST"
cp Vertical.fcpworkspace "$DEST/"
echo "Installed. Quit and reopen Final Cut Pro, then choose Window > Workspaces > Vertical."
