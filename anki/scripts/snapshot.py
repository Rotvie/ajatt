#!/usr/bin/env python3
"""Snapshot every field of every note before a bulk edit.

    python3 snapshot.py [outdir]

Writes <outdir>/fields-snapshot-<timestamp>.json mapping noteId -> {field: value}.
The filename carries a time, not just a date, so repeated snapshots in one
session never overwrite an earlier baseline.
This file is what makes a bulk write reversible field-by-field. Take one every
time, even for a "small" pass.
"""
import datetime, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from anki import all_notes, fields, NOTE_TYPE

out = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
out.mkdir(parents=True, exist_ok=True)
notes = all_notes()
snap = {str(n["noteId"]): fields(n) for n in notes}
stamp = datetime.datetime.now().strftime("%Y-%m-%dT%H%M%S")
path = out / f"fields-snapshot-{stamp}.json"
path.write_text(json.dumps(snap, ensure_ascii=False, indent=0), encoding="utf-8")
print(f"{len(snap)} notes from '{NOTE_TYPE}' -> {path}")
