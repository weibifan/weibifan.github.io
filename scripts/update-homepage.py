#!/usr/bin/env python3
"""Update homepage: add research interests tag cloud + BibTeX links"""
import re

HOME = "d:/MyCodeSpace/MyGithub/homepage_repo"
with open(f"{HOME}/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# === 1. Research Interests Tag Cloud ===

tag_cloud = """
          <!-- ========== Research Interests ========== -->
          <h1 style="margin-top:1.5em;"><i class="fas fa-tags" style="margin-right:8px;"></i> <span class="lang-zh">研究方向</span><span class="lang-en">Research Interests</span></h1>
          <div class="tag-cloud">
            <a href="https://scholar.google.com/citations?user=G0DQL4YAAAAJ&hl=en#" target="_blank" class="tag-cloud-item" style="font-size:1.2em;">Knowledge Graph</a>
            <a href="https://scholar.google.com/scholar?q=smart+education+knowledge+engineering" target="_blank" class="tag-cloud-item" style="font-size:1.1em;">Smart Education</a>
            <a href="https://scholar.google.com/scholar?q=question+generation+NLP" target="_blank" class="tag-cloud-item" style="font-size:1.1em;">Question Generation</a>
            <a href="https://scholar.google.com/scholar?q=multimodal+reasoning+diagram" target="_blank" class="tag-cloud-item" style="font-size:1.05em;">Multimodal Reasoning</a>
            <a href="https://scholar.google.com/scholar?q=geometry+problem+solving+neural+symbolic" target="_blank" class="tag-cloud-item" style="font-size:0.95em;">Geometry Solving</a>
            <a href="https://scholar.google.com/scholar?q=text+segmentation+facet+mining" target="_blank" class="tag-cloud-item" style="font-size:0.95em;">Text Segmentation</a>
            <a href="https://scholar.google.com/scholar?q=knowledge+graph+ontology+engineering" target="_blank" class="tag-cloud-item" style="font-size:1.1em;">Knowledge Engineering</a>
            <a href="https://scholar.google.com/scholar?q=conversational+QA+question+answering" target="_blank" class="tag-cloud-item" style="font-size:0.95em;">Question Answering</a>
            <a href="https://scholar.google.com/scholar?q=RDF+conflict+resolution+data+integration" target="_blank" class="tag-cloud-item" style="font-size:0.85em;">Data Integration</a>
            <a href="https://scholar.google.com/scholar?q=intelligent+tutoring+system+AI+education" target="_blank" class="tag-cloud-item" style="font-size:1.0em;">Intelligent Tutoring</a>
            <a href="https://scholar.google.com/scholar?q=spiking+neural+P+system+membrane+computing" target="_blank" class="tag-cloud-item" style="font-size:0.85em;">Membrane Computing</a>
          </div>
"""

# Insert after the English about-me section, before News
marker = 'He has published <strong>40+ papers</strong> in leading venues'
replacement_marker = 'He has published <strong>40+ papers</strong> in leading venues'
# Find the end of the div that wraps the about section and the start of news
old = '          </div>\n\n          <!-- ========== News ========== -->'
new = '          </div>' + tag_cloud + '\n          <!-- ========== News ========== -->'

# Use the second occurrence (the English section's closing div)
parts = content.split(old)
if len(parts) >= 2:
    # First occurrence is the Chinese section's closing, second is English's
    content = old.join(parts[:2]) + tag_cloud + '\n          <!-- ========== News ========== -->' + old.join(parts[2:])
    print("1. Tag cloud inserted OK")
else:
    print("1. ERROR: could not split")

# === 2. CSS for tag cloud and BibTeX ===

css_additions = """
    /* --- Research tag cloud --- */
    .tag-cloud { display: flex; flex-wrap: wrap; gap: 8px; margin: 0.8em 0 1.2em; }
    .tag-cloud-item {
        display: inline-block; padding: 4px 14px; border-radius: 20px;
        background: #f0f4fa; color: #224b8d; text-decoration: none;
        transition: all 0.2s; border: 1px solid #dde6f0;
    }
    .tag-cloud-item:hover { background: #224b8d; color: #fff; transform: scale(1.05); }

    /* --- BibTeX link --- */
    .bib-link { color: #6b6b6b; font-size: 0.85em; text-decoration: none; }
    .bib-link:hover { color: #224b8d; text-decoration: underline; }
    .bib-dl { color: #224b8d; font-size: 0.85em; text-decoration: none; }
    .bib-dl:hover { text-decoration: underline; }

    /* --- Copy toast --- */
    .bib-toast {
        position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%);
        background: #224b8d; color: #fff; padding: 8px 20px; border-radius: 20px;
        font-size: 0.85em; z-index: 999; opacity: 0; transition: opacity 0.3s;
        pointer-events: none;
    }
    .bib-toast.show { opacity: 1; }
"""

# Insert CSS before the responsive section
content = content.replace(
    "    /* --- Responsive --- */",
    css_additions + "\n    /* --- Responsive --- */"
)
print("2. CSS added OK")

# === 3. BibTeX links + download all ===

# Update publications header
old_hdr = '<span class="lang-zh">40+ 篇论文 · 含 PDF 链接</span>\n            <span class="lang-en">40+ papers · PDF links available</span>'
new_hdr = '<span class="lang-zh">40+ 篇论文 · 含 PDF / BibTeX 链接</span>\n            <span class="lang-en">40+ papers · PDF &amp; BibTeX available</span>\n            <span style="margin-left:12px;"><a href="papers/publications.bib" target="_blank" class="bib-dl"><i class="fa fa-download"></i> <span class="lang-zh">全部 BibTeX</span><span class="lang-en">All BibTeX</span></a></span>'
if old_hdr in content:
    content = content.replace(old_hdr, new_hdr)
    print("3a. All BibTeX link added OK")
else:
    print("3a. ERROR: could not find pub header")

# Add [BibTeX] link after each [PDF] link
bib_replacements = [
    ('2026_WTASNP_IC.pdf" target="_blank">[PDF]</a>', '2026_WTASNP_IC.pdf" target="_blank">[PDF]</a> <a href="#" onclick="return copyBib(\'bao2026wnp\')" class="bib-link">[BibTeX]</a>'),
    ('2026_NS-GPS_PR.pdf" target="_blank">[PDF]</a>', '2026_NS-GPS_PR.pdf" target="_blank">[PDF]</a> <a href="#" onclick="return copyBib(\'wang2026nsgps\')" class="bib-link">[BibTeX]</a>'),
    ('2026_GeoTree_TMM.pdf" target="_blank">[PDF]</a>', '2026_GeoTree_TMM.pdf" target="_blank">[PDF]</a> <a href="#" onclick="return copyBib(\'wang2026geotree\')" class="bib-link">[BibTeX]</a>'),
    ('2025_GlFoMR_SIGIR.pdf" target="_blank">[PDF]</a>', '2025_GlFoMR_SIGIR.pdf" target="_blank">[PDF]</a> <a href="#" onclick="return copyBib(\'wang2025glfomr\')" class="bib-link">[BibTeX]</a>'),
]
for old_str, new_str in bib_replacements:
    content = content.replace(old_str, new_str)

# Papers that also have [arXiv] link - handle differently
content = content.replace(
    '2024_QGEval_EMNLP.pdf" target="_blank">[PDF]</a> <a href="https://arxiv.org/abs/2406.05707" target="_blank">[arXiv]</a>',
    '2024_QGEval_EMNLP.pdf" target="_blank">[PDF]</a> <a href="https://arxiv.org/abs/2406.05707" target="_blank">[arXiv]</a> <a href="#" onclick="return copyBib(\'fu2024qgeval\')" class="bib-link">[BibTeX]</a>'
)

# Remaining papers
remaining = [
    ('2024_RTRL_KBS.pdf" target="_blank">[PDF]</a>', 'zeng2024rtrl'),
    ('2023_SPARTA_ACL.pdf" target="_blank">[PDF]</a>', 'zeng2023sparta'),
    ('2023_DisAVR_TIP.pdf" target="_blank">[PDF]</a>', 'wang2023disavr'),
    ('2023_SSCGN_TCSVT.pdf" target="_blank">[PDF]</a>', 'wang2023sscgn'),
    ('2021_FTS_TNNLS.pdf" target="_blank">[PDF]</a>', 'wu2021fts'),
    ('2020_KPO_BigData.pdf" target="_blank">[PDF]</a>', 'ma2020kpo'),
    ('2018_FACM_NeuralComput.pdf" target="_blank">[PDF]</a>', 'wu2018facet'),
]
for pdf_marker, bib_key in remaining:
    old_str = f'{pdf_marker}'
    new_str = f'{pdf_marker} <a href="#" onclick="return copyBib(\'{bib_key}\')" class="bib-link">[BibTeX]</a>'
    if old_str in content:
        content = content.replace(old_str, new_str)

print("3b. BibTeX links added OK")

# === 4. Add copyBib JS function ===

js_bib = '''
    // BibTeX copy-to-clipboard
    var BIB_DATA = null;
    function loadBibData() {
        if (BIB_DATA) return Promise.resolve(BIB_DATA);
        return fetch("papers/publications.bib").then(function(r) { return r.text(); }).then(function(t) {
            // Parse into a map of key -> entry text
            var map = {};
            var entries = t.split(/@\w+\{/);
            for (var i = 1; i < entries.length; i++) {
                var keyEnd = entries[i].indexOf(",");
                if (keyEnd < 0) continue;
                var key = entries[i].substring(0, keyEnd).trim();
                map[key] = "@" + entries[i].split("@")[0]; // re-add the split-off prefix
                // Also trim braces
                if (map[key].endsWith("}")) map[key] = map[key].substring(0, map[key].length - 1) + "}";
            }
            BIB_DATA = map;
            return map;
        });
    }
    function copyBib(key) {
        loadBibData().then(function(map) {
            var text = map[key];
            if (!text) { alert("BibTeX not found: " + key); return; }
            navigator.clipboard.writeText(text).then(function() {
                showBibToast("Copied: " + key);
            });
        });
        return false;
    }
    function showBibToast(msg) {
        var el = document.getElementById("bib-toast");
        if (!el) {
            el = document.createElement("div");
            el.id = "bib-toast";
            el.className = "bib-toast";
            document.body.appendChild(el);
        }
        el.textContent = msg;
        el.classList.add("show");
        setTimeout(function() { el.classList.remove("show"); }, 2000);
    }
'''

# Insert before the closing </body>
content = content.replace("</body>", js_bib + "\n</body>")
print("4. JS added OK")

with open(f"{HOME}/index.html", "w", encoding="utf-8") as f:
    f.write(content)
print("5. File saved OK!")
