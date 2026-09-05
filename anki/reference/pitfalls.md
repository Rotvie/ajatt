# Pitfalls

Failure modes seen in a real mined collection. None are hypothetical.

## Data problems worth checking for

| Symptom | What it is |
|---|---|
| Ruby inside `SentKanji` | Readings leaked onto the card *front*, defeating the point of a recognition card |
| `SentKanji` and `SentFurigana` swapped | The plain sentence is in the furigana field and vice versa |
| Ruby inside `VocabKanji` | The furigana string got written into both vocab fields |
| `X[reading,lemma]` brackets | MeCab lemma leaked into the furigana; see conventions |
| `<divstyle=` `<bodystyle=` `<imgsrc=` | Pasted from a Qt editor, which ate the space before the first attribute. Browsers treat these as unknown elements and render the text anyway, so they are invisible until you grep |
| Images inside `VocabDef` | Render inline in the definition instead of the image block, bypassing the styling |
| HTML / `&nbsp;` inside `VocabKanji` | Shows up inside `【…】` and corrupts links built from the field |

## Traps

- **Comparing "stripped" text is not a safety check.** Verifying two fields match after
  removing ruby passes trivially when one side has no ruby — and would delete the only copy
  of the readings. Require the ruby to be *present and identical*.
- **A field can hold the other field's value.** Check both directions before deciding which
  one is wrong.
- **Dictionary brackets are not all furigana.** For loanwords 【…】 holds the foreign
  etymology — `マンネリズム【mannerism】`. Taking it as the word writes Latin text into a
  Japanese field.
- **One regex, two meanings.** `X[a,b]` and `X[a, b]` differ only by a space and mean
  completely different things. A rule that ignores the separator destroys real data while
  fixing junk.
- **Verifying against an old snapshot flags earlier passes.** Scope each comparison to the
  fields the current pass writes.
- **Date-named snapshots overwrite each other.** Timestamp to the second.

Every one of these was caught by the snapshot-then-dry-run habit in the README, not by
careful coding. When a rule cannot decide, skip and report rather than guess.
