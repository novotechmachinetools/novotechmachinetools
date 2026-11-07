/* The home page: the header video, the AI machine finder boxes, the machines-at-work slides and their videos, and the
   index of every kind of machine (folded on phones). Loaded by templates/home.html only. */
(function () {
  "use strict";
  var d = document, w = window;
  var reduce = w.matchMedia && w.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var conn = navigator.connection || {};
  var slow = !!conn.saveData || /(^|-)(2g|3g)$/.test(conn.effectiveType || "");

  /* ---------- header video: starts once the page has loaded; phones get the small file; a still picture on
     Save-Data, slow connections and reduced motion; pauses when it scrolls out of view; a button pauses it ---------- */
  var hero = d.querySelector(".hp-hero"), vid = hero && hero.querySelector("video"), toggle = hero && hero.querySelector(".hp-video-toggle");
  var userPaused = false, inView = true;
  function label(paused) {
    if (!toggle) return;
    toggle.setAttribute("aria-pressed", paused ? "true" : "false");
    toggle.querySelector(".hp-video-label").textContent = paused ? "Play video" : "Pause video";
  }
  function play() { var p = vid.play(); if (p && p.catch) p.catch(function () {}); }
  function startVideo() {
    if (!vid || reduce || slow) return;
    var small = Math.min(screen.width || 9999, w.innerWidth) < 900;
    vid.src = small ? vid.dataset.srcSmall : vid.dataset.src;
    vid.preload = "auto";
    play();
    if (toggle) toggle.hidden = false;
  }
  if (vid) {
    vid.addEventListener("playing", function () { vid.classList.add("is-playing"); label(false); });
    vid.addEventListener("pause", function () { label(true); });
    if (toggle) toggle.addEventListener("click", function () {
      if (vid.paused) { userPaused = false; play(); } else { userPaused = true; vid.pause(); }
    });
    if ("IntersectionObserver" in w) {
      new IntersectionObserver(function (es) {
        inView = es[0].isIntersecting;
        if (!vid.src) return;
        if (!inView && !vid.paused) vid.pause();
        else if (inView && vid.paused && !userPaused) play();
      }, { threshold: 0.15 }).observe(hero);
    }
    d.addEventListener("visibilitychange", function () { if (d.hidden && vid.src && !vid.paused) vid.pause(); else if (!d.hidden && inView && !userPaused && vid.src) play(); });
    if (d.readyState === "complete") setTimeout(startVideo, 300);
    else w.addEventListener("load", function () { setTimeout(startVideo, 300); });
  }

  /* ---------- the AI machine finder: the boxes on this page open the finder and ask the question ---------- */
  function askAI(q) {
    var open = d.querySelector(".site-header .ai-open");
    if (!open) return;
    q = (q || "").trim();
    if (q) {
      if (w.NTFinderAsk) { open.click(); w.NTFinderAsk(q); return; }
      w.NT_AI_PENDING = q;          // ai.js asks it as soon as it has loaded
    }
    open.click();
  }
  if (w.matchMedia && w.matchMedia("(max-width: 640px)").matches) {        // phones: a placeholder that fits
    Array.prototype.forEach.call(d.querySelectorAll(".hp-ask input[data-short]"), function (i) { i.placeholder = i.dataset.short; });
  }
  Array.prototype.forEach.call(d.querySelectorAll(".hp-ask"), function (f) {
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var inp = f.querySelector("input");
      askAI(inp.value);
      inp.value = "";
    });
  });
  Array.prototype.forEach.call(d.querySelectorAll("[data-ask]"), function (b) {
    b.addEventListener("click", function () { askAI(b.getAttribute("data-ask")); });
  });

  /* ---------- machines at work: one slide in view, arrows, thumbnails, swipe (scroll snap), autoplay ---------- */
  Array.prototype.forEach.call(d.querySelectorAll("[data-slider]"), function (sl) {
    var track = sl.querySelector(".hp-slides"), slides = track.querySelectorAll(".hp-slide"), thumbs = sl.querySelectorAll(".hp-thumbs button");
    var n = slides.length, cur = 0, timer = null, hold = false, DELAY = 6500;
    if (!n) return;
    sl.style.setProperty("--hp-slide", DELAY / 1000 + "s");
    function mark(i) {
      cur = i;
      Array.prototype.forEach.call(thumbs, function (t, k) {
        if (k === i) t.setAttribute("aria-current", "true"); else t.removeAttribute("aria-current");
      });
      var t = thumbs[i];
      if (t && t.parentNode && t.parentNode.parentNode.scrollWidth > t.parentNode.parentNode.clientWidth) {
        var list = t.parentNode.parentNode, li = t.parentNode;
        list.scrollTo({ left: li.offsetLeft - (list.clientWidth - li.offsetWidth) / 2, behavior: reduce ? "auto" : "smooth" });
      }
    }
    function go(i, fromUser) {
      i = (i + n) % n;
      track.scrollTo({ left: slides[i].offsetLeft - track.offsetLeft, behavior: reduce ? "auto" : "smooth" });
      mark(i);
      if (fromUser) restart();
    }
    var settle = null;
    track.addEventListener("scroll", function () {      // swiping: the slide that comes to rest is the current one
      clearTimeout(settle);
      settle = setTimeout(function () {
        var i = Math.round(track.scrollLeft / track.clientWidth);
        if (i !== cur && i >= 0 && i < n) { mark(i); restart(); }
      }, 120);
    }, { passive: true });
    function tick() { if (!hold && !d.hidden) go(cur + 1); }
    function restart() {
      clearInterval(timer);
      if (reduce) return;
      // the progress bar starts again with the new slide
      sl.classList.remove("is-auto"); void sl.offsetWidth; sl.classList.add("is-auto");
      timer = setInterval(tick, DELAY);
    }
    sl.querySelector(".hp-prev").addEventListener("click", function () { go(cur - 1, true); });
    sl.querySelector(".hp-next").addEventListener("click", function () { go(cur + 1, true); });
    Array.prototype.forEach.call(thumbs, function (t) { t.addEventListener("click", function () { go(+t.dataset.go, true); }); });
    track.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") { e.preventDefault(); go(cur + 1, true); }
      if (e.key === "ArrowLeft") { e.preventDefault(); go(cur - 1, true); }
    });
    function pause(on) { hold = on; sl.classList.toggle("is-paused", on); }
    sl.addEventListener("mouseenter", function () { pause(true); });
    sl.addEventListener("mouseleave", function () { pause(false); });
    sl.addEventListener("focusin", function () { pause(true); });
    sl.addEventListener("focusout", function () { pause(false); });
    sl.addEventListener("touchstart", function () { pause(true); }, { passive: true });
    sl.addEventListener("touchend", function () { setTimeout(function () { pause(false); }, 4000); }, { passive: true });
    if ("IntersectionObserver" in w) {          // the slides only move while they are on screen
      new IntersectionObserver(function (es) {
        if (es[0].isIntersecting) { if (!timer) restart(); } else { clearInterval(timer); timer = null; }
      }, { threshold: 0.3 }).observe(sl);
    } else restart();
    mark(0);
  });

  /* ---------- "Watch it run": the machine's video in a lightbox (youtube-nocookie) ---------- */
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  Array.prototype.forEach.call(d.querySelectorAll(".hp-watch[data-yt]"), function (b) {
    b.addEventListener("click", function () {
      var back = d.activeElement, id = b.dataset.yt, title = b.dataset.title || "Video";
      var m = d.createElement("div");
      m.className = "hp-modal";
      m.innerHTML = '<div class="hp-modal-box" role="dialog" aria-modal="true" aria-label="' + esc(title) + '">' +
        '<button type="button" class="hp-modal-close" aria-label="Close video">×</button>' +
        '<div class="hp-modal-frame"><iframe src="https://www.youtube-nocookie.com/embed/' + encodeURIComponent(id) + '?autoplay=1&rel=0&modestbranding=1&playsinline=1" title="' + esc(title) +
        '" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe></div>' +
        '<p class="hp-modal-title">' + esc(title) + "</p></div>";
      function close() {
        d.removeEventListener("keydown", onKey);
        if (m.parentNode) m.parentNode.removeChild(m);
        d.body.classList.remove("ai-locked");
        if (back && back.focus) back.focus();
        if (vid && vid.src && inView && !userPaused) play();
      }
      function onKey(e) { if (e.key === "Escape") close(); }
      m.addEventListener("click", function (e) { if (e.target === m || e.target.closest(".hp-modal-close")) close(); });
      d.addEventListener("keydown", onKey);
      d.body.appendChild(m);
      d.body.classList.add("ai-locked");
      if (vid && !vid.paused) vid.pause();
      m.querySelector(".hp-modal-close").focus();
    });
  });

  /* ---------- every kind of machine: folded on phones, open elsewhere ---------- */
  if (w.matchMedia && w.matchMedia("(max-width: 640px)").matches) {
    Array.prototype.forEach.call(d.querySelectorAll(".hp-idx"), function (x, i) { if (i > 0) x.removeAttribute("open"); });
  } else {
    Array.prototype.forEach.call(d.querySelectorAll(".hp-idx summary"), function (s) {
      s.addEventListener("click", function (e) { if (!w.matchMedia("(max-width: 640px)").matches) e.preventDefault(); });   // the index stays open on large screens
    });
  }
})();
