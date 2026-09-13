# Yomitan

[Yomitan](https://github.com/yomidevs/yomitan) is the dictionary. In this setup it does the
lookup **and** writes the word half of each card — word, reading, definition, word audio.
[mpvacious](../mpv/) then attaches the sentence audio, screenshot and source to that same
card.

> **Browser:** Chrome (or any Chromium) or Firefox. There is no Safari version, and the
> workflow needs background clipboard access anyway.

Nothing to install from this repo — Yomitan's settings live in the browser. This page is the
record of how they're set.

## How it fits together

```
mpv ── subtitle line ──► clipboard ──► Yomitan search page
                                          │  Shift+hover word, click ＋
                                          ▼
                                   Anki card: sentence, word, definition, word audio
                                          ▲
mpvacious ── sees new card with no media ─┘  adds SentAudio, Image, Source (~2 s)
```

The contract between the two: **Yomitan leaves `SentAudio`, `Image` and `Source` empty.**
mpvacious only attaches media to a recent card that has none.

## Setup

1. Install the extension, open its settings.
2. **Dictionaries** → import. Currently installed:
   - 三省堂国語辞典 第八版 — monolingual
   - 実用日本語表現辞典 — monolingual
   - *(no pitch accent dictionary yet — see below)*
3. **Clipboard** → enable background clipboard text monitoring. Also flip the
   **Clipboard monitor** toggle at the top of the search page; allow clipboard permission.
4. **Anki** → enable. **Configure Anki card format**:
   Deck `Sentence Mining JP`, Model `Sentence Mining JP`.

| Field | Yomitan marker | Output seen on real cards |
|---|---|---|
| `SentKanji` | `{cloze-prefix}<b>{cloze-body}</b>{cloze-suffix}` | ` この町に…<b>人畜無害</b>なヤツなんて` — ⚠ leading space from the subtitle |
| `SentFurigana` | `{sentence-furigana}` | ⚠ see below |
| `SentAudio` | *(empty)* | mpvacious: `[sound:…_20m10s292ms_20m13s921ms.ogg]` |
| `VocabKanji` | `{expression}` | `人畜無害` |
| `VocabFurigana` | `{furigana-plain}` | `人畜無害[じんちくむがい]` |
| `VocabPitchPattern` | `{pitch-accents}` | empty until a pitch dictionary is imported |
| `VocabPitchNum` | `{pitch-accent-positions}` | empty until a pitch dictionary is imported |
| `VocabDef` | `{glossary}` | HTML list, one `<li>` per dictionary; `{glossary-first}` for just the first |
| `VocabAudio` | `{audio}` | `[sound:yomitan_audio_….mp3]` |
| `Image` | *(empty)* | mpvacious: `<img alt="snapshot" src="….avif">` |
| `Notes` | *(empty)* | |
| `MakeProductionCard` | *(empty)* | |
| `Source` | *(empty)* | mpvacious: `Monogatari_S01 EP03 (20m13s170ms)` |

## Mining

1. Play in mpv; each subtitle appears in the search page as it's shown.
2. Pause (`Space`) on a line with one unknown word.
3. `Shift` + hover the word, click **＋**.
4. Wait for mpv's confirmation. Nothing after a few seconds → `Ctrl+m` in mpv.

Key bindings and mpvacious settings: [`mpv/`](../mpv/).

## Known gaps

These new cards don't yet match the formats in
[`anki/reference/fields.md`](../anki/reference/fields.md):

- **`SentFurigana` is wrong.** `{sentence-furigana}` writes HTML `<ruby>` (not `漢字[かな]`)
  and reads kanji in isolation: 町→ちょう, 人間→じんかん, 僕→しもべ. Leave the field empty
  and fill it afterwards with a script or AJT Japanese, or fix readings by hand.
- **Pitch fields empty** — no pitch accent dictionary imported. Once one is,
  check that `{pitch-accents}` output matches the overline-span format the card's colouring
  script and `anki/scripts/pitchnum.py` expect.
- **`VocabDef`** is Yomitan's structured HTML, not the plain 大辞林-style text of older cards.
  Renders fine; bulk scripts that parse `【headword】` may not.
- **Leading space** in `SentKanji` when the subtitle line starts with one.
