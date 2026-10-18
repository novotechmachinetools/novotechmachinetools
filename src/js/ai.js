/* NovoTech machine finder — loaded on demand when the "Find a machine" panel opens.
   1. Instant keyword search over ai/catalogue.json (works everywhere, no server needed).
   2. Conversational answers from ask.php (Anthropic API on the server) with product cards. */
(function () {
  "use strict";
  var d = document;
  var panel = d.getElementById("ai-panel");
  if (!panel || panel.dataset.ready) return;
  panel.dataset.ready = "1";
  var log = d.getElementById("ai-log");
  var form = d.getElementById("ai-form");
  var input = d.getElementById("ai-q");
  var suggest = d.getElementById("ai-suggest");
  var STAGING = !!panel.dataset.staging;
  var history = [];
  var catalogue = null;

  function el(tag, cls, html) { var e = d.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function scroll() { log.scrollTop = log.scrollHeight; }

  function loadCatalogue() {
    if (catalogue) return Promise.resolve(catalogue);
    return fetch("ai/catalogue.json").then(function (r) { return r.json(); }).then(function (j) { catalogue = j.families || []; return catalogue; });
  }

  /* ---------- instant search: tokens in names / models / summary, numbers matched against capacities ---------- */
  var INCH = /(\d+(?:[.,]\d+)?)\s*(?:"|″|''|in\b|inch(?:es)?)/i, MM = /(\d+(?:[.,]\d+)?)\s*mm\b/i;
  function capInches(m) {
    var t = (m.round_capacity || m.max_single_bar || m.cutting_capacity || "");
    var x = /Ø?\s*(\d+)(?:-(\d+)\/(\d+))?″/.exec(t);
    if (!x) return null;
    return parseInt(x[1], 10) + (x[2] ? parseInt(x[2], 10) / parseInt(x[3], 10) : 0);
  }
  function localSearch(q) {
    var words = q.toLowerCase().replace(/[^\w\s"″.\/-]/g, " ").split(/\s+/).filter(function (w) { return w.length > 1; });
    var need = null, mi = INCH.exec(q), mmm = MM.exec(q);
    if (mi) need = parseFloat(mi[1].replace(",", ".")); else if (mmm) need = parseFloat(mmm[1].replace(",", ".")) / 25.4;
    var wantAuto = /\bauto|automatic|cnc|nc\b|unattended/i.test(q), wantManual = /\bmanual|gravity|budget|cheap|value|small shop|maintenance/i.test(q);
    var wantMiter = /mit(e|re)|angle|45|60|degree|°/i.test(q), wantDC = /double[- ]column|twin[- ]column|dual[- ]column|heavy|solid|billet|block/i.test(q);
    var wantRebar = /rebar|stirrup|bar bend|cutter|cut rebar|\d+m\b|#\d/i.test(q);
    var scored = catalogue.map(function (f) {
      var hay = (f.name + " " + f.models_label + " " + f.category + " " + f.summary + " " + f.features.join(" ")).toLowerCase();
      var s = 0;
      words.forEach(function (w) { if (hay.indexOf(w) >= 0) s += w.length > 3 ? 2 : 1; });
      f.models.forEach(function (m) { if (q.toLowerCase().indexOf(m.name.toLowerCase()) >= 0) s += 12; });
      var isBandsaw = /band saw|bandsaw/i.test(f.category + " " + f.page_title);
      if (wantRebar && !isBandsaw) s += 3; if (wantRebar && isBandsaw) s -= 3;
      if (!wantRebar && isBandsaw) s += 1;
      if (wantAuto && f.automation === "automatic") s += 4;
      if (wantManual && f.automation === "manual") s += 4;
      if (wantDC && f.automation === "double-column") s += 4;
      if (wantMiter && /mit(e|re)|swivel|angle/i.test(hay)) s += 2;
      var fit = null;
      if (need) {
        f.models.forEach(function (m) { var c = capInches(m); if (c != null && c >= need && (fit == null || c < fit)) fit = c; });
        if (fit != null) s += 6 - Math.min(4, (fit - need) / 2); else s -= 6;
      }
      return { f: f, s: s, fit: fit };
    }).filter(function (x) { return x.s > 0; });
    scored.sort(function (a, b) { return b.s - a.s; });
    return scored.slice(0, 4);
  }

  /* ---------- rendering ---------- */
  function bubble(role, html) { var b = el("div", "ai-msg ai-" + role, html); log.appendChild(b); scroll(); return b; }
  function cards(results) {
    var wrap = el("div", "ai-cards");
    results.forEach(function (r) {
      var f = typeof r.id === "string" ? catalogue.filter(function (x) { return x.id === r.id; })[0] : r.f;
      if (!f) return;
      var model = r.model && f.models.some(function (m) { return m.name === r.model; }) ? f.models.filter(function (m) { return m.name === r.model; })[0] : null;
      var cap = model ? (model.round_capacity || model.max_single_bar || model.cutting_capacity || "") : (f.headline || "");
      var a = el("a", "ai-card");
      a.href = f.href;
      a.innerHTML = (f.image ? '<img src="' + esc(f.image) + '" alt="" loading="lazy" width="96" height="72">' : "") +
        '<span class="ai-card-body"><span class="ai-card-line">' + esc((f.brand || "") + (f.line ? " · " + f.line : "")) + "</span>" +
        "<strong>" + esc(model ? model.name : f.name) + "</strong>" +
        (model ? '<span class="ai-card-fam">' + esc(f.name) + "</span>" : "") +
        (cap ? '<span class="ai-card-cap">' + esc(cap) + "</span>" : "") +
        '<span class="ai-card-go">Specifications and photos →</span></span>';
      wrap.appendChild(a);
    });
    if (wrap.children.length) { log.appendChild(wrap); scroll(); }
  }
  function md(t) {
    // minimal markdown: paragraphs, bullets, bold
    var lines = esc(t).split(/\n/), out = "", inList = false;
    lines.forEach(function (ln) {
      var m = /^\s*(?:[-*•]|\d+[.)])\s+(.*)$/.exec(ln);
      if (m) { if (!inList) { out += "<ul>"; inList = true; } out += "<li>" + m[1] + "</li>"; return; }
      if (inList) { out += "</ul>"; inList = false; }
      if (ln.trim()) out += "<p>" + ln + "</p>";
    });
    if (inList) out += "</ul>";
    return out.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
  }

  /* ---------- ask ---------- */
  var busy = false;
  function ask(q) {
    if (busy || !q.trim()) return;
    busy = true; form.querySelector("button").disabled = true;
    suggest.hidden = true;
    bubble("user", esc(q));
    history.push({ role: "user", content: q });
    var thinking = bubble("assistant ai-thinking", "Looking through the catalogue…");
    loadCatalogue().then(function () {
      var local = localSearch(q);
      if (STAGING) {
        thinking.innerHTML = md(local.length ? "Here is what matches on this site (the conversational assistant runs on the live NovoTechMachineTools.com server, not on this test copy):" : "Nothing on this site matches that description — on the live site the assistant can discuss alternatives, or call +1 647 526 5510.");
        cards(local);
        return;
      }
      return fetch("ask.php", { method: "POST", headers: { "Content-Type": "application/json", "Accept": "application/json" }, body: JSON.stringify({ messages: history, page: panel.dataset.page }) })
        .then(function (r) { return r.json().catch(function () { return { error: "bad_json" }; }); })
        .then(function (j) {
          if (j.error === "not_configured" || j.error === "bad_json" || (j.error && !j.answer)) {
            thinking.innerHTML = md(local.length ? "Here is what matches your description in our catalogue:" : (j.message || "The assistant is not available right now — please call +1 647 526 5510 or email us."));
            cards(local);
            return;
          }
          thinking.className = "ai-msg ai-assistant";
          thinking.innerHTML = md(j.answer || "");
          history.push({ role: "assistant", content: j.answer || "" });
          cards((j.results && j.results.length) ? j.results : local.slice(0, 2));
        });
    }).catch(function () {
      thinking.innerHTML = "The assistant could not be reached. Please call +1 647 526 5510 or email info@NovoTechMachineTools.com.";
    }).then(function () { busy = false; form.querySelector("button").disabled = false; input.focus(); });
  }

  form.addEventListener("submit", function (e) { e.preventDefault(); var q = input.value; input.value = ""; ask(q); });
  input.addEventListener("keydown", function (e) { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); form.requestSubmit ? form.requestSubmit() : form.dispatchEvent(new Event("submit")); } });
  suggest.addEventListener("click", function (e) { var b = e.target.closest("button"); if (b) ask(b.textContent); });
  loadCatalogue();
  input.focus();
})();
