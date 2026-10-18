/* NovoTech site script — no dependencies. Progressive: the page works without it. */
(function () {
  "use strict";
  var d = document;
  var PREVIEW = !!d.querySelector(".preview-note"); // artifact preview: no embeds, no mail handler

  /* ---------- mobile navigation ---------- */
  var toggle = d.querySelector(".nav-toggle");
  var menu = d.getElementById("nav-menu");
  if (toggle && menu) {
    toggle.addEventListener("click", function () {
      var open = menu.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    menu.querySelectorAll(".sub-toggle").forEach(function (b) {
      b.addEventListener("click", function () {
        var li = b.closest("li");
        var open = li.classList.toggle("open");
        b.setAttribute("aria-expanded", open ? "true" : "false");
      });
    });
  }

  /* ---------- jump nav: highlight the section in view ---------- */
  var jumpLinks = Array.prototype.slice.call(d.querySelectorAll(".jump-list a[href^='#']"));
  if (jumpLinks.length && "IntersectionObserver" in window) {
    var byId = {};
    jumpLinks.forEach(function (a) { byId[a.getAttribute("href").slice(1)] = a; });
    var targets = Object.keys(byId).map(function (id) { return d.getElementById(id); }).filter(Boolean);
    var current = null;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          if (current) current.classList.remove("is-active");
          current = byId[e.target.id];
          if (current) {
            current.classList.add("is-active");
            // keep the active chip visible in the scrolling strip
            var list = current.parentNode.parentNode;
            var left = current.offsetLeft - list.clientWidth / 2 + current.offsetWidth / 2;
            if (typeof list.scrollTo === "function") list.scrollTo({ left: left, behavior: "smooth" }); else list.scrollLeft = left;
          }
        }
      });
    }, { rootMargin: "-140px 0px -60% 0px", threshold: 0 });
    targets.forEach(function (t) { io.observe(t); });
  }

  /* ---------- galleries: thumbnails swap the main image, lightbox on click ---------- */
  var lightbox = null, lbImg, lbCap, lbItems = [], lbIndex = 0;
  function ensureLightbox() {
    if (lightbox) return;
    lightbox = d.createElement("dialog");
    lightbox.className = "lightbox";
    lightbox.setAttribute("aria-label", "Photo viewer");
    lightbox.innerHTML = '<div class="lightbox-inner"><img alt=""><p class="lightbox-caption"></p>' +
      '<button type="button" class="lb-prev" aria-label="Previous photo">‹</button>' +
      '<button type="button" class="lb-next" aria-label="Next photo">›</button>' +
      '<button type="button" class="lb-close" aria-label="Close">×</button></div>';
    d.body.appendChild(lightbox);
    lbImg = lightbox.querySelector("img");
    lbCap = lightbox.querySelector(".lightbox-caption");
    lightbox.querySelector(".lb-prev").addEventListener("click", function () { showLb(lbIndex - 1); });
    lightbox.querySelector(".lb-next").addEventListener("click", function () { showLb(lbIndex + 1); });
    lightbox.querySelector(".lb-close").addEventListener("click", function () { lightbox.close(); });
    lightbox.addEventListener("click", function (e) { if (e.target === lightbox) lightbox.close(); });
    lightbox.addEventListener("keydown", function (e) {
      if (e.key === "ArrowLeft") showLb(lbIndex - 1);
      if (e.key === "ArrowRight") showLb(lbIndex + 1);
    });
    onSwipe(lightbox.querySelector(".lightbox-inner"), function (dir) { showLb(lbIndex + dir); });
  }
  function showLb(i) {
    if (!lbItems.length) return;
    lbIndex = (i + lbItems.length) % lbItems.length;
    var it = lbItems[lbIndex];
    lbImg.src = it.src; lbImg.srcset = it.srcset || ""; lbImg.sizes = "92vw"; lbImg.alt = it.alt; lbCap.textContent = it.alt;
  }
  /* Horizontal swipe / drag detection shared by galleries and the lightbox */
  function onSwipe(el, cb) {
    var x0 = null, y0 = null, id = null;
    el.addEventListener("pointerdown", function (e) { if (e.button !== undefined && e.button !== 0) return; x0 = e.clientX; y0 = e.clientY; id = e.pointerId; });
    el.addEventListener("pointerup", function (e) {
      if (x0 === null || e.pointerId !== id) return;
      var dx = e.clientX - x0, dy = e.clientY - y0; x0 = null;
      if (Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy) * 1.5) { el._swiped = true; cb(dx < 0 ? 1 : -1); setTimeout(function () { el._swiped = false; }, 250); }
    });
    el.addEventListener("pointercancel", function () { x0 = null; });
    el.addEventListener("dragstart", function (e) { e.preventDefault(); }); // links/images would otherwise start a native drag
    el.style.touchAction = "pan-y";
  }

  d.querySelectorAll(".gallery").forEach(function (g) {
    var main = g.querySelector(".gallery-main img");
    var link = g.querySelector(".gallery-main .gallery-link");
    var figure = g.querySelector(".gallery-main");
    var cap = g.querySelector(".gallery-main figcaption");
    var counter = g.querySelector(".gal-index");
    var thumbs = Array.prototype.slice.call(g.querySelectorAll(".thumb"));
    var items = thumbs.length ? thumbs.map(function (t) {
      return { src: t.dataset.src, srcset: t.dataset.srcset, w: t.dataset.w, h: t.dataset.h, alt: t.dataset.alt, cutout: t.classList.contains("is-cutout") };
    }) : [{ src: main.currentSrc || main.src, srcset: main.srcset, w: main.width, h: main.height, alt: main.alt, cutout: figure.classList.contains("is-cutout") }];
    var index = 0;
    function show(i) {
      index = (i + items.length) % items.length;
      var it = items[index];
      main.src = it.src; main.srcset = it.srcset || ""; main.width = it.w; main.height = it.h; main.alt = it.alt;
      link.href = it.src; link.dataset.index = index;
      cap.textContent = it.alt;
      if (counter) counter.textContent = index + 1;
      figure.classList.toggle("is-cutout", !!it.cutout);
      thumbs.forEach(function (t, j) { t.classList.toggle("is-current", j === index); });
      var cur = thumbs[index];
      if (cur && cur.scrollIntoView) cur.scrollIntoView({ block: "nearest", inline: "nearest" });
    }
    thumbs.forEach(function (t, i) {
      t.addEventListener("click", function (e) { e.preventDefault(); show(i); });
    });
    var prev = g.querySelector(".gal-prev"), next = g.querySelector(".gal-next");
    if (prev) prev.addEventListener("click", function () { show(index - 1); });
    if (next) next.addEventListener("click", function () { show(index + 1); });
    if (items.length > 1) {
      onSwipe(figure, function (dir) { show(index + dir); });
      figure.setAttribute("tabindex", "0");
      figure.addEventListener("keydown", function (e) {
        if (e.key === "ArrowLeft") { e.preventDefault(); show(index - 1); }
        if (e.key === "ArrowRight") { e.preventDefault(); show(index + 1); }
      });
    }
    link.addEventListener("click", function (e) {
      if (figure._swiped) { e.preventDefault(); return; }
      if (!window.HTMLDialogElement) return; // old browsers: open the image itself
      e.preventDefault();
      ensureLightbox();
      lbItems = items; showLb(index);
      lightbox.showModal();
    });
  });

  /* ---------- YouTube players: poster first; when a video scrolls into view it autoplays muted,
     when it scrolls away the player is removed again so only one player runs at a time ---------- */
  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var saveData = navigator.connection && navigator.connection.saveData;
  function makePlayer(v, muted) {
    var f = d.createElement("iframe");
    f.src = "https://www.youtube-nocookie.com/embed/" + v.dataset.video + "?autoplay=1&rel=0&modestbranding=1&playsinline=1" + (muted ? "&mute=1" : "");
    f.title = v.dataset.title || "Video";
    f.allow = "accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture; web-share";
    f.setAttribute("allowfullscreen", "");
    return f;
  }
  var videos = Array.prototype.slice.call(d.querySelectorAll(".video[data-video]"));
  videos.forEach(function (v) {
    var poster = v.querySelector(".video-poster");
    if (!poster || PREVIEW) return; // in the preview the poster simply links to YouTube
    v._poster = poster;
    poster.addEventListener("click", function (e) {
      e.preventDefault();
      var f = makePlayer(v, false);     // a click is a user gesture: play with sound
      (v.querySelector("iframe") || poster).replaceWith(f);
      v.dataset.userStarted = "1";
    });
  });
  if (videos.length && "IntersectionObserver" in window && !reduceMotion && !saveData && !PREVIEW) {
    var vio = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        var v = e.target;
        if (!v._poster) return;
        var frame = v.querySelector("iframe");
        if (e.isIntersecting && e.intersectionRatio >= 0.5 && !frame) {
          v.querySelector(".video-poster").replaceWith(makePlayer(v, true));   // autoplay, muted
        } else if (!e.isIntersecting && frame && !v.dataset.userStarted) {
          frame.replaceWith(v._poster);                                         // stop and free the player
        }
      });
    }, { threshold: [0, 0.5] });
    videos.forEach(function (v) { vio.observe(v); });
  }

  /* ---------- "Request a quote" buttons pre-select the machine ---------- */
  var select = d.getElementById("q-machine");
  if (select) {
    d.querySelectorAll("a[data-machine]").forEach(function (a) {
      a.addEventListener("click", function () {
        var name = a.dataset.machine;
        for (var i = 0; i < select.options.length; i++) {
          if (select.options[i].value === name) { select.selectedIndex = i; break; }
        }
      });
    });
  }

  /* ---------- quote form: submit in place, fall back to a normal POST ---------- */
  var form = d.querySelector(".quote-form");
  if (form && window.fetch && window.FormData) {
    var status = form.querySelector(".form-status");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (PREVIEW) { status.className = "form-status"; status.textContent = "This is a preview — on the live site this sends the request to info@NovoTechMachineTools.com."; return; }
      var ok = true;
      form.querySelectorAll("[required]").forEach(function (el) {
        var bad = !el.value.trim() || (el.type === "email" && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(el.value));
        el.setAttribute("aria-invalid", bad ? "true" : "false");
        if (bad) ok = false;
      });
      if (!ok) { status.className = "form-status is-error"; status.textContent = "Please add your name and a valid email address."; return; }
      var btn = form.querySelector("button[type=submit]");
      btn.disabled = true; status.className = "form-status"; status.textContent = "Sending…";
      fetch(form.action, { method: "POST", body: new FormData(form), headers: { "Accept": "application/json" } })
        .then(function (r) { return r.json(); })
        .then(function (j) {
          if (j && j.ok) {
            status.className = "form-status is-ok"; status.textContent = "Thanks — your request is on its way. We will reply within one business day.";
            form.reset();
          } else { throw new Error(j && j.error ? j.error : "send failed"); }
        })
        .catch(function () {
          status.className = "form-status is-error";
          status.innerHTML = "We could not send the form from this page. Please email <a href=\"mailto:info@NovoTechMachineTools.com\">info@NovoTechMachineTools.com</a> or call +1 647 526 5510.";
        })
        .then(function () { btn.disabled = false; });
    });
  }
})();
