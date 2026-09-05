"""Lookup over the kanjium pitch-accent table.

Data: https://github.com/mifunetoshiro/kanjium (CC BY-SA 4.0). 124,137 words.
      "The pitch accent notation was provided by Uros O. through his free database."

Not vendored - fetch it once:

    curl -o anki/data/accents.txt \
      https://raw.githubusercontent.com/mifunetoshiro/kanjium/master/data/source_files/raw/accents.txt

File format: word <TAB> reading <TAB> accents   (kana headwords leave reading blank)
Accents are comma-separated positions; the first is the primary one.

Useful for filling VocabPitchNum where VocabPitchPattern is absent, and as an
independent check on values derived from the pattern - agreement between the two
is what makes a bulk pitch fill trustworthy.
"""
import re, unicodedata
from collections import defaultdict
from pathlib import Path

PATH = Path(__file__).resolve().parent.parent / "data" / "accents.txt"


def kata_to_hira(s):
    return "".join(chr(ord(c) - 0x60) if "ァ" <= c <= "ヶ" else c for c in s)


def norm(s):
    return kata_to_hira(unicodedata.normalize("NFKC", s or "")).strip()


class AccentDB:
    def __init__(self, path=PATH):
        path = Path(path)
        if not path.exists():
            raise SystemExit(
                f"Accent table not found at {path}\n"
                "Fetch it (CC BY-SA 4.0, https://github.com/mifunetoshiro/kanjium):\n"
                "  mkdir -p anki/data && curl -o anki/data/accents.txt \\\n"
                "    https://raw.githubusercontent.com/mifunetoshiro/kanjium"
                "/master/data/source_files/raw/accents.txt")
        self.by_pair, self.by_word = {}, defaultdict(list)
        for line in path.read_text(encoding="utf-8").splitlines():
            p = line.split("\t")
            if len(p) < 3:
                continue
            word, reading, acc = norm(p[0]), norm(p[1]), p[2]
            vals = [int(x) for x in re.findall(r'-?\d+', acc)]
            if not vals:
                continue
            self.by_pair.setdefault((word, reading), vals)
            self.by_word[word].append(vals)

    def lookup(self, word, reading=None):
        """(accents, how) or (None, reason). Never guesses across differing readings."""
        w = norm(word)
        r = norm((reading or "").split(",")[0])
        if r and (w, r) in self.by_pair:
            return self.by_pair[(w, r)], "word+reading"
        if (w, "") in self.by_pair:
            return self.by_pair[(w, "")], "kana word"
        entries = self.by_word.get(w)
        if not entries:
            return None, "not in dataset"
        primaries = {e[0] for e in entries}
        if len(primaries) == 1:
            return entries[0], "word only (readings agree)"
        return None, f"word has differing accents by reading {sorted(primaries)}"
