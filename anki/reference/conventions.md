# Furigana and pitch conventions

## Bracket notation

Anki's `furigana:` filter turns `漢字[かな]` into `<ruby>`. "Ruby" and "furigana" mean the
same thing here.

A **space precedes every kanji run that does not start the string** — that is how Anki
delimits words:

```
目指[めざ]す              single run at the start, no space
押[お]し 入[い]れ          space before 入
ずる 休[やす]み           space before 休
付[つ]け 焼[や]き 刃[ば]
```

Kana-only words carry **no brackets at all**: `VocabKanji あっさり` / `VocabFurigana あっさり`.

## Building furigana

`scripts/furigana.py::align(word, reading)` distributes a kana reading over a word.

```python
align("目指す", "めざす")        # 目指[めざ]す
align("打ち明ける", "うちあける")  # 打[う]ち 明[あ]ける
align("あっさり", "あっさり")     # あっさり   (unchanged, no kanji)
align("食べる", "たべ")          # None       (cannot align -> skip the note)
```

`align` returns `None` when the reading does not fit the word. **Skip that note**; never
force a value.

Known limit: a single kanji run that is really two words is ambiguous. `慈悲深い` /
`じひぶかい` yields `慈悲深[じひぶか]い`, while the deck sometimes stores
`慈悲[じひ] 深[ぶか]い`. Both render acceptably; the joined form is the convention. Not worth special-casing.

## Pitch accent

`VocabPitchPattern` is HTML and is **content, not styling**:

```
ム<span style="text-decoration:overline;">ク</span>ꜜイ・ム<span ...>クイ</span>
```

The overline marks high pitch and `ꜜ` marks the drop. Stripping the tags destroys the
information. Any HTML-cleaning pass must exclude this field.

`VocabPitchNum` is the accent number the template's colouring script reads. Derive it from
`VocabPitchPattern` (below), or look it up in the kanjium table.

## Sentence formatting

`SentKanji` is plain Japanese. Two things that must never appear in it:

- **ruby** — leaks the reading onto the card front
- **MeCab token spaces** — `実は 　 あんた かなり 評判 に なっ てた` should read
  `実は　あんたかなり評判になってた`

ASCII spaces between Japanese characters are tokenizer residue and should be removed.
Ideographic (`　`) and EN (` `) spaces are real and appear in clean notes — keep them.

## Deriving VocabPitchNum from VocabPitchPattern

`VocabPitchPattern` already encodes the accent number, so it rarely needs looking up.
`scripts/pitchnum.py::derive(pattern)` reads it.

```
カ<span ...>バ</span>ꜜウ    -> 2    morae before the downstep
<span ...>に</span>ꜜんむ    -> 1
ツ<span ...>イキュー</span>  -> 0    no downstep = 平板
```

Details that matter:

- the downstep is `ꜜ` (U+A71C) and also appears as the entity `&#42780;`
- `°` is a nasal-g marker, **not a mora** — counting it inflates the number by one
- small `ゃゅょ` combine with the preceding mora; `ー`, `っ`, `ん` each count as one
- some stored numbers use fullwidth digits (`０`); normalise with NFKC before comparing
- entries may list several accepted accents (`ムクꜜイ・ムクイ`). **Take the first** — that
  is the deck's convention. `derive(..., strict=True)` refuses ambiguous ones instead.

## Cross-checking pitch against the NHK-derived table

`scripts/accentdb.py` reads the [kanjium](https://github.com/mifunetoshiro/kanjium) accent
table (word / reading / positions), fetched into `anki/data/` — see there.

Matching, in order — it never guesses across readings that disagree:

1. `(word, reading)` — reading from `furigana_to_kana(VocabFurigana)`
2. `(word, "")` — kana headwords store a blank reading column
3. word only, **and only when every reading of that word shares one accent**
   (`脅かす` is おどかす=0,3 vs おびやかす=4, so it is refused)

If `VocabFurigana` has no ruby, `furigana_to_kana` returns the kanji — treat that as
"no reading", not as a reading, or matching silently fails.

Use it as an audit as well as a source: a pattern-derived value and the table agreeing is
what makes a bulk fill trustworthy.

Known disagreement classes (do not bulk-overwrite on a mismatch):

- **different reading, both correct** — `経緯` as イキサツ[0] vs ケイイ[1]
- **corrupt `VocabPitchPattern`** — `貪る` stored as `ボꜜル・ムサボꜜル`, first variant a fragment
- **pattern missing its downstep** — `湯呑み`, `高嶺の花` derive 0, dictionary disagrees
- **the table itself can be wrong** — `はにかむ` is [3]; the table says 1

## Comma inside a furigana bracket — two different things

Do not treat these alike. The separator is the tell:

| Form | Meaning | Action |
|---|---|---|
| `X[reading,lemma]` — **no** space | MeCab lemma leaked in | keep the first value: `守[まも,まもる]` → `守[まも]` |
| `[,lemma]` — no space, empty first | kana word, nothing to annotate | delete the whole bracket: `する[,する]` → `する` |
| `X[a, b]` — **space** after comma | genuine alternative readings | **leave alone** |

Where the same base appears cleanly elsewhere in the deck, it is the first value that
matches — that is why it is kept.

The space-separated form is real data — `筒[とう, つつ]`, `経緯[けいい, いきさつ, たてぬき]`,
`鋼[こう, はがね]`. A rule that ignores the separator destroys it while fixing the leaks.

Regex that matches only the leak:  `\[([^\]]*?,(?!\s)[^\]]*)\]`
