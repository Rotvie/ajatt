"""Minimal AnkiConnect client. Anki must be running."""
import json, subprocess

URL = "http://localhost:8765"
NOTE_TYPE = "Sentence Mining JP"
DECK = "Sentence Mining JP"


def anki(action, **params):
    payload = json.dumps({"action": action, "version": 6, "params": params})
    proc = subprocess.run(["curl", "-s", "-m", "60", "-X", "POST", URL, "-d", payload],
                          capture_output=True, text=True)
    if not proc.stdout:
        raise RuntimeError("no response from AnkiConnect - is Anki running?")
    data = json.loads(proc.stdout)
    if data.get("error"):
        raise RuntimeError(f"{action}: {data['error']}")
    return data["result"]


def all_notes(note_type=NOTE_TYPE):
    return anki("notesInfo", notes=anki("findNotes", query=f'note:"{note_type}"'))


def fields(note):
    return {k: v["value"] for k, v in note["fields"].items()}


def write(note_id, **field_values):
    """Writes ONLY the named fields; everything else on the note is untouched."""
    anki("updateNoteFields", note={"id": note_id, "fields": field_values})


def can_add(note_fields, deck=DECK, note_type=NOTE_TYPE):
    """True if Anki would accept this note - i.e. it is not a duplicate.
    Read-only. Duplicates are judged on the first field, SentKanji."""
    note = {"deckName": deck, "modelName": note_type, "fields": note_fields}
    return anki("canAddNotes", notes=[note])[0]


def add_note(note_fields, tags=(), deck=DECK, note_type=NOTE_TYPE):
    """Create one note. Returns the new noteId. Refuses duplicates.

    note_fields: {field name: value} - missing fields are left empty.
    Check the card count before and after; it must rise by exactly one.
    """
    if not can_add(note_fields, deck, note_type):
        raise ValueError(f"duplicate: {note_fields.get('SentKanji', '')[:40]!r}")
    note = {"deckName": deck, "modelName": note_type,
            "fields": note_fields, "tags": list(tags),
            "options": {"allowDuplicate": False}}
    return anki("addNote", note=note)
