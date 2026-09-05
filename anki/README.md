# Anki

[Anki](https://apps.ankiweb.net/) is the SRS the whole workflow feeds into. Cards come from
immersion — mined out of mpv with [mpvacious](https://github.com/Ajatt-Tools/mpvacious) —
and are reviewed daily.

```
anki/
├── card-formulation/                what makes a card cheap or expensive to review
├── note-types/sentence-mining-jp/   the note type + install.py
├── reference/                       how the deck is formatted, and how to edit it safely
│   ├── adding-cards.md              turning a mined sentence into a note
│   ├── fields.md                    the 13 fields and their exact formats
│   ├── conventions.md               furigana notation, pitch derivation, bracket forms
│   ├── pitfalls.md                  failure modes, and the habits that catch them
│   └── operations.md                backups, template edits, invariants
└── scripts/                         plain Python helpers over AnkiConnect
```

## Add-ons

Installed — the setup depends on these:

| Add-on | Why |
|---|---|
| [AnkiConnect](https://ankiweb.net/shared/info/2055492159) | Local API. How mpvacious, `install.py` and every script here reach Anki |
| [Review Heatmap](https://ankiweb.net/shared/info/1771074083) | Consistency at a glance — the thing AJATT actually runs on |

Worth considering — not installed here, but they do at mining time what the scripts in this
repo do in bulk afterwards:

| Add-on | Why |
|---|---|
| [AJT Japanese](https://ankiweb.net/shared/info/1344485230) | Generates furigana and pitch accent on new cards. Replaces the older *AJT Furigana* and *AJT Pitch Accent* add-ons |
| [AJT Flexible Grading](https://ankiweb.net/shared/info/1715096333) | Pass/fail grading suited to sentence cards |
| [AJT Media Converter](https://ankiweb.net/shared/info/1151815987) | Shrinks pasted screenshots to WebP — mined cards accumulate fast |

## Setup

1. Install Anki, then AnkiConnect at minimum (Tools → Add-ons → Get Add-ons, paste the
   code from the link). Restart Anki.
2. Create the note type — see [note-types/sentence-mining-jp/](note-types/sentence-mining-jp/).
3. Install [mpvacious](https://github.com/Ajatt-Tools/mpvacious) in mpv and point it at that
   note type, so `Ctrl+E` during playback creates a card.
4. Read [`reference/conventions.md`](reference/conventions.md) before writing any script
   that edits notes in bulk.

AnkiConnect listens on `http://localhost:8765` and only works while Anki is running.

## Working on the collection programmatically

`updateNoteFields` writes only the fields you pass, which makes targeted bulk edits safe.
Two habits worth keeping:

- **Snapshot every field of every note before a bulk edit.** It is what makes a bad pass
  reversible field-by-field, and it costs a couple of MB.
- **Dry-run first, printing every before/after pair.** Regexes over furigana and HTML go
  wrong in ways that are obvious in a diff and invisible in aggregate counts.

### Scripts

`scripts/` holds plain Python over AnkiConnect — no MCP server, no bridge process, usable
from any agent harness or on their own:

| Script | Does |
|---|---|
| `anki.py` | Minimal AnkiConnect client: read, update, `can_add`, `add_note` |
| `snapshot.py` | Dump every field of every note before a bulk edit |
| `furigana.py` | `align("目指す", "めざす")` → `目指[めざ]す` |
| `pitchnum.py` | Derive the accent number from `VocabPitchPattern` |
| `vocabdef.py` | Pull headword and reading out of a dictionary definition |
| `accentdb.py` | Look up accents in the NHK-derived table |

```sh
python3 anki/scripts/snapshot.py ./backup   # run this before touching anything
```

[`reference/pitfalls.md`](reference/pitfalls.md) is the list of ways bulk edits actually went
wrong, and why the dry-run habit is worth keeping.

### Data sources

| Source | Licence | For |
|---|---|---|
| [kanjium](https://github.com/mifunetoshiro/kanjium) | CC BY-SA 4.0 | Pitch accent for 124k words — fills `VocabPitchNum`, and cross-checks values derived from `VocabPitchPattern` |
| [jpdb](https://jpdb.io) | — | Pitch, monolingual definition and examples for one word. Linked from the card |

Fetch instructions and attribution are in [`data/`](data/).

Cross-check pattern-derived accents against the table: where they disagree, the stored
pattern is usually the corrupt one.

For card *formulation* — what makes a good card rather than how to write one — see
[`card-formulation/`](card-formulation/). A Claude Code skill in `.claude/skills/` loads all of this automatically.
