# Data

Not tracked — fetch what you need.

## `accents.txt` — pitch accent table

124,137 words with their accent positions. Used by
[`../scripts/accentdb.py`](../scripts/accentdb.py) to fill `VocabPitchNum` and, more
usefully, to **check** values derived from `VocabPitchPattern` against an independent source.

```sh
curl -o anki/data/accents.txt \
  https://raw.githubusercontent.com/mifunetoshiro/kanjium/master/data/source_files/raw/accents.txt
```

From [kanjium](https://github.com/mifunetoshiro/kanjium), **CC BY-SA 4.0**.

> The pitch accent notation was provided by Uros O. through his free database.

Not vendored here: it's ~3 MB, it changes upstream, and fetching keeps the attribution
pointing at the source rather than at a stale copy.
