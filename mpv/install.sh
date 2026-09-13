#!/bin/sh
# Install this mpv configuration, then fetch the third-party scripts it uses.
#
#   sh mpv/install.sh                       # -> ~/.config/mpv
#   MPV_HOME=/some/dir sh mpv/install.sh
#
# Third-party code is fetched rather than vendored, so each project keeps its
# own licence and this repo carries none of them:
#
#   uosc       tomasklaen/uosc          4.6.0 (pinned)   LGPL-2.1
#   thumbfast  po5/thumbfast            master           MPL-2.0
#   autoload   mpv-player/mpv           master           LGPL-2.1+
#   recent     hacel/recent             master           (no licence stated)
#   bookmarker NurioHin/mpv-bookmarker  master           (no licence stated)
#   mpvacious  Ajatt-Tools/mpvacious    v26.7.28.0       GPL-3.0
#
# uosc is pinned because 5.x changed its layout and this config is untested
# against it. Bump the version below when you've tried it.
#
# mpvacious is pinned to the release this config was checked against: its
# subs2srs.conf keys and key bindings change between releases.
set -eu
UOSC_VERSION=4.6.0
MPVACIOUS_VERSION=v26.7.28.0
HERE=$(cd "$(dirname "$0")" && pwd)
DEST=${MPV_HOME:-$HOME/.config/mpv}
RAW=https://raw.githubusercontent.com

mkdir -p "$DEST/scripts" "$DEST/script-opts"
cp "$HERE/mpv.conf" "$HERE/input.conf" "$DEST/"
cp "$HERE/script-opts/"* "$DEST/script-opts/"
cp "$HERE/scripts/"*.lua "$DEST/scripts/"

echo "fetching uosc $UOSC_VERSION"
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
curl -sSL -o "$TMP/uosc.zip" "https://github.com/tomasklaen/uosc/releases/download/$UOSC_VERSION/uosc.zip"
unzip -qo "$TMP/uosc.zip" -d "$DEST"           # ships scripts/uosc.lua, scripts/uosc_shared/, fonts/

for spec in \
  "scripts/thumbfast.lua        po5/thumbfast/master/thumbfast.lua" \
  "script-opts/thumbfast.conf   po5/thumbfast/master/thumbfast.conf" \
  "scripts/autoload.lua         mpv-player/mpv/master/TOOLS/lua/autoload.lua" \
  "scripts/recent.lua           hacel/recent/master/recent.lua" \
  "scripts/bookmarker-menu.lua  NurioHin/mpv-bookmarker/master/bookmarker-menu.lua"
do
  set -- $spec
  echo "fetching $1"
  curl -sSL -o "$DEST/$1" "$RAW/$2"
done

echo "fetching mpvacious $MPVACIOUS_VERSION"
curl -sSL -o "$TMP/mpvacious.zip" "https://github.com/Ajatt-Tools/mpvacious/releases/download/$MPVACIOUS_VERSION/mpvacious_$MPVACIOUS_VERSION.zip"
rm -rf "$DEST/scripts/mpvacious"
unzip -qo "$TMP/mpvacious.zip" -d "$DEST/scripts"   # ships scripts/mpvacious/

echo "done -> $DEST"
