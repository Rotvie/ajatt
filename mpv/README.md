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
| mpvacious — cards from playback | [Ajatt-Tools/mpvacious](https://github.com/Ajatt-Tools/mpvacious) | **v26.7.28.0**, pinned; config keys and bindings change between releases |

Re-running the script **overwrites** `~/.config/mpv/script-opts/subs2srs.conf` with the one
here. mpvacious needs `ffmpeg` only if `use_ffmpeg=yes`; by default mpv encodes the media.

## What's here

```
install.sh            copy config + fetch scripts
mpv.conf              player settings
input.conf            key bindings (zoom, pan, rotate, bookmarks)
script-opts/          per-script settings — subs2srs.conf is mpvacious
scripts/              play-on-startup.lua — the one script that's mine
```

`mpv.conf` sets the subtitle font to Kaiti SC (Chinese brush style, ships with macOS; some kanji take
Chinese glyph forms — `Hiragino Kaku Gothic Pro` is the Japanese alternative) and
points mpv at Homebrew's `yt-dlp`, so `mpv <YouTube URL>` streams.

## mpvacious

[mpvacious](https://github.com/Ajatt-Tools/mpvacious) cuts sentence audio and a screenshot
out of playback and writes them to Anki through AnkiConnect. **Anki must be running.**

It does not look words up. The word, definition, furigana and pitch come from
[Yomitan](../yomitan/); mpvacious attaches media to the card Yomitan just made.

### Mining loop

1. Play a video with Japanese text subtitles. Each line is copied to the clipboard as it
   appears (`autoclip=yes`) and shows up in Yomitan's search page.
2. Pause on a line with one unknown word. `Shift` + hover it in Yomitan, click **＋**.
3. Within ~2 s mpvacious spots the new card and adds `SentAudio`, `Image` and `Source`.
   If it doesn't, `Ctrl+m` in mpv.

`Ctrl+n` makes a sentence-only card without Yomitan.

### `script-opts/subs2srs.conf`

Only the settings that matter are set; everything else is an upstream default.

| Setting | Value | Why |
|---|---|---|
| `deck_name` / `model_name` | `Sentence Mining JP` | The [note type](../anki/note-types/sentence-mining-jp/) |
| `sentence_field` | `SentKanji` | Yomitan fills it too; mpvacious keeps Yomitan's `<b>` on the target word |
| `audio_field` / `image_field` | `SentAudio` / `Image` | Filled only if empty — Yomitan must leave them blank |
| `vocab_field` / `vocab_audio_field` | `VocabKanji` / `VocabAudio` | |
| `miscinfo_field` | `Source` | Show, episode, timestamp. Keeps `Notes` free |
| `secondary_field` | *(empty)* | No English sentence field |
| `autoclip` | `yes` | The hand-off to Yomitan. `Ctrl+t` toggles |
| `enable_new_note_timer` | `yes` | Auto-attaches media to Yomitan's card |
| `snapshot_format` | `avif` | Homebrew mpv/ffmpeg have **no webp encoder** — webp gives no image |
| `audio_padding` | `0.5` | Added to both ends: clip is 1 s longer |

The config is re-read before every card, so edits apply without restarting mpv. Pads are
not applied to timings set by hand in the menu.

## Key bindings

From `input.conf`:

| Key | Does |
|---|---|
| `Alt` `+` / `-` | Zoom in / out |
| `Alt` `h` `j` `k` `l` | Pan |
| `Tab` | Rotate 90° |
| `b` / `B` | Bookmark menu / quick-save |
| `ñ` | Recently-played menu — rebind in `script-opts/recent.conf` |

mpvacious adds its own on top (v26.7.28.0, from its `main.lua`):

| Key | Does |
|---|---|
| `a` | mpvacious menu — set clip start/end by hand for lines with bad timing |
| `Ctrl+n` | New card from the current line |
| `Ctrl+m` | Add audio + screenshot to the last added card (fills empty fields) |
| `Ctrl+M` | Same, but **overwrites** — e.g. to redo a clip after changing `audio_padding` |
| `Ctrl+t` | Toggle clipboard autocopy |
| `Ctrl+c` | Copy the current line by hand |
| `H` / `L` | Previous / next subtitle |

mpvacious's `Alt+h` / `Alt+l` (seek and pause) are shadowed by the pan bindings in
`input.conf`, which take priority over non-forced script bindings.
