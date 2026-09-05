# mpv

[mpv](https://mpv.io/) is where immersion happens: subtitles, instant dictionary lookups,
and card creation straight out of playback via
[mpvacious](https://github.com/Ajatt-Tools/mpvacious).

## Install

```sh
sh mpv/install.sh            # copies the config to ~/.config/mpv and fetches the scripts
```

`MPV_HOME=/other/dir sh mpv/install.sh` to target somewhere else.

The script copies `mpv.conf`, `input.conf`, `script-opts/` and `scripts/`, then fetches the
third-party scripts — nothing third-party is checked in here, so each project keeps its own
licence:

| Script | Upstream | Version |
|---|---|---|
| uosc — the UI | [tomasklaen/uosc](https://github.com/tomasklaen/uosc) | **4.6.0**, pinned; 5.x changed its layout and is untested here |
| thumbfast — seekbar thumbnails | [po5/thumbfast](https://github.com/po5/thumbfast) | master |
| autoload — queue the folder | [mpv](https://github.com/mpv-player/mpv/blob/master/TOOLS/lua/autoload.lua) | master |
| recent — play history | [hacel/recent](https://github.com/hacel/recent) | master |
| bookmarker — video bookmarks | [NurioHin/mpv-bookmarker](https://github.com/NurioHin/mpv-bookmarker) | master |

Then install [mpvacious](https://github.com/Ajatt-Tools/mpvacious) per its own instructions —
it's the piece that turns playback into Anki cards.

## What's here

```
install.sh            copy config + fetch scripts
mpv.conf              player settings
input.conf            key bindings (zoom, pan, rotate, bookmarks)
script-opts/          per-script settings
scripts/              play-on-startup.lua — the one script that's mine
```

`mpv.conf` sets a Japanese-capable subtitle font (Hiragino, which ships with macOS).

## Key bindings

From `input.conf`:

| Key | Does |
|---|---|
| `Alt` `+` / `-` | Zoom in / out |
| `Alt` `h` `j` `k` `l` | Pan |
| `Tab` | Rotate 90° |
| `b` / `B` | Bookmark menu / quick-save |
| `ñ` | Recently-played menu — rebind in `script-opts/recent.conf` |

mpvacious adds its own bindings on top — `Ctrl+E` to create a card is the important one.
