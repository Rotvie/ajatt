# Notes for agents

This repo is a personal Japanese-immersion (AJATT) setup: configuration for the tools, plus
resources for the Anki collection they feed. Read this before changing anything.

## What matters here

| Path | What it is |
|---|---|
| `anki/note-types/sentence-mining-jp/` | The Anki note type. `install.py` creates or updates it via AnkiConnect. **Source of truth for the templates** — do not hand-edit them in the Anki GUI, edit the files and re-run the installer |
| `anki/reference/` | How the deck is formatted and how to edit it safely — `fields`, `conventions`, `pitfalls`, `operations`. Read before touching note content |
| `anki/scripts/` | Plain Python over AnkiConnect. `snapshot.py` first, always |
| `.claude/skills/sentence-mining-jp/` | Claude Code skill; a pointer into `anki/`, loads automatically inside this repo |
| `anki/card-formulation/` | Policy for what makes a good card. Apply it before creating cards |
| `mpv/`, `yt-dlp/` | Tool configs. Plain dotfiles. `mpv/script-opts/subs2srs.conf` maps mpvacious onto the note type's fields |
| `yomitan/` | Browser-side setup, done by hand: dictionaries and the Anki field mapping. Must stay consistent with `subs2srs.conf` — Yomitan leaves `SentAudio`, `Image`, `Source` empty for mpvacious |

## If you are adding cards

`anki/reference/adding-cards.md` — inputs, how each field is built, the duplicate check,
and what to leave empty. `anki/card-formulation/` decides whether a sentence should be a
card at all. Readings are looked up, never guessed.

## If you are editing the Anki collection

Read `anki/reference/` first — field spec, formatting rules, failure modes. Helper scripts
are in `anki/scripts/`. The short version:

1. **Anki must be running.** AnkiConnect is on `http://localhost:8765`.
2. **Snapshot before any bulk edit** — `python3 anki/scripts/snapshot.py ./backup`.
   It dumps every field of every note, which is what makes a bad pass reversible.
3. **Dry-run first, printing every before/after pair.** Aggregate counts hide the errors that
   matter; a diff does not.
4. **Verify after writing** by re-deriving the value from the note's own data, and confirm no
   unintended field changed.
5. **Skip rather than guess.** A skipped note is a todo; a wrong write is damage.

Three things that look like markup and are not:

- `VocabPitchPattern` — the `<span style="text-decoration:overline">` tags and `ꜜ` **are**
  the pitch data. An HTML cleanup destroys it.
- `漢字[かな]` furigana brackets — plain text, and load-bearing.
- `X[a,b]` vs `X[a, b]` — differ by one space and mean different things. See
  `anki/reference/conventions.md`.

Adding or removing a note-type **field** is a schema change that forces a one-way full sync
to AnkiWeb. Never do it without being asked.

After a template change, card count must still equal note count — otherwise the
`{{#MakeProductionCard}}` gate broke and Anki generated a second card per note.

## If you are editing configs

They are copied into place, not symlinked, so editing a file here does not change a running
tool until it is copied again. Each folder's README gives the destination path.

Nothing third-party is checked in. `mpv/install.sh` fetches the mpv scripts from upstream
at the versions it pins — do not vendor them into the repo; that is what created the
licensing sprawl this replaced.

## Licensing

MIT, except `anki/note-types/sentence-mining-jp/`, which is GPL-3.0 and carries its own
LICENSE. Keep it that way.
