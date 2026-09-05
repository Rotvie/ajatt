---
name: sentence-mining-jp
description: >
  Read, edit, and create notes in the "Sentence Mining JP" Anki deck and note type over
  AnkiConnect. Use whenever adding a Japanese card, editing or auditing JP notes, doing
  bulk field fixes, or answering questions about how the deck or its card template works.
  Trigger: "add a card to my JP deck", "sentence mining", "Sentence Mining JP",
  "my Anki Japanese deck", "fix my JP notes".
---

# Sentence Mining JP

A pointer, not a source. The rules live in the repository so they work from any harness.

1. `AGENTS.md` at the repo root — the safe-edit workflow and the hard rules. Already loaded
   if you're inside the repo; read it if not.
2. `anki/reference/adding-cards.md` — to create a note from a mined sentence.
3. `anki/reference/fields.md` — **before writing any field.**
4. `anki/reference/conventions.md` — furigana, pitch, the two bracket forms.
5. `anki/reference/pitfalls.md` and `operations.md` — as needed.

Scripts are plain Python in `anki/scripts/`:

```python
import sys; sys.path.insert(0, "anki/scripts")
from anki import all_notes, fields, write, add_note, can_add
from furigana import align          # align("目指す", "めざす") -> "目指[めざ]す"
from pitchnum import derive         # accent number from VocabPitchPattern
```
