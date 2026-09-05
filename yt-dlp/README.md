# yt-dlp

[yt-dlp](https://github.com/yt-dlp/yt-dlp) downloads immersion material — with Japanese
subtitles embedded, which is what makes it minable later.

## Install

```sh
mkdir -p ~/.config/yt-dlp && cp yt-dlp/config.txt ~/.config/yt-dlp/config
```

**Edit the `-P` line** to your own download directory before using it.

## What the settings do

| Flag | Why |
|---|---|
| `--write-subs` `--embed-subs` | Keep the Japanese subtitles — without them the file can't be mined |
| `--embed-metadata` `--embed-thumbnail` `--embed-chapters` | Self-contained files |
| `--no-mtime` | Timestamp when downloaded, so recent material sorts first |
| `--playlist-reverse` | Oldest first — right for series |
| `--no-abort-on-error` | One dead video doesn't kill a long playlist |
| `--windows-filenames` | Filenames that survive being copied to any filesystem |

`--convert-subs srt` is commented out. Leave it off unless a tool needs SRT — converting
from ASS loses styling and positioning.

mpv streams through yt-dlp directly, so `mpv <url>` works with no download at all.
