/* NovoTech — Black Friday sale page (templates/black-friday.html): the countdown, the "Get instant QUOTE" buttons on the
   machine cards (they tick that machine in the form) and the instant-quote form, sent to bf-quote.php. The server checks
   the buyer and e-mails the price list; its answer is shown under the button. */
(function () {
  "use strict";
  var d = document;

  /* countdown to the end of the sale: days, hours, minutes and seconds, ticking every second (the owner, Nov 14 2026) */
  var cnt = d.querySelector("[data-bf-end]");
  if (cnt) {
    var END = Date.parse(cnt.getAttribute("data-bf-end")), timer = 0;
    var pad = function (n) { return (n < 10 ? "0" : "") + n; };
    var set = function (sel, v) { var el = cnt.querySelector(sel); if (el && el.textContent !== v) el.textContent = v; };
    var tick = function () {
      var ms = END - Date.now();
      if (!(ms > 0)) {
        clearInterval(timer);
        cnt.innerHTML = '<p class="bf-count-label">The Black Friday sale has ended.</p>';
        return false;
      }
      set("[data-cd-d]", pad(Math.floor(ms / 864e5))); set("[data-cd-h]", pad(Math.floor(ms % 864e5 / 36e5)));
      set("[data-cd-m]", pad(Math.floor(ms % 36e5 / 6e4))); set("[data-cd-s]", pad(Math.floor(ms % 6e4 / 1e3)));
      return true;
    };
    var start = function () { clearInterval(timer); if (tick()) timer = setInterval(tick, 1000); };
    d.addEventListener("visibilitychange", function () { if (d.hidden) clearInterval(timer); else start(); });
    start();
  }

  /* the category chips: the one whose machines are on screen is marked */
  var chips = d.querySelectorAll(".bf-cats a");
  if (chips.length && "IntersectionObserver" in window) {
    var mark = function (id) { chips.forEach(function (a) { a.classList.toggle("is-current", a.getAttribute("href") === "#" + id); }); };
    var cio = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) mark(e.target.id); });
    }, { rootMargin: "-45% 0px -50% 0px" });
    d.querySelectorAll(".bf-cat").forEach(function (s) { cio.observe(s); });
  }

  var form = d.querySelector(".bf-form");
  if (!form) return;

  /* a card's button chooses its machine in the form's drop-down */
  d.querySelectorAll("[data-bf-pick]").forEach(function (a) {
    a.addEventListener("click", function () {
      var sel = form.querySelector("select[name='machines[]']"), id = a.getAttribute("data-bf-pick");
      if (sel && sel.querySelector("option[value='" + id + "']")) sel.value = id;
      setTimeout(function () { var n = form.querySelector("#bf-name"); if (n && !n.value) n.focus({ preventScroll: true }); }, 450);
    });
  });

  /* a link that names a machine (?m=bt26, from the Mailchimp campaign: the owner, Nov 14 2026) chooses it in the form */
  try {
    var want = new URLSearchParams(location.search).get("m"), msel = form.querySelector("select[name='machines[]']");
    if (want && msel && /^[a-z0-9-]{1,60}$/.test(want) && msel.querySelector("option[value='" + want + "']")) msel.value = want;
  } catch (e) {}

  var ts = form.querySelector("input[name=ts]");
  if (ts) ts.value = String(Math.floor(Date.now() / 1000));
  var status = form.querySelector(".form-status");
  var esc = function (t) { return String(t).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var say = function (cls, msg, html) { status.className = "form-status" + (cls ? " " + cls : ""); if (html) status.innerHTML = msg; else status.textContent = msg; };
  var CALL = "call <a href=\"tel:+16475265510\">+1 647 526 5510</a>";

  /* Google reCAPTCHA v3, as on the quote form: loaded when the form comes near, a fresh token at the moment of sending */
  var capKey = form.dataset.recaptcha || "", capLoading = false;
  var loadCaptcha = function () {
    if (!capKey || capLoading || form.dataset.staging) return;
    capLoading = true;
    var sc = d.createElement("script");
    sc.src = "https://www.google.com/recaptcha/api.js?render=" + encodeURIComponent(capKey);
    sc.async = true; sc.defer = true;
    d.head.appendChild(sc);
  };
  var withToken = function (done) {
    if (!capKey) { done(); return; }
    loadCaptcha();
    var tries = 0;
    (function wait() {
      if (window.grecaptcha && window.grecaptcha.execute) {
        window.grecaptcha.ready(function () {
          window.grecaptcha.execute(capKey, { action: "bf_quote" }).then(function (tok) {
            var h = form.querySelector("input[name='g-recaptcha-response']"); if (h) h.value = tok; done();
          }, function () { done(); });
        });
      } else if (++tries < 50) { setTimeout(wait, 100); }
      else { done(); }
    })();
  };
  if (capKey) {
    form.addEventListener("focusin", loadCaptcha);
    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (es) { if (es.some(function (e) { return e.isIntersecting; })) { loadCaptcha(); io.disconnect(); } }, { rootMargin: "600px 0px" });
      io.observe(form);
    }
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var bad = [];
    form.querySelectorAll("[required]").forEach(function (el) {
      var wrong = el.type === "checkbox" ? !el.checked
        : (!el.value.trim() || (el.type === "email" && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(el.value.trim())));
      el.setAttribute("aria-invalid", wrong ? "true" : "false");
      if (wrong) bad.push(el);
    });
    if (bad.length) {
      say("is-error", "Please fill in your name, email and phone number.");
      bad[0].focus();
      return;
    }
    if (form.dataset.staging) {
      say("", "This is the test site and it cannot send email. On NovoTechMachineTools.com the price list is emailed automatically.");
      return;
    }
    var btn = form.querySelector("button[type=submit]");
    btn.disabled = true; say("", "Sending…");
    withToken(function () {
      fetch(form.action, { method: "POST", body: new FormData(form), headers: { "Accept": "application/json" } })
        .then(function (r) { return r.json().catch(function () { return { ok: false }; }); })
        .then(function (j) {
          if (j && j.ok) {
            say("is-ok", esc(j.message || "Thank you — your request is on its way."), true);
            form.reset();
            if (ts) ts.value = String(Math.floor(Date.now() / 1000));
          } else {
            say("is-error", (j && j.error ? esc(j.error) + " " : "We could not send the form from this page. ") +
              "You can also " + CALL + " or email <a href=\"mailto:info@NovoTechMachineTools.com\">info@NovoTechMachineTools.com</a>.", true);
          }
        })
        .catch(function () {
          say("is-error", "We could not send the form from this page. Please " + CALL + " or email <a href=\"mailto:info@NovoTechMachineTools.com\">info@NovoTechMachineTools.com</a>.", true);
        })
        .then(function () { btn.disabled = false; });
    });
  });
})();
