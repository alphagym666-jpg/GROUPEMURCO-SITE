(function () {
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Entrée du titre de l'accueil : les mots arrivent un à un ---------- */
  var heroTitle = document.querySelector('.hero-title');
  var heroBg = document.querySelector('.hero-bg');
  if (heroTitle) {
    var txt = heroTitle.textContent.trim();
    var escTxt = function (w) { return w.replace(/&/g, '&amp;').replace(/</g, '&lt;'); };
    heroTitle.setAttribute('aria-label', txt);
    heroTitle.innerHTML = txt.split(/\s+/).map(function (w, i) {
      return '<span class="w" aria-hidden="true" style="--i:' + i + '">' + escTxt(w) + '</span>';
    }).join(' ');
  }
  if (heroBg) {
    requestAnimationFrame(function () { requestAnimationFrame(function () {
      heroBg.classList.add('is-in');
      if (heroTitle) heroTitle.classList.add('is-in');
    }); });
  }

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

  /* ---------- Vidéo d'arrière-plan de l'accueil ----------
     Fichiers dans photos/ : video-accueil-exterieur.mp4 (+ .webm) et la version verticale
     video-accueil-exterieur-mobile.mp4 (+ .webm). On essaie dans l'ordre : version mobile
     (cellulaire seulement), WebM (plus léger) puis MP4. Si rien ne joue, la
     photo reste. Pas de vidéo en économie de données ou animations réduites. */
  var video = document.querySelector('.hero-video');
  var conn = navigator.connection || {};
  var slow = conn.saveData || /(^|-)2g$/.test(conn.effectiveType || '');
  if (video && video.getAttribute('data-src') && !reduce && !slow) {
    var bases = [];
    if (window.matchMedia('(max-width: 900px)').matches && video.getAttribute('data-src-mobile')) bases.push(video.getAttribute('data-src-mobile'));
    bases.push(video.getAttribute('data-src'));
    var webm = video.canPlayType('video/webm; codecs="vp9"') !== '';
    var queue = [];
    bases.forEach(function (b) { if (webm) queue.push(b + '.webm'); queue.push(b + '.mp4'); });
    var next = function () {
      if (!queue.length) return;
      video.src = queue.shift();
      var play = video.play();
      if (play && play.catch) play.catch(function () {});
    };
    video.addEventListener('playing', function () { video.classList.add('is-playing'); });
    video.addEventListener('error', next);
    window.addEventListener('load', next);
  }

  /* ---------- Apparition au défilement (titres, cartes, étapes…) ---------- */
  if (!reduce && 'IntersectionObserver' in window) {
    var rvIo = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); rvIo.unobserve(e.target); } });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px' });
    document.querySelectorAll('.section-head, .svc, .reason, .steps li, .stat, .svc-detail, .faq details, .commitments, .about-text, .city-gallery, .next-steps li, .cta-band .wrap > *').forEach(function (el) {
      var i = Array.prototype.indexOf.call(el.parentNode.children, el);
      el.style.setProperty('--d', Math.min(i, 6));
      el.classList.add('rv');
      rvIo.observe(el);
    });
  }

  /* ---------- Lueur qui suit la souris sur les cartes ---------- */
  document.querySelectorAll('.svc').forEach(function (card) {
    card.addEventListener('pointermove', function (e) {
      var r = card.getBoundingClientRect();
      card.style.setProperty('--mx', (e.clientX - r.left) + 'px');
      card.style.setProperty('--my', (e.clientY - r.top) + 'px');
    });
  });

  /* ---------- Scène avant / après pilotée par le défilement ---------- */
  var scrub = document.querySelector('.scrub');
  if (scrub) {
    var scrubSteps = scrub.querySelectorAll('.scrub-steps li');
    var scrubTick = false;
    var scrubRun = function () {
      var r = scrub.getBoundingClientRect();
      var total = r.height - window.innerHeight;
      var t = total > 0 ? Math.min(1, Math.max(0, -r.top / total)) : 1;
      var p = Math.min(1, Math.max(0, (t - 0.28) / 0.44));
      scrub.style.setProperty('--t', t.toFixed(4));
      scrub.style.setProperty('--p', p.toFixed(4));
      var idx = t < 0.3 ? 0 : (t < 0.72 ? 1 : 2);
      scrubSteps.forEach(function (li, i) { li.classList.toggle('on', i === idx); });
      scrubTick = false;
    };
    window.addEventListener('scroll', function () { if (!scrubTick) { scrubTick = true; requestAnimationFrame(scrubRun); } }, { passive: true });
    window.addEventListener('resize', scrubRun);
    scrubRun();
  }

  /* ---------- Photos avant / après par ville ----------
     Dépose photos/villes/<ville>-avant.jpg et <ville>-apres.jpg
     (ex. candiac-avant.jpg, saint-remi-apres.jpg). Elles remplacent
     toutes seules la photo d'exemple, sur l'accueil et la page de la ville. */
  var loadPair = function (slug, cb) {
    var a = new Image(), b = new Image(), n = 0, ok = true;
    var done = function () { if (++n === 2) cb(ok ? [a.src, b.src] : null); };
    a.onload = b.onload = done;
    a.onerror = b.onerror = function () { ok = false; done(); };
    a.src = 'photos/villes/' + slug + '-avant.jpg';
    b.src = 'photos/villes/' + slug + '-apres.jpg';
  };
  var showPair = function (ba, pair) {
    var before = ba.querySelector('[data-ba-before]'), after = ba.querySelector('[data-ba-after]');
    if (!before || !after) return;
    before.removeAttribute('srcset'); after.removeAttribute('srcset');
    before.src = pair[0]; after.src = pair[1];
  };
  document.querySelectorAll('.ba[data-ville]').forEach(function (ba) {
    var cap = document.querySelector('[data-city-caption]');
    loadPair(ba.getAttribute('data-ville'), function (pair) {
      if (!pair) return;
      showPair(ba, pair);
      if (cap) cap.textContent = 'Glissez la poignée pour comparer. Job réalisée à ' + ba.getAttribute('data-ville-nom') + '.';
    });
  });
  document.querySelectorAll('[data-city-gallery]').forEach(function (gal) {
    var ba = gal.querySelector('.ba');
    var cap = gal.querySelector('[data-city-caption]');
    var link = gal.querySelector('[data-city-link]');
    var chips = gal.querySelectorAll('.city-chip');
    var pick = function (chip, i) {
      chips.forEach(function (c) { c.setAttribute('aria-selected', c === chip ? 'true' : 'false'); });
      var slug = chip.getAttribute('data-ville'), nom = chip.textContent;
      link.href = 'calfeutrage-peinture-' + slug + '.html';
      link.textContent = 'Voir la page ' + nom;
      ba.classList.add('is-swapping');
      loadPair(slug, function (pair) {
        showPair(ba, pair || ['photos/villes-exemples/' + slug + '-avant.jpg', 'photos/villes-exemples/' + slug + '-apres.jpg']);
        cap.textContent = pair ? 'Job réalisée à ' + nom + '.' : "Photo d'une de nos jobs. Les photos de " + nom + ' arrivent bientôt.';
        setTimeout(function () { ba.classList.remove('is-swapping'); }, 150);
      });
    };
    chips.forEach(function (chip, i) { chip.addEventListener('click', function () { pick(chip, i); }); });
    if (chips.length) pick(chips[0], 0);
  });

  /* ---------- Vidéos des services : jouent seulement quand elles sont visibles ---------- */
  document.querySelectorAll('.svc-shot-video video').forEach(function (v) {
    if (reduce) { v.removeAttribute('autoplay'); v.pause(); return; }
    if (!('IntersectionObserver' in window)) return;
    new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { var p = v.play(); if (p && p.catch) p.catch(function () {}); } else v.pause(); });
    }, { threshold: 0.25 }).observe(v);
  });

  /* ---------- Cartes de services : vidéo au survol, avant → après au défilement ---------- */
  var hover = window.matchMedia('(hover: hover)').matches;
  var webmOk = document.createElement('video').canPlayType('video/webm; codecs="vp9"') !== '';
  document.querySelectorAll('.svc').forEach(function (card) {
    var v = card.querySelector('.svc-vid');
    if (v && hover && !reduce) {
      card.addEventListener('mouseenter', function () {
        if (!v.src) v.src = v.getAttribute('data-src') + (webmOk ? '.webm' : '.mp4');
        var p = v.play(); if (p && p.catch) p.catch(function () {});
        card.classList.add('is-playing');
      });
      card.addEventListener('mouseleave', function () { v.pause(); card.classList.remove('is-playing'); });
    }
    // sans souris (cellulaire) : la gouttière se nettoie quand la carte apparaît
    if (!hover && card.querySelector('.svc-after, .svc-zoom, .svc-trace') && 'IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) { setTimeout(function () { card.classList.add('is-revealed'); }, 500); io.disconnect(); } });
      }, { threshold: 0.6 });
      io.observe(card);
    }
  });

  /* ---------- Bande saisonnière : visible seulement les mois indiqués ---------- */
  document.querySelectorAll('[data-season]').forEach(function (bar) {
    var mois = bar.getAttribute('data-season').split(',').map(Number);
    if (mois.indexOf(new Date().getMonth() + 1) !== -1) bar.hidden = false;
  });

  /* ---------- Calfeutrage : les joints se tracent quand la photo arrive à l'écran ---------- */
  document.querySelectorAll('[data-joint-trace]').forEach(function (fig) {
    if (reduce || !('IntersectionObserver' in window)) { fig.classList.add('is-on'); return; }
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { fig.classList.add('is-on'); io.disconnect(); } });
    }, { threshold: 0.45 });
    io.observe(fig);
  });

  /* ---------- Calculateur de prix ---------- */
  var calc = document.querySelector('[data-calc]');
  if (calc && typeof PRIX !== 'undefined') {
    var NOMS = { calfeutrage: 'Calfeutrage', peinture: 'Peinture extérieure', brique: 'Lavage de brique' };
    var SVC = { calfeutrage: 'calfeutrage', peinture: 'peinture', brique: 'brique' };
    var arrondi = function (n) { return Math.round(n / 5) * 5; };
    var fmt = function (n) { return arrondi(n).toLocaleString('fr-CA') + ' $'; };
    var recalc = function () {
      var et = calc.querySelector('[data-etages]').value;
      var mult = (PRIX.etages && PRIX.etages[et]) || 1;
      var total = 0, lignes = [], details = ['Maison de ' + et + ' étage(s)'], svcs = [];
      calc.querySelectorAll('[data-svc-row]').forEach(function (row) {
        var k = row.getAttribute('data-svc-row'), cb = row.querySelector('input[type=checkbox]');
        var q = Math.max(0, parseFloat(row.querySelector('input[type=number]').value) || 0);
        row.classList.toggle('on', cb.checked);
        if (!cb.checked || !PRIX[k]) return;
        var m = mult;
        var v = Math.max(PRIX[k].min, q * PRIX[k].taux * m);
        total += v; svcs.push(SVC[k]);
        lignes.push('<li><span>' + NOMS[k] + '</span><span>' + fmt(v) + '</span></li>');
        var u = PRIX[k].unite; if (q > 1) u = u.replace(/^(\S+)/, '$1s').replace(/ (\S+)$/, function (m, w) { return ' ' + (/[sx]$/.test(w) ? w : w + 's'); });
        details.push(NOMS[k] + ' : ' + q + ' ' + u);
      });
      calc.querySelector('[data-total]').textContent = total ? fmt(total * 0.9) + ' – ' + fmt(total * 1.1) : '—';
      calc.querySelector('[data-lines]').innerHTML = lignes.join('');
      var cta = calc.querySelector('[data-calc-cta]');
      cta.href = 'contact.html?' + (svcs.length ? 'service=' + svcs.join(',') + '&' : '') + 'details=' +
        encodeURIComponent(details.join(' · ') + (total ? ' · Estimation en ligne : ' + fmt(total * 0.9) + ' – ' + fmt(total * 1.1) : ''));
    };
    calc.addEventListener('input', recalc);
    calc.addEventListener('change', recalc);
    recalc();
  }

  /* ---------- Formulaire : préremplir depuis le calculateur ---------- */
  var qs = new URLSearchParams(location.search);
  var svcParam = qs.get('service');
  if (svcParam) svcParam.split(',').forEach(function (k) { var c = document.querySelector('[data-svc="' + k + '"]'); if (c) c.checked = true; });
  var det = qs.get('details'), ta = document.getElementById('c-msg');
  if (det && ta && !ta.value) ta.value = det;

  /* ---------- Badges RBQ / assurance (config.js) ---------- */
  var badgeBox = document.querySelector('[data-badges]');
  if (badgeBox) {
    if (typeof NUMERO_RBQ === 'string' && NUMERO_RBQ) {
      var rbqSpan = badgeBox.querySelector('span');
      if (rbqSpan && /RBQ/.test(rbqSpan.textContent)) rbqSpan.innerHTML = '<b>✓</b> Licence RBQ ' + NUMERO_RBQ.replace(/</g, '');
    }
    if (typeof ASSURANCE === 'string' && ASSURANCE) badgeBox.insertAdjacentHTML('beforeend', '<span><b>✓</b> ' + ASSURANCE.replace(/</g, '') + '</span>');
  }

  /* ---------- Suivi des visites avec consentement (Loi 25) ---------- */
  var GA = (typeof GOOGLE_ANALYTICS_ID === 'string') ? GOOGLE_ANALYTICS_ID : '';
  var PX = (typeof META_PIXEL_ID === 'string') ? META_PIXEL_ID : '';
  var loadTracking = function () {
    if (GA) {
      var g = document.createElement('script'); g.async = true; g.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(GA); document.head.appendChild(g);
      window.dataLayer = window.dataLayer || []; window.gtag = function () { window.dataLayer.push(arguments); };
      window.gtag('js', new Date()); window.gtag('config', GA);
    }
    if (PX) {
      !function (f, b, e, v, n, t, s) { if (f.fbq) return; n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); };
        if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = '2.0'; n.queue = []; t = b.createElement(e); t.async = !0; t.src = v;
        s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s); }(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
      window.fbq('init', PX); window.fbq('track', 'PageView');
    }
  };
  if (GA || PX) {
    var choix = null;
    try { choix = localStorage.getItem('murco-consentement'); } catch (e) {}
    if (choix === 'oui') loadTracking();
    else if (choix !== 'non') {
      document.body.insertAdjacentHTML('beforeend', '<div class="consent-bar" role="dialog" aria-label="Témoins"><p>Nous utilisons des témoins pour mesurer la visite du site et améliorer nos publicités. <a href="/confidentialite.html">En savoir plus</a></p><div class="actions"><button class="btn" data-ok>Accepter</button><button class="btn btn-ghost" data-no>Refuser</button></div></div>');
      var bar = document.querySelector('.consent-bar');
      var save = function (v) { try { localStorage.setItem('murco-consentement', v); } catch (e) {} bar.remove(); if (v === 'oui') loadTracking(); };
      bar.querySelector('[data-ok]').addEventListener('click', function () { save('oui'); });
      bar.querySelector('[data-no]').addEventListener('click', function () { save('non'); });
    }
  }

  /* ---------- Numéro RBQ (config.js) dans le pied de page et À propos ---------- */
  if (typeof NUMERO_RBQ === 'string' && NUMERO_RBQ) {
    var num = NUMERO_RBQ.replace(/</g, '');
    document.querySelectorAll('[data-rbq-footer]').forEach(function (el) { el.textContent = 'Licence RBQ ' + num; });
    document.querySelectorAll('[data-rbq-num]').forEach(function (el) { el.textContent = ', no ' + num; });
  }

  /* ---------- Simulateur de couleur de revêtement ---------- */
  document.querySelectorAll('[data-simulateur]').forEach(function (sim) {
    var canvas = sim.querySelector('.sim-canvas');
    var ctx = canvas.getContext && canvas.getContext('2d', { willReadFrequently: true });
    if (!ctx) return;
    var photo = new Image(), masque = new Image(), loaded = 0, base = null, mask = null, lum = null, mean = 0.265;
    var ready = function () {
      if (++loaded < 2) return;
      var W = canvas.width, Hh = canvas.height;
      ctx.drawImage(masque, 0, 0, W, Hh); mask = ctx.getImageData(0, 0, W, Hh).data;
      ctx.drawImage(photo, 0, 0, W, Hh); base = ctx.getImageData(0, 0, W, Hh);
      var d = base.data; lum = new Float32Array(W * Hh); var sum = 0, cnt = 0;
      for (var i = 0, p = 0; i < d.length; i += 4, p++) {
        var L = (0.2126 * d[i] + 0.7152 * d[i + 1] + 0.0722 * d[i + 2]) / 255; lum[p] = L;
        var m = mask[i] / 255; sum += L * m; cnt += m;
      }
      if (cnt) mean = sum / cnt;
      sim.classList.add('is-ready');
    };
    photo.onload = masque.onload = ready;
    photo.src = sim.getAttribute('data-sim-photo'); masque.src = sim.getAttribute('data-masque');
    var paint = function (hex) {
      if (!base) return;
      if (!hex) { sim.classList.remove('is-colored'); return; }
      var r = parseInt(hex.slice(1, 3), 16), g = parseInt(hex.slice(3, 5), 16), b = parseInt(hex.slice(5, 7), 16);
      var out = ctx.createImageData(base); var o = out.data, d = base.data;
      for (var i = 0, p = 0; i < d.length; i += 4, p++) {
        var m = mask[i] / 255, f = Math.min(2.2, lum[p] / mean);
        o[i] = d[i] * (1 - m) + Math.min(255, r * f) * m;
        o[i + 1] = d[i + 1] * (1 - m) + Math.min(255, g * f) * m;
        o[i + 2] = d[i + 2] * (1 - m) + Math.min(255, b * f) * m;
        o[i + 3] = 255;
      }
      ctx.putImageData(out, 0, 0); sim.classList.add('is-colored');
    };
    var btns = sim.querySelectorAll('.sim-swatches button');
    var select = function (btn, hex) {
      btns.forEach(function (b) { b.setAttribute('aria-checked', b === btn ? 'true' : 'false'); });
      var go = function () { paint(hex); };
      if (base) go(); else { var t = setInterval(function () { if (base) { clearInterval(t); go(); } }, 100); }
    };
    btns.forEach(function (btn) { btn.addEventListener('click', function () { select(btn, btn.getAttribute('data-color')); }); });
    var custom = sim.querySelector('[data-custom]');
    if (custom) custom.addEventListener('input', function () { select(null, custom.value); });
  });

  /* ---------- Année dans le pied de page ---------- */
  document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });


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

  /* ---------- Formulaires : éviter le double envoi ---------- */
  document.querySelectorAll('form[data-netlify]').forEach(function (form) {
    var btn = form.querySelector('button[type="submit"]');
    if (!btn) return;
    var label = btn.textContent;
    form.addEventListener('submit', function () { btn.disabled = true; btn.textContent = 'Envoi en cours…'; });
    // retour arrière dans le navigateur : on réactive le bouton
    window.addEventListener('pageshow', function () { btn.disabled = false; btn.textContent = label; });
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
