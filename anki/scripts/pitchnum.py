"""Derive VocabPitchNum from VocabPitchPattern.

The pattern marks high morae with an overline span and the downstep with 'ꜜ'
(U+A71C, sometimes written as the entity &#42780;). The accent number is the
count of morae before the downstep; no downstep means 平板 = 0.

    カ<span ...>バ</span>ꜜウ   -> 2
    <span ...>に</span>ꜜんむ   -> 1
    ツ<span ...>イキュー</span> -> 0
"""
import html as _html
import re

TAG = re.compile(r'<[^>]+>')
DROP = "ꜜ"                      # ꜜ
SMALL = "ゃゅょャュョ"                # combine with the preceding mora
MARKS = "\u00b0\u309c\u309b"            # nasal-g / dakuten marks: not morae


def plain(pattern):
    """HTML pattern -> plain kana text, entities resolved, tags removed."""
    return TAG.sub("", _html.unescape(pattern)).strip()


def moras(kana):
    return sum(1 for ch in kana if ch not in SMALL and ch not in MARKS)


def _one(variant):
    if not variant:
        return None
    if DROP not in variant:
        return 0 if moras(variant) else None
    n = moras(variant.split(DROP)[0])
    return n if n else None


def derive(pattern, strict=False):
    """Accent number, or None when the pattern is unusable.

    Entries may list several accepted accents separated by '・'. The deck's
    convention is the FIRST variant (29 of 30 existing notes that list variants
    store the first one), so that is the default. strict=True instead returns
    None whenever the variants disagree, leaving the note untouched.
    """
    text = plain(pattern)
    if not text:
        return None
    variants = [v.strip() for v in text.split("・") if v.strip()]
    if not variants:
        return None
    if strict:
        vals = {_one(v) for v in variants}
        vals.discard(None)
        return vals.pop() if len(vals) == 1 else None
    return _one(variants[0])
