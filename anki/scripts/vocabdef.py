"""Extract the dictionary headword and its reading from a VocabDef field.

Entries look like:   しりょう【資料】     し-りょう―レウ[1]【資料】
The reading may be broken by '-' or '・' syllable separators, which are not
part of the reading itself.
"""
import re

TAG = re.compile(r'<[^>]+>')
HEAD = re.compile(r'【([^】]+)】')
# kana, long-vowel mark, and the separators dictionaries insert
READ = re.compile(r'([぀-ヿー\-‐‑–—−・]+)\s*【')
SEPARATORS = str.maketrans("", "", "-‐‑–—−・")


def clean(s):
    return TAG.sub('', s)


RUBY = re.compile(r'([一-鿿々〆ヶ぀-ヿ]+)\[([^\]]+)\]')
CJK = re.compile(r'[一-鿿々〆ヶ぀-ヿ]')


def headwords(vocabdef):
    """Words listed in 【…】.

    Notes:
      - some entries carry ruby inside the brackets: 【恒星[こうせい]】
      - 大辞泉 marks okurigana boundaries with '=' : 【逆＝上せる】
      - for loanwords 【…】 holds the FOREIGN ETYMOLOGY, not the word
        (マンネリズム【mannerism】), so Latin-only entries are rejected
    """
    d = clean(vocabdef)
    out = []
    for m in HEAD.findall(d):
        for h in re.split(r'[・／/]', m):
            h = RUBY.sub(r'\1', h)
            h = re.sub(r'[△×（）()＝=‐-]', '', h).strip()
            if h and CJK.search(h):
                out.append(h)
    return out


def reading(vocabdef):
    m = READ.search(clean(vocabdef))
    if not m:
        return None
    r = m.group(1).translate(SEPARATORS).strip()
    return r or None
