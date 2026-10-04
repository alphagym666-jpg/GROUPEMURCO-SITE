(function () {
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Menu mobile ---------- */
  var header = document.querySelector('.site-header');
  var toggle = document.querySelector('.menu-toggle');
  if (toggle && header) {
    toggle.addEventListener('click', function () {
      var open = header.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.setAttribute('aria-label', open ? 'Fermer le menu' : 'Ouvrir le menu');
    });
    header.querySelectorAll('.nav a').forEach(function (a) {
      a.addEventListener('click', function () {
        header.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  /* ---------- En-tête au défilement + barre de progression ---------- */
  var bar = document.querySelector('.progress');
  function onScroll() {
    var y = window.scrollY || 0;
    if (header) header.classList.toggle('scrolled', y > 12);
    if (bar) {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.width = (h > 0 ? (y / h) * 100 : 0) + '%';
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- Apparition au défilement ---------- */
  var revealables = document.querySelectorAll('.reveal-once');
  if (reduce || !('IntersectionObserver' in window)) {
    revealables.forEach(function (el) { el.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -60px' });
    revealables.forEach(function (el) { io.observe(el); });
  }

  /* ---------- Compteurs ---------- */
  var nums = document.querySelectorAll('[data-count]');
  function runCount(el) {
    var target = parseFloat(el.getAttribute('data-count'));
    var suffix = el.getAttribute('data-suffix') || '';
    if (reduce) { el.textContent = target + suffix; return; }
    var start = null, dur = 1400;
    function step(ts) {
      if (start === null) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(target * eased) + suffix;
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  if (nums.length) {
    if (!('IntersectionObserver' in window)) { nums.forEach(runCount); }
    else {
      var io2 = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) { if (e.isIntersecting) { runCount(e.target); io2.unobserve(e.target); } });
      }, { threshold: 0.5 });
      nums.forEach(function (el) { io2.observe(el); });
    }
  }

  /* ---------- Parallaxe douce (souris + défilement) ---------- */
  var layers = document.querySelectorAll('.plx');
  if (layers.length && !reduce && window.innerWidth > 900) {
    var mx = 0, my = 0, sy = 0, ticking = false;
    function apply() {
      layers.forEach(function (l) {
        var d = parseFloat(l.getAttribute('data-depth')) || 0.2;
        l.style.transform = 'translate3d(' + (mx * d * 22) + 'px,' + ((my * d * 14) + (sy * d * -0.06)) + 'px,0)';
      });
      ticking = false;
    }
    function request() { if (!ticking) { ticking = true; requestAnimationFrame(apply); } }
    window.addEventListener('mousemove', function (e) {
      mx = (e.clientX / window.innerWidth) * 2 - 1;
      my = (e.clientY / window.innerHeight) * 2 - 1;
      request();
    }, { passive: true });
    window.addEventListener('scroll', function () { sy = window.scrollY; request(); }, { passive: true });
  }

  /* ---------- Curseur avant / après ---------- */
  document.querySelectorAll('.ba').forEach(function (ba) {
    var after = ba.querySelector('.ba-after');
    var handle = ba.querySelector('.ba-handle');
    var range = ba.querySelector('.ba-range');
    if (!after || !handle || !range) return;
    function set(pct) {
      pct = Math.max(0, Math.min(100, pct));
      after.style.clipPath = 'inset(0 0 0 ' + pct + '%)';
      handle.style.left = pct + '%';
      range.value = pct;
      range.setAttribute('aria-valuenow', Math.round(pct));
    }
    range.addEventListener('input', function () { set(parseFloat(range.value)); });
    function fromPointer(e) {
      var r = ba.getBoundingClientRect();
      var x = (e.touches ? e.touches[0].clientX : e.clientX) - r.left;
      set((x / r.width) * 100);
    }
    var dragging = false;
    ba.addEventListener('pointerdown', function (e) { dragging = true; fromPointer(e); });
    window.addEventListener('pointermove', function (e) { if (dragging) fromPointer(e); });
    window.addEventListener('pointerup', function () { dragging = false; });
    set(50);
    // petite démonstration au premier affichage
    if (!reduce && 'IntersectionObserver' in window) {
      var io3 = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (!e.isIntersecting) return;
          io3.unobserve(e.target);
          var t0 = null;
          function demo(ts) {
            if (t0 === null) t0 = ts;
            var p = Math.min((ts - t0) / 1800, 1);
            var eased = p < .5 ? 2 * p * p : 1 - Math.pow(-2 * p + 2, 2) / 2;
            set(50 + Math.sin(eased * Math.PI) * 26);
            if (p < 1 && !dragging) requestAnimationFrame(demo);
          }
          requestAnimationFrame(demo);
        });
      }, { threshold: 0.45 });
      io3.observe(ba);
    }
  });

  /* ---------- Année dans le pied de page ---------- */
  document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* ---------- Service pré-coché depuis la page Services ---------- */
  var p = new URLSearchParams(location.search).get('service');
  if (p) {
    var c = document.querySelector('[data-svc="' + p + '"]');
    if (c) c.checked = true;
  }

  /* ---------- Formulaire : regrouper les services cochés ---------- */
  document.querySelectorAll('form[data-netlify]').forEach(function (form) {
    var out = form.querySelector('input[name="services-choisis"]');
    if (!out) return;
    form.addEventListener('submit', function () {
      var vals = [];
      form.querySelectorAll('input[name="services"]:checked').forEach(function (c) { vals.push(c.value); });
      out.value = vals.join(', ');
    });
  });

  /* ---------- Avis clients ---------- */
  var grid = document.getElementById('reviews');
  if (grid && typeof AVIS !== 'undefined') {
    var empty = document.getElementById('reviews-empty');
    document.querySelectorAll('[data-google-review]').forEach(function (btn) {
      if (typeof LIEN_AVIS_GOOGLE === 'string' && LIEN_AVIS_GOOGLE) btn.href = LIEN_AVIS_GOOGLE;
      else btn.remove();
    });
    if (!AVIS.length) { grid.remove(); }
    else {
      if (empty) empty.remove();
      var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]; }); };
      grid.innerHTML = AVIS.map(function (a) {
        var n = Math.max(1, Math.min(5, Number(a.note) || 5));
        return '<figure class="review reveal"><div class="stars" aria-label="' + n + ' sur 5">' +
          '★'.repeat(n) + '☆'.repeat(5 - n) + '</div><blockquote>' + esc(a.texte) + '</blockquote>' +
          '<figcaption>' + esc(a.nom) + '<span>' + esc([a.ville, a.service].filter(Boolean).join(', ')) + '</span></figcaption></figure>';
      }).join('');
      grid.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('in'); });
    }
  }

  /* ---------- Vraies photos si présentes dans /photos ---------- */
  document.querySelectorAll('[data-photo]').forEach(function (holder) {
    var src = holder.getAttribute('data-photo');
    var img = new Image();
    img.onload = function () {
      img.alt = holder.getAttribute('data-alt') || '';
      img.loading = 'lazy';
      holder.innerHTML = '';
      holder.appendChild(img);
    };
    img.src = src;
  });
})();
