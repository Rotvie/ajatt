# Operations

## Environment

- Anki profile: whatever `getActiveProfile` returns. Check it before writing, so a
  script never edits the wrong collection.
- Deck and note type: both named **Sentence Mining JP**; one deck, no subdecks
- One card per note (Recognition). Production is gated and generates nothing by default
- Check which add-ons are installed before assuming a field is auto-generated.
  If there is no pitch-accent or furigana add-on, anything that looks auto-filled
  was done by hand or by a script.

## Invariant worth checking

**Cards must equal notes.** If a template edit changes the count, the
`{{#MakeProductionCard}}` gate on the Production front was broken and Anki has generated
a second card per note. Check before and after every template write:

```python
len(anki("findCards", query='note:"Sentence Mining JP"'))
```

The note type and templates live in `anki/note-types/sentence-mining-jp/`; use its
`install.py` rather than hand-editing templates in the Anki GUI.

## Backups

Two kinds, both cheap. Take both before anything structural:

```python
# 1. full deck package: media + scheduling, restorable via File > Import
anki("exportPackage", deck="Sentence Mining JP",
     path="/absolute/path/deck-YYYY-MM-DD.apkg", includeSched=True)
```

```bash
# 2. field-level snapshot: enables exact per-field revert
python3 scripts/snapshot.py ./backup
```

The `.apkg` restores everything but is coarse. The JSON snapshot is what you diff against
to prove a pass only changed what it intended.

## Editing the card templates

```python
anki("updateModelTemplates", model={"name": "Sentence Mining JP", "templates": {
        "Recognition": {"Front": front_html, "Back": back_html},
        "Production":  {"Front": front_html, "Back": back_html}}})
anki("updateModelStyling",  model={"name": "Sentence Mining JP", "css": css})
```

Read the current ones first with `modelTemplates` / `modelStyling` and save them.

**Template and CSS edits sync normally.** Adding, removing or renaming a *field* is a
**schema change** and forces a one-way full sync to AnkiWeb — never do it casually.

Anki silently ignores unknown template filters, so a stale filter such as
`{{morphHighlight:…}}` fails invisibly rather than erroring. Do not assume a filter works
because the card renders.

## Verifying a rendered card

`cardsInfo` returns the fully rendered `question` and `answer` HTML — the only way to
check what a card actually produces without opening Anki:

```python
cid = anki("findCards", query=f"nid:{note_id}")[0]
html = anki("cardsInfo", cards=[cid])[0]["answer"]
```

## Telling your edits from the user's

`noteId` is the creation time in milliseconds; `mod` is the last-modified time in seconds.
A cluster of notes modified ~30 seconds apart is a human clicking through the browser; a
script writes hundreds within a second. Use this before blaming a script — or an add-on —
for an unexpected change.
