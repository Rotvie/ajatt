"""Align a dictionary-form word with its kana reading to produce Anki furigana.

Anki delimits furigana words with a space before each kanji run that does not
start the string:  押[お]し 入[い]れ   目指[めざ]す   ずる 休[やす]み
"""
import re

KANJI = r'[一-鿿々〆ヶ]'
IS_KANJI = re.compile(KANJI)
RUBY = re.compile(r'(' + KANJI + r'+)\[([^\]]+)\]')


def segments(word):
    out, cur, cur_k = [], "", None
    for ch in word:
        k = bool(IS_KANJI.match(ch))
        if cur and k != cur_k:
            out.append((cur_k, cur)); cur = ""
        cur, cur_k = cur + ch, k
    if cur:
        out.append((cur_k, cur))
    return out


def furigana_to_kana(s):
    """'押[お]し 入[い]れ' -> 'おしいれ'  (spaces are delimiters, not reading)"""
    return RUBY.sub(r'\2', s).replace(" ", "").replace("　", "")


def align(word, reading):
    word = word.strip()
    reading = reading.replace(" ", "").replace("　", "").strip()
    segs = segments(word)
    if not any(k for k, _ in segs):
        return word                                   # pure kana: no brackets
    m = re.fullmatch("".join("(.+?)" if k else re.escape(t) for k, t in segs), reading)
    if not m:
        return None
    out, gi = [], 0
    for i, (k, t) in enumerate(segs):
        if k:
            gi += 1
            out.append((" " if i else "") + f"{t}[{m.group(gi)}]")
        else:
            out.append(t)
    return "".join(out)
