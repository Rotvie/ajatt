#!/usr/bin/env python3
"""Create or update the "Sentence Mining JP" note type in Anki.

    python3 install.py              # show what would change
    python3 install.py --apply

Anki must be running with AnkiConnect (add-on 2055492159) installed.

Each template is the matching .html file with shared.js appended inside a
<script> tag, so the script lives in one plain .js file instead of four
diverging copies embedded in HTML.

Field changes are NOT applied automatically: adding or removing a field is a
schema change and forces a one-way full sync to AnkiWeb. If the fields differ,
this tells you and stops.
"""
import argparse, json, subprocess, sys
from pathlib import Path

HERE = Path(__file__).parent
URL = "http://localhost:8765"


def anki(action, **params):
    payload = json.dumps({"action": action, "version": 6, "params": params})
    proc = subprocess.run(["curl", "-s", "-m", "60", "-X", "POST", URL, "-d", payload],
                          capture_output=True, text=True)
    if not proc.stdout:
        sys.exit("No response from AnkiConnect. Is Anki running with the add-on installed?")
    data = json.loads(proc.stdout)
    if data.get("error"):
        sys.exit(f"AnkiConnect error on {action}: {data['error']}")
    return data["result"]


def build():
    spec = json.loads((HERE / "model.json").read_text(encoding="utf-8"))
    shared = "<script>\n" + (HERE / spec["sharedScript"]).read_text(encoding="utf-8").strip() + "\n</script>"
    css = (HERE / spec["styling"]).read_text(encoding="utf-8")
    tmpls = {}
    for t in spec["templates"]:
        front = (HERE / t["front"]).read_text(encoding="utf-8").rstrip()
        back = (HERE / t["back"]).read_text(encoding="utf-8").rstrip()
        tmpls[t["name"]] = {"Front": front + "\n\n" + shared,
                            "Back": back + "\n\n" + shared}
    return spec, css, tmpls


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    spec, css, tmpls = build()
    name = spec["name"]
    existing = anki("modelNames")

    if name not in existing:
        print(f"'{name}' does not exist - it will be CREATED")
        print(f"  fields    : {', '.join(spec['fields'])}")
        print(f"  templates : {', '.join(tmpls)}")
        if not args.apply:
            print("\nDry run. Re-run with --apply."); return
        anki("createModel", modelName=name, inOrderFields=spec["fields"], css=css,
             isCloze=spec["isCloze"],
             cardTemplates=[{"Name": n, "Front": t["Front"], "Back": t["Back"]}
                            for n, t in tmpls.items()])
        print(f"\nCreated '{name}'.")
        return

    print(f"'{name}' already exists - templates and styling will be UPDATED")
    have = anki("modelFieldNames", modelName=name)
    if have != spec["fields"]:
        print("\n  ! Field mismatch - not changing fields (that is a schema change).")
        print(f"    in Anki   : {have}")
        print(f"    expected  : {spec['fields']}")
        missing = [f for f in spec["fields"] if f not in have]
        if missing:
            print(f"    add these by hand first: {missing}")
            sys.exit(1)

    before = len(anki("findCards", query=f'note:"{name}"'))
    print(f"  cards currently : {before}")
    if not args.apply:
        print("\nDry run. Re-run with --apply."); return
    anki("updateModelTemplates", model={"name": name, "templates": tmpls})
    anki("updateModelStyling", model={"name": name, "css": css})
    after = len(anki("findCards", query=f'note:"{name}"'))
    print(f"  cards after     : {after}")
    if after != before:
        print("  ! Card count changed - check the {{#MakeProductionCard}} gate "
              "on the Production front.")
    print(f"\nUpdated '{name}'.")


if __name__ == "__main__":
    main()
