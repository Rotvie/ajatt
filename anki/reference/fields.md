# Field reference — Sentence Mining JP

13 fields.

| Field | Purpose and exact format |
|---|---|
| `SentKanji` | The sentence as it should be **read**: plain Japanese, **no ruby**, no MeCab token spaces. Target word wrapped in `<b>`. Shown on the card front. |
| `SentFurigana` | Same sentence **with** ruby in `漢字[かな]` notation, space-delimited between words. Shown on the back. |
| `SentAudio` | `[sound:xxx.mp3]`; cards mined with mpvacious get `.ogg` (opus) |
| `VocabKanji` | Target word in **dictionary form**, plain text: no ruby, no HTML, no spaces. Kana-only words are stored as kana (`あっさり`, `パンク`). Drives the `【…】` display and every footer lookup link. |
| `VocabFurigana` | Same word with ruby (`目指[めざ]す`). Kana-only words repeat the word unchanged. |
| `VocabPitchPattern` | Pitch contour as HTML: `ム<span style="text-decoration:overline;">ク</span>ꜜイ`. **Semantic — never strip these tags.** |
| `VocabPitchNum` | Accent number (`0`,`1`,`2`…). Drives the front-side colouring script. |
| `VocabDef` | Monolingual Japanese definition. Mostly 大辞林-style; some entries from 大辞泉, goo辞書 or Weblio. |
| `VocabAudio` | `[sound:xxx.mp3]` |
| `Image` | `<img src="xxx.webp">`; cards mined with mpvacious get `<img alt="snapshot" src="xxx.avif">` |
| `Notes` | Free text |
| `MakeProductionCard` | Gate for the Production card type. Empty by default; setting it generates a second card for that note. |
| `Source` | Where the sentence came from. Optional. |

## Dictionary-form rule

`VocabKanji` holds the **dictionary form**, not the inflected form from the sentence:

```
sentence 目指そう      -> VocabKanji 目指す
sentence 備わってるんだ -> VocabKanji 備わる
sentence 散っていって   -> VocabKanji 散る
```

The reliable source is the `【headword】` in `VocabDef`, which is already the dictionary
form. `scripts/vocabdef.py::headwords()` extracts it, handling three traps:

- ruby inside the brackets — `【恒星[こうせい]】` → `恒星`
- 大辞泉 okurigana markers — `【逆＝上せる】` → `逆上せる`
- **loanwords put the foreign etymology in the brackets** — `マンネリズム【mannerism】`.
  Latin-only bracket contents are rejected; they are not the word.

## Reading source

`scripts/vocabdef.py::reading()` takes the kana printed before `【…】`. Dictionaries insert
syllable separators there (`がん-らい【元来】`), which are stripped. Fall back to the ruby on
the bolded span in `SentFurigana` when `VocabDef` has no reading.

How the cards render, and the lookup links, are described with the
[note type](../note-types/sentence-mining-jp/).
