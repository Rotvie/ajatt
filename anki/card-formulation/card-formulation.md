# Card Formulation Policy

> Personal policy for formulating Anki cards for Japanese, with LLM-assisted sentence
> mining. Adapted from Piotr Woźniak's [Twenty Rules of Formulating Knowledge](https://www.supermemo.com/en/blog/twenty-rules-of-formulating-knowledge).
> This is a living document and will evolve.

## The premise

How a card is formulated dominates the cost of learning it — the same content, well- vs.
badly-formed, differs enormously in review effort. Woźniak's minimum information principle
(each item retrieves the smallest possible unit) is the highest-leverage lever. This doc is
what changes when (a) an **agent** formulates cards via
[AnkiConnect](https://ankiweb.net/shared/info/2055492159) — the add-on exposing Anki's local
HTTP API — instead of a human by hand, and (b) the language is **Japanese**, where the
doctrine partly breaks.

## Who owns which rule (for an automated registrar)

The twenty rules don't all belong to the agent. Sorting them by owner is the actual design:

- **Hard automated gates** — the agent just enforces these: minimum information principle
  (as the i+1 gate, for sentence cards), no sets or enumerations, source-stamp, duplicate
  check, monolingual definition.
- **LLM rewrite passes** — automatable judgment: wording, and — for card types that
  atomize — splitting an overloaded card into atomic ones (the "Dead Sea" move).
- **User-facing flags, never automation** — don't register what the learner doesn't
  understand; personalization / emotional cues. The best hooks come from the learner's own
  associations; an agent inventing them produces generic filler. Surface these as prompts.

## The Japanese exception

**The minimum information principle actively fights language cards where the sentence is the
unit of meaning.** Collocations, readings-in-context, and particle nuance live in the
sentence; atomizing them destroys the thing being learned and can *worsen* interference
between confusables (けど / けれど / が, look-alike kanji). Atomization is not a universal
good — it is card-type-dependent.

The classic failure — ease-hell leech sentences — is usually blamed on sentence length. It's
not: the real cause is **multiple unknowns per card**, not the sentence frame itself.

Definitions are **monolingual**. A JP→EN gloss on the back trains translation, not reading;
once a learner can parse a dictionary entry, English on a card is a regression.

## Per-card-type policy

| Card type | Atomization stance | Primary risk | Policy |
|---|---|---|---|
| **Vocab** | Atomize hard — one word, one sense | Losing collocation / register | Target word + minimal disambiguating context; one sense per card |
| **Kanji** | Atomize — one keyword/reading | Interference between look-alikes | Isolate, but attach a distinguishing cue vs. known confusables |
| **Grammar** | Moderate — one pattern | A pattern is meaningless without a frame | One pattern + minimal example sentence as scaffold |
| **Sentence (i+1)** | **Do not atomize** — the sentence *is* the unit | Breaking it destroys the meaning | Whole sentence, **exactly one unknown**; context carries the load |

The **i+1 gate** (exactly one unknown word per sentence) keeps sentence cards inside the
minimum-information principle *in spirit* — one question, one answer — without stripping
context. A captured sentence with two or more unknowns is flagged back, not carded.

## In this repo

There is one note type, [Sentence Mining JP](../note-types/sentence-mining-jp/), and it is
a **sentence card**. Every mined item becomes one. The vocab, kanji and grammar rows above
are general policy — they apply only if you add note types for them.

What that means for an agent working here:

- **Applies:** the i+1 gate, monolingual definition, `Source` stamp, duplicate check
  (`can_add`), never register what the learner says they don't understand.
- **Does not apply:** cloze conversion (the note type has no cloze), splitting into atomic
  cards, date-stamping (Anki keeps creation time in the note id). Do not atomize a sentence.

How the fields are built is in [`../reference/adding-cards.md`](../reference/adding-cards.md).

## Boundary: what a static policy cannot own

Genuine interference avoidance requires knowing **what is already in the collection** — a
learner model over review history, not a static doc or prompt. A formulation step can do the
cheap guard AnkiConnect gives for free (`canAddNotes` dupe-checking) and *flag* suspected
confusables, but it must not pretend to own real interference detection. Keep that seam clean
so a retrieval layer can plug in later.
