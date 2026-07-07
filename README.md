# All Japanese All The Time (AJATT)

* [All Japanese All The Time (AJATT)](#all-japanese-all-the-time-ajatt)
   * [What is AJATT?](#what-is-ajatt)
   * [My tools](#my-tools)
      * [Anki](#anki)
      * [LLM-assisted Card Formulation](#llm-assisted-card-formulation)
      * [MPV Media Player](#mpv-media-player)
      * [Dictionaries](#dictionaries)
         * [qolibri EPWING dictionary viewer](#qolibri-epwing-dictionary-viewer)
      * [Vimium](#vimium)
      * [AutoHotkey](#autohotkey)
      * [Miscellaneous Tools](#miscellaneous-tools)
      
## What is AJATT?
AJATT is a language learning approach that encourages full immersion in Japanese. It involves surrounding yourself with the language in everyday life, sentence mining for effective vocabulary acquisition, and using timeboxing for focused study periods. Customizable to individual needs, AJATT commonly uses resources like Anki flashcards, Japanese media, and books. Here are a few references:
- [Tatsumoto ToC](https://tatsumoto.neocities.org/blog/table-of-contents.html)
- [AJATT ToC](http://www.alljapaneseallthetime.com/blog/all-japanese-all-the-time-ajatt-how-to-learn-japanese-on-your-own-having-fun-and-to-fluency/)
- [Roadmap|Refold](https://refold.la/roadmap)

## My tools
### Anki
[Anki](https://apps.ankiweb.net/) is a popular and powerful spaced repetition software (SRS) designed to help users with efficient learning. It allows you to create and manage flashcards on various subjects, enabling the reinforcement of memory through regular and strategically timed reviews.

Here are some of the Anki Addons I use: 
- [AJT Flexible Grading](https://ankiweb.net/shared/info/1715096333)
- [AJT Pitch Accent](https://ankiweb.net/shared/info/1225470483)
- [AJT Furigana](https://ankiweb.net/shared/info/1344485230)
- [Review Heatmap](https://ankiweb.net/shared/info/1771074083)
- [Paste Images As WebP](https://ankiweb.net/shared/info/1151815987)
- [Edit Field During Review Cloze](https://ankiweb.net/shared/info/385888438)
- [Add Hyperlink](https://ankiweb.net/shared/info/318752047)

### LLM-assisted Card Formulation
Well-formed cards matter more than the algorithm scheduling them. I use an LLM (Claude, with [AnkiConnect](https://ankiweb.net/shared/info/2055492159)) to formulate and register cards following an explicit policy adapted from Woźniak's [Twenty Rules of Formulating Knowledge](https://www.supermemo.com/en/blog/twenty-rules-of-formulating-knowledge) — with a per-card-type policy table and an i+1 gate for sentence mining (one unknown word per sentence).

- [`card-formulation.md`](card-formulation/card-formulation.md) — the policy: automated gates vs. LLM rewrites vs. user-facing flags, the Japanese exception to atomization, and the per-card-type table.
- [`claude-card-formulation.prompt.md`](card-formulation/claude-card-formulation.prompt.md) — a ready-to-use prompt that applies the policy; drop it into a Claude project. If the session can read this repo, the prompt alone is enough — Claude reads the policy itself. In a plain chat, paste `card-formulation.md` along with it.

**Setup:** install the [AnkiConnect](https://ankiweb.net/shared/info/2055492159) add-on in Anki, then configure the [Anki MCP server](https://github.com/ankimcp/anki-mcp-server) in your Claude client (Claude Desktop or Claude Code) so the agent can reach Anki's local API — AnkiConnect is the add-on exposing the API, the MCP server is the bridge that gives Claude access to it. Anki must be running.

**Workflow:** capture sentences during immersion into a mining inbox; Claude reads the inbox, applies the policy (i+1 gate, per-card-type atomization, dupe-checking via `canAddNotes`), and registers the cards in the target deck with furigana generated at build time.

### MPV Media Player

[MPV](https://mpv.io/) is a powerful, open-source media player appreciated for its cross-platform capabilities, customization, and scripting options. With its light design and wide compatibility with various media formats, it is a favored choice for many.

One of the notable features of MPV is its seamless integration with [yt-dlp](https://github.com/yt-dlp/yt-dlp), an enhanced fork of youtube-dl. This integration allows users to directly stream videos from platforms like YouTube as well as download content. You can find my configuration for yt-dlp in the `yt-dlp` folder.

For language learning, MPV's scripting capacity is a valuable asset. By incorporating Lua scripts, you can tailor MPV to boost your learning experience with additional functionalities. The `mpv` folder in this repository includes my current configuration of MPV.

### Dictionaries
Learning Japanese becomes significantly easier with the help of dictionaries, especially JP-JP ones.

#### qolibri EPWING dictionary viewer
Use [qolibri](https://github.com/ludios/qolibri) to search multiple dictionaries simultaneously. It requires dictionaries in EPWING format.
Here are some downloadable EPWING dictionaries for qolibri:
- [Japanese_Dictionaries](https://www.mediafire.com/folder/ldyklp3362pgg/Japanese_Dictionaries)
- [NHK_Pitch_Accent](https://www.mediafire.com/file/sxmpse8n92c9oxg/NHKACT.zip)

### Vimium
[Vimium](https://vimium.github.io/) is a handy extension that brings the efficiency of Vim-style keyboard navigation to your web browsing experience. With Vimium, you can scroll, follow links, navigate through history, and more, all without leaving your keyboard.
To add an extra layer of convenience, I've created a custom configuration file in the `vimium` folder with my personal key mappings, mainly for quick access to various search functions. You can import these mappings into your own Vimium setup. This is a short overview of them:

```
gi: https://www.google.com/search?q=%s&tbm=isch
ya: https://yandex.ru/search/?text=%s
yh: https://search.yahoo.co.jp/search?p=%s
y:  https://www.youtube.com/results?search_query=%s
w: https://ja.wikipedia.org/wiki/%s
go: https://dictionary.goo.ne.jp/srch/all/%s/m1u
ji:  https://jisho.org/search/%s
```

With these shortcuts, you can quickly search Google Images (gi), Yandex (ya), Yahoo Japan (yh), YouTube (y), Japanese Wikipedia (w), Goo dictionary (go), and Jisho dictionary (ji).

### AutoHotkey
[AutoHotkey](https://www.autohotkey.com/) is a scripting language for automating tasks on Windows. The `autohotkey` folder contains the hotkey scripts I use around immersion: toggling the Japanese IME, sending URLs straight to MPV, quick dictionary lookups in qolibri, and opening a PowerShell window.

### Miscellaneous Tools
In addition to dictionaries, some other tools can enhance your Japanese learning experience. Here are some of them:
- [Textractor](https://github.com/Artikash/Textractor): A handy tool for extracting text from Visual Novels. This can help improve your reading comprehension skills
- [VPNGate](https://www.vpngate.net/en/download.aspx): A VPN service that allows you to unlock Japanese content, broadening your exposure to authentic language use
- [subs2cia](https://github.com/dxing97/subs2cia): Allows you to condense the audio from videos to increase passive immersion density
