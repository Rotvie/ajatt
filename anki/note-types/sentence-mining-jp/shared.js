(function () {
    function byId(id) { return document.getElementById(id); }
    function txt(id) { var e = byId(id); return e ? e.textContent.trim() : ""; }

    /* --- pitch accent colouring --------------------------------------- */
    function moraCount(kana) { return kana.replace(/[ャュョゃゅょ]/g, "").length; }

    function pitchColour(n, kana) {
        if (n === 0) { return "#3366CC"; }                 /* 平板 heiban  */
        if (n === 1) { return "red"; }                     /* 頭高 atamadaka */
        return moraCount(kana) === n ? "green"             /* 尾高 odaka   */
                                     : "#ff6207";          /* 中高 nakadaka */
    }

    function markPitch() {
        var m = txt("src-pitchnum").match(/\d+/);
        if (!m) { return; }
        var colour = pitchColour(Number(m[0]), txt("src-kana"));
        var words = document.querySelectorAll(".jpsentence b, .jpsentence strong");
        for (var i = 0; i < words.length; i++) { words[i].style.color = colour; }
    }

    /* --- tags --------------------------------------------------------- */
    function buildTags() {
        var bars = document.querySelectorAll("header.tagbar");
        for (var b = 0; b < bars.length; b++) {
            var bar = bars[b];
            var tags = bar.textContent.trim().split(/\s+/);
            bar.textContent = "";
            for (var i = 0; i < tags.length; i++) {
                if (!tags[i]) { continue; }
                var d = document.createElement("div");
                d.className = "tag";
                d.textContent = tags[i];
                bar.appendChild(d);
            }
        }
    }

    /* --- dictionary links --------------------------------------------
       All word-keyed: the sentence is already on the card, and sentence
       searches returned noise. Built in JS so the query is percent-encoded
       (Anki has no urlencode filter).                                     */
    function buildLinks() {
        var foot = byId("lookup");
        if (!foot) { return; }
        var word = txt("src-word");
        if (!word) { return; }
        var w = encodeURIComponent(word);
        var links = [
            ["Kotobank", "https://kotobank.jp/word/" + w],
            ["Massif", "https://massif.la/ja/search?q=" + w],
            ["ImmersionKit", "https://www.immersionkit.com/dictionary?keyword=" + w],
            ["jpdb", "https://jpdb.io/search?q=" + w + "&lang=japanese#a"],
            ["YouGlish", "https://youglish.com/pronounce/" + w + "/japanese"]
        ];
        foot.textContent = "";
        for (var i = 0; i < links.length; i++) {
            var a = document.createElement("a");
            a.href = links[i][1];
            a.textContent = links[i][0];
            a.rel = "noopener";
            foot.appendChild(a);
        }
    }

    /* --- production front: replace the target word with its kana shape - */
    function maskProduction() {
        var hidden = document.querySelectorAll(".production b, .production strong");
        for (var i = 0; i < hidden.length; i++) {
            var kana = hidden[i].innerText.replace(/[^ぁ-んァ-ン]/g, "");
            hidden[i].style.visibility = "visible";
            hidden[i].innerText = "【" + kana + "】";
        }
    }

    /* pitch number is stored as e.g. "[3]" on some notes */
    function tidyPitchChip() {
        var chip = byId("pitch-chip");
        if (chip) { chip.textContent = chip.textContent.replace(/[\[\]]/g, ""); }
    }

    window.smjRender = function () {
        buildTags();
        tidyPitchChip();
        markPitch();
        buildLinks();
        maskProduction();
    };
    window.smjRender();
})();
