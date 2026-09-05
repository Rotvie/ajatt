# Sentence Mining JP — note type

The Anki note type I use for Japanese sentence mining, derived from
**mpvacious cards v13** ([Ajatt-Tools](https://github.com/Ajatt-Tools/AnkiNoteTypes)) and
reworked. Pairs with [mpvacious](https://github.com/Ajatt-Tools/mpvacious), which creates
the cards from mpv.

> **Licence:** GPL-3.0 (see [LICENSE](LICENSE)) — inherited from the note type it derives
> from, unlike the rest of this repository, which is MIT.

A rendered card is in the [root README](../../../README.md#the-loop).

## Fields

`SentKanji` `SentFurigana` `SentAudio` `VocabKanji` `VocabFurigana` `VocabPitchPattern`
`VocabPitchNum` `VocabDef` `VocabAudio` `Image` `Notes` `MakeProductionCard` `Source`

Exact formats: [`../../reference/fields.md`](../../reference/fields.md).

## Cards

**Recognition** — front shows the sentence with no readings; back adds furigana, the pitch
line, `【word】`, the definition, images and dictionary links.

**Production** — gated on `MakeProductionCard`, so it generates nothing until you fill that
field. Front hides the target word behind its kana shape; back shows stroke order.

## Pitch accent colouring

When `VocabPitchNum` is set, the bolded word on the front is coloured by accent type:

| Colour | Accent | Type |
|---|---|---|
| Blue | `0` | 平板 heiban |
| Red | `1` | 頭高 atamadaka |
| Green | `n` == mora count | 尾高 odaka |
| Orange | otherwise | 中高 nakadaka |

## Dictionary links

Built in JavaScript with `encodeURIComponent`, because Anki has no URL-encoding filter and
static hrefs break on sentences containing `?`, `&` or `%`. All keyed on the **word**, not
the sentence, and all monolingual:

| Link | Gives |
|---|---|
| Kotobank | 大辞泉 + 日本国語大辞典 (the on-card definition is 大辞林, so this complements it) |
| Massif | written usage from novels, shows register and frequency |
| ImmersionKit | anime/drama sentences with audio and screenshots |
| jpdb | pitch accent, monolingual definition, kanji breakdown, examples |
| YouGlish | the word spoken by many real speakers |


## Installing

With Anki running and [AnkiConnect](https://ankiweb.net/shared/info/2055492159) installed:

```sh
python3 install.py            # dry run - says what it would do
python3 install.py --apply
```

It creates the note type if missing, or updates the templates and styling if it already
exists. `model.json` holds the field list and order; each template is its `.html` plus
`shared.js` wrapped in a `<script>` tag, so the script lives in one plain file rather than
four diverging copies embedded in HTML.

**Fields are never changed automatically.** Adding or removing one is a schema change that
forces a one-way full sync to AnkiWeb, so the installer reports a mismatch and stops.

The installer also checks the card count before and after: it must not change, or the
`{{#MakeProductionCard}}` gate on the Production front has broken and Anki has generated a
second card for every note.

### By hand

Create a note type with the fields above in that order. For each of the four templates,
paste the `.html` file, then `shared.js` wrapped in `<script>…</script>` at the end.
