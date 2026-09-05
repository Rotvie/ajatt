# Adding a card

What an agent needs to turn a mined sentence into a note. Read
[`../card-formulation/`](../card-formulation/) first for *whether* to card it; this is
*how*.

## Inputs

| You need | Where it comes from |
|---|---|
| The sentence, plain Japanese | The subtitle line, the text you were given |
| The target word — **exactly one** unknown | The learner says which; the i+1 gate is theirs to pass |
| The word's dictionary form and reading | jpdb, Kotobank, or the dictionary app. Never guess a reading |
| A monolingual definition | Same sources. Japanese only — no English glosses |
| Readings for the other kanji words in the sentence | Needed for `SentFurigana`. From the subtitle's furigana if it has any, otherwise look them up |
| Image / audio | Optional. mpvacious captures these; by hand they're usually skipped |

## Build the fields

```python
import sys; sys.path.insert(0, "anki/scripts")
from anki import add_note, can_add
from furigana import align
from accentdb import AccentDB

word, reading = "報い", "むくい"                  # dictionary form + reading, looked up
sentence = "これは美穂いじめの報いなんじゃないのかな"

acc, _ = AccentDB().lookup(word, reading)      # None if the table lacks it -> leave empty

fields = {
    "SentKanji":     sentence.replace(word, f"<b>{word}</b>", 1),
    "SentFurigana":  "これは 美穂[みほ]いじめの <b>報[むく]い</b>なんじゃないのかな",
    "VocabKanji":    word,
    "VocabFurigana": align(word, reading),     # 報[むく]い
    "VocabPitchNum": str(acc[0]) if acc else "",
    "VocabDef":      "よいことあるいは悪いことをした結果として，身に受けるもの。",
    "Source":        "the show / episode / book",
}
```

`SentFurigana` is the one field that can't be generated from a single lookup: every kanji
word in the sentence gets `漢字[かな]`, with a space before each kanji run that doesn't start
the string. `align()` builds each word; you assemble the sentence. Formats are in
[`fields.md`](fields.md), the notation in [`conventions.md`](conventions.md).

Leave empty rather than fill wrongly: `VocabPitchPattern` (no way to generate it without
a pitch add-on), `VocabPitchNum` when the table has no entry, `SentAudio`, `VocabAudio`,
`Image`, `Notes`, `MakeProductionCard`.

## Add it

```python
assert can_add(fields)                         # duplicate check, on SentKanji
before = len(anki("findCards", query='note:"Sentence Mining JP"'))
nid = add_note(fields, tags=["mined"])
after  = len(anki("findCards", query='note:"Sentence Mining JP"'))
assert after == before + 1                     # one note, one card
```

`can_add` compares `SentKanji` with HTML stripped, but a different space character or
punctuation slips past it. Also search before adding — `findNotes` with
`"VocabKanji:報い"` — and tell the learner if the word is already carded.

Then read it back with `notesInfo` and confirm every field holds what you sent. If the
learner is watching, show them the card before adding — a wrong reading in `SentFurigana`
is worse than no furigana.

## Do not

- Put readings in `SentKanji`. That's the front; it defeats the card.
- Store the inflected form in `VocabKanji`. `目指そう` in the sentence, `目指す` in the field.
- Invent a pitch number. Empty is correct; wrong is a lie the colouring repeats every review.
- Card a sentence with two unknowns. Flag it back.
