/* NovoTech — Black Friday 2026 popup (the bar and the popup markup are in templates/partials/promo.html).
   When it opens by itself:
     desktop  after 9 s on the page, at 35% scroll, or when the pointer heads for the tab bar (exit intent)
     phones   from the 2nd page of the visit, or at 50% scroll — never on the page a visitor lands on (Google's
              mobile-interstitial rule), and as a small card at the bottom instead of a centred box
   Once closed it stays closed for 3 days (a "Black Friday" pill at bottom left reopens it); after "Get my quote"
   it never opens by itself again. Not on the contact, privacy and 404 pages. ?bfpreview shows it at any date. */
(function () {
  "use strict";
  var bar = document.getElementById("promo-bar");
  var tpl = document.getElementById("promo-tpl");
  if (!bar || !tpl || !("content" in tpl)) return;

  var START = Date.parse(bar.getAttribute("data-start"));
  var END = Date.parse(bar.getAttribute("data-end"));
  var preview = location.search.indexOf("bfpreview") > -1;
  if (!preview && (Date.now() < START || Date.now() > END)) { document.documentElement.classList.add("promo-off"); return; }

  var K = "nt-bf26-";
  function lget(k) { try { return localStorage.getItem(K + k); } catch (e) { return null; } }
  function lset(k, v) { try { localStorage.setItem(K + k, v); } catch (e) {} }
  function sget(k) { try { return sessionStorage.getItem(K + k); } catch (e) { return null; } }
  function sset(k, v) { try { sessionStorage.setItem(K + k, v); } catch (e) {} }

  var views = (parseInt(sget("pv"), 10) || 0) + 1;
  sset("pv", String(views));
  var phone = window.matchMedia("(max-width: 700px)").matches;
  var quoteUrl = bar.getAttribute("data-quote") || "#reques-a-quote";
  var dlg = null, teaser = null, timer = null, autoDone = false, lastFocus = null;

  function left() {
    var ms = Math.max(0, END - Date.now());
    var d = Math.floor(ms / 864e5), h = Math.floor(ms % 864e5 / 36e5), m = Math.floor(ms % 36e5 / 6e4);
    if (d >= 1) return d + (d === 1 ? " day " : " days ") + h + " h";
    return h + " h " + m + " min";
  }
  function tick() {
    if (!dlg) return;
    var t = left();
    dlg.querySelectorAll("[data-promo-count]").forEach(function (el) { el.textContent = t; });
  }

  function prefill() {
    var m = document.getElementById("q-message");
    if (m && !m.value) m.value = "Black Friday 2026 offer — I'm interested in: ";
  }
  if (sget("prefill")) prefill();

  function build() {
    dlg = tpl.content.firstElementChild.cloneNode(true);
    document.body.appendChild(dlg);
    var go = dlg.querySelector("[data-promo-quote]");
    go.setAttribute("href", quoteUrl);
    go.addEventListener("click", function () {
      lset("quote", "1"); sset("prefill", "1");
      close();
      if (quoteUrl.charAt(0) === "#") setTimeout(prefill, 50);
    });
    dlg.querySelector("[data-promo-close]").addEventListener("click", close);
    dlg.addEventListener("click", function (e) { if (e.target === dlg) close(); });   // backdrop (desktop)
    dlg.addEventListener("keydown", function (e) { if (e.key === "Escape" && !dlg.hasAttribute("aria-modal")) close(); });
    dlg.addEventListener("close", function () {
      clearInterval(timer);
      lset("closed", String(Date.now()));
      showTeaser();
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    });
  }

  function open() {
    if (!dlg) build();
    if (dlg.open) return;
    lastFocus = document.activeElement;
    tick(); timer = setInterval(tick, 30000);
    if (teaser) teaser.hidden = true;
    if (phone || typeof dlg.showModal !== "function") {
      dlg.classList.add("is-sheet");
      dlg.show();
      dlg.querySelector("[data-promo-close]").focus();
    } else {
      dlg.setAttribute("aria-modal", "true");
      dlg.showModal();
    }
  }
  function close() { if (dlg && dlg.open) dlg.close(); }

  function showTeaser() {
    if (!teaser) {
      teaser = document.createElement("button");
      teaser.type = "button";
      teaser.className = "promo-teaser";
      teaser.setAttribute("aria-haspopup", "dialog");
      teaser.innerHTML = "<b>Sale</b>Black Friday deals";
      teaser.addEventListener("click", open);
      document.body.appendChild(teaser);
    }
    teaser.hidden = false;
  }

  document.querySelectorAll("[data-promo-open]").forEach(function (b) { b.addEventListener("click", open); });

  /* automatic opening */
  var path = location.pathname;
  var quietPage = /contact-us|privacy-policy|page-not-found|404/.test(path);
  var closedAt = parseInt(lget("closed"), 10) || 0;
  var recentlyClosed = Date.now() - closedAt < 3 * 864e5;
  if (closedAt && !quietPage) showTeaser();
  if (!preview && (quietPage || lget("quote") || recentlyClosed)) return;

  function busy() {   // never interrupt someone typing in the quote form or using the AI machine finder
    var a = document.activeElement;
    var ai = document.getElementById("ai-panel");
    return (a && a.closest && a.closest("form, input, textarea, select")) || (ai && !ai.hidden);
  }
  function auto() {
    if (autoDone) return;
    if (busy()) { setTimeout(auto, 8000); return; }
    autoDone = true;
    open();
  }
  function atScroll(frac) {
    function on() {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      if (h > 0 && window.scrollY / h >= frac) { window.removeEventListener("scroll", on); auto(); }
    }
    window.addEventListener("scroll", on, { passive: true });
  }

  if (phone) {
    if (views >= 2) setTimeout(auto, 3500);
    else atScroll(0.5);
  } else {
    setTimeout(auto, 9000);
    atScroll(0.35);
    document.addEventListener("mouseout", function (e) {
      if (!e.relatedTarget && e.clientY <= 8) auto();
    });
  }
})();
