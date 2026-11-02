#!/bin/zsh -f
# Installs the Vertical workspace into Final Cut Pro.
set -e

SRC="${0:A:h}/Vertical.fcpworkspace"
DEST="$HOME/Library/Application Support/Final Cut Pro/Workspaces"

if [[ ! -f "$SRC" ]]; then
  echo "Vertical.fcpworkspace was not found next to this installer."
  echo "Unzip the whole folder, then run Install.command from inside it."
  exit 1
fi

mkdir -p "$DEST"

# Keep a copy of any different workspace already called Vertical.
if [[ -f "$DEST/Vertical.fcpworkspace" ]] && ! cmp -s "$SRC" "$DEST/Vertical.fcpworkspace"; then
  cp "$DEST/Vertical.fcpworkspace" "$DEST/Vertical.fcpworkspace.backup"
  echo "Your existing Vertical workspace was saved as Vertical.fcpworkspace.backup."
fi

cp "$SRC" "$DEST/"
echo "Installed. Quit and reopen Final Cut Pro, then choose Window > Workspaces > Vertical."
