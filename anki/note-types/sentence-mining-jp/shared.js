(function () {
    function byId(id) { return document.getElementById(id); }
    function txt(id) { var e = byId(id); return e ? e.textContent.trim() : ""; }

    /* --- pitch accent colouring --------------------------------------- */
    function moraCount(kana) { return kana.replace(/[ャュョゃゅょァィゥェォぁぃぅぇぉヮゎ]/g, "").length; }

    function pitchColour(n, kana) {
        if (n === 0) { return "#3366CC"; }                 /* 平板 heiban  */
        if (n === 1) { return "red"; }                     /* 頭高 atamadaka */
        return moraCount(kana) === n ? "green"             /* 尾高 odaka   */
                                     : "#ff6207";          /* 中高 nakadaka */
    }

    function markPitch() {
        var m = txt("src-pitchnum").replace(/[０-９]/g, function (c) {
            return String.fromCharCode(c.charCodeAt(0) - 0xFEE0);   /* full-width digits */
        }).match(/\d+/);
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
            /* a back that embeds the front runs this script twice; build once */
            if (bar.getAttribute("data-built")) { continue; }
            bar.setAttribute("data-built", "1");
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

    /* --- production front: hide the target word completely ------------ */
    function maskProduction() {
        var hidden = document.querySelectorAll(".production b, .production strong");
        for (var i = 0; i < hidden.length; i++) {
            hidden[i].style.visibility = "visible";
            hidden[i].textContent = "【＿＿＿】";
        }
    }

    /* --- production front: one short meaning as the cue ----------------
       Takes the sense bolded at mining time if there is one, else the first
       real definition line: headword, grammar-label and etymology lines are
       skipped, leading 〔〕［］（） annotations and sense numbers stripped,
       examples 「…」 dropped, first sentence kept. The target word and its
       reading are blanked so the hint never gives the answer away.        */
    function pickHint(html, hide) {
        function plain(s) {
            return s.replace(/<[^>]+>/g, "").replace(/&nbsp;/g, " ").replace(/&lt;/g, "<")
                    .replace(/&gt;/g, ">").replace(/&amp;/g, "&").replace(/\s+/g, " ")
                    .replace(/([^\x00-\x7f]) /g, "$1").replace(/ ([^\x00-\x7f])/g, "$1").trim();
        }
        var lead = /^(?:〔[^〕]*〕|［[^］]*］|（[^）]*）|\([^)]*\)|■[^■]*■|[①-⑳㋐-㋾]|スル|[０-９\d]+(?![０-９\d])[\s.．]?|△|▲|《[^》]*》|\[|[ぁ-ん]+・[ぁ-ん]+(?![ぁ-ん]))\s*/;
        var bold = null, re = /<(b|strong)>([\s\S]*?)<\/\1>/gi, m;
        while (!bold && (m = re.exec(html))) {          /* skip bolded sense numbers */
            if (plain(m[2]).length > 3) { bold = m[2]; }
        }
        var lines = (bold || html).split(/<br\s*\/?>|<\/?(?:div|li|ol|ul|p)[^>]*>/i);
        var pick = "";
        /* pass 0 skips lines starting with ― (examples); pass 1 allows them,
           for dictionaries that write the sense as "―する …"                */
        for (var pass = 0; pass < 2 && !pick; pass++) {
            for (var i = 0; i < lines.length && !pick; i++) {
                var l = plain(lines[i]);
                if (/【|\[\d|★|^→|[ぁ-んァ-ン][\-‐][ぁ-んァ-ン][^。]*$/.test(l)) { continue; } /* headword / reading / xref */
                var gloss = l.match(/^[―─]〔＝([^〕]+)〕/);   /* 新明解 example gloss */
                if (gloss) { pick = gloss[1]; continue; }
                if (pass === 0 && /^[―─]/.test(l)) { continue; }
                l = l.replace(/「[^」]*[―─][^」]*」/g, "").replace(/［[^］]*］/g, "")
                     .replace(/^(?:[―─][ぁ-ん]{0,2}／?)+/, "");
                var prev;
                do { prev = l; l = l.replace(lead, ""); } while (l !== prev);
                l = l.split(/。/)[0].replace(/[．\s]+$/, "");
                if (!l || (/^[ぁ-んァ-ンー・\-―\s]+$/.test(l) && /[・\-―\s]/.test(l))) { continue; } /* reading line */
                if (/^[ァ-ン]{1,2}$/.test(l)) { continue; }   /* leftover grammar label: ナリ, タリ */
                if (/^[（(［\[]/.test(l) || /^[^ぁ-ん]*[（［](?:動|形|副|名|感|接|連)/.test(l)) { continue; }
                if (hide.indexOf(l) >= 0) { continue; }      /* the bare headword */
                pick = l;
            }
        }
        for (var j = 0; j < hide.length; j++) {
            if (hide[j]) { pick = pick.split(hide[j]).join("＿＿"); }
        }
        return pick.length > 80 ? pick.slice(0, 80) + "…" : pick;
    }

    function buildHint() {
        var box = byId("hint"), src = byId("src-def");
        if (!box || !src || box.getAttribute("data-built")) { return; }
        box.setAttribute("data-built", "1");
        var h = pickHint(src.innerHTML, [txt("src-hide-word"), txt("src-hide-kana")]);
        if (h) { box.textContent = h; } else { box.style.display = "none"; }
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
        buildHint();
    };
    window.smjRender();
})();
