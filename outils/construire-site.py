# -*- coding: utf-8 -*-
# Régénère toutes les pages : python3 outils/construire-site.py (depuis le dossier du site)
"""Reconstruit le site Groupe Murco autour de 3 métiers :
calfeutrage, peinture de revêtement extérieur, lavage de brique à pression."""
import json, re, os, html as H
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(R)

TEL = '514-232-1837'; TELH = '+15142321837'
SITE = 'https://groupemurco.com/'
VILLES = [('sherrington', 'Sherrington'), ('napierville', 'Napierville'), ('saint-remi', 'Saint-Rémi'),
          ('chateauguay', 'Châteauguay'), ('la-prairie', 'La Prairie'), ('candiac', 'Candiac')]
def vurl(slug): return f'calfeutrage-peinture-{slug}.html'

SVC = [
  dict(id='calfeutrage', nom='Calfeutrage', court='Calfeutrage', prix='350',
       carte="Fenêtres, portes et joints de revêtement : on retire le vieux scellant fissuré et on refait des joints étanches et propres.",
       img='photos/metiers/carte-calfeutrage.jpg', alt="Fenêtre neuve dans la brique, joints blancs nets tout autour du cadre",
       hover='trace', hint='Voir les <b>joints</b>'),
  dict(id='peinture', nom='Peinture de revêtement extérieur', court='Peinture extérieure', prix='2 500',
       carte="Revêtement de bois, de vinyle, d'aluminium ou de fibrociment : préparation, apprêt et deux couches, au pistolet ou au rouleau.",
       img='photos/metiers/carte-peinture.jpg', alt='Peintre en nacelle sur un mur extérieur',
       hover='video', hint='<b>▶</b> En action'),
  dict(id='brique', nom='Lavage de brique à pression', court='Lavage de brique', prix='400',
       carte="Mousse, saleté, efflorescence et taches noires : on nettoie la brique et la pierre avec la bonne pression, sans abîmer les joints.",
       img='photos/avant-apres/carte-brique-avant.jpg', alt='Brique encrassée : coulisses noires, efflorescence et mousse',
       after='photos/avant-apres/carte-brique-apres.jpg', hover='avant-apres', hint='Sale <b>→</b> propre'),
]
SVCD = {s['id']: s for s in SVC}

PHONE_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 3h3l2 5-2.5 1.5a11 11 0 0 0 7 7L16 14l5 2v3a2 2 0 0 1-2 2A17 17 0 0 1 3 5a2 2 0 0 1 2-2z"/></svg>'
SMS_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/></svg>'
ICON = {
 'ruler': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 15L15 3l6 6L9 21z"/><path d="M7 11l2 2M10 8l2 2M13 5l2 2"/></svg>',
 'badge': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2l3 3h4v4l3 3-3 3v4h-4l-3 3-3-3H5v-4l-3-3 3-3V5h4z"/><path d="M8.5 12l2.3 2.3L15.5 9.6"/></svg>',
 'pin': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s7-6.2 7-12A7 7 0 0 0 5 10c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.6"/></svg>',
 'shield': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2l8 3v6c0 5-3.4 9.3-8 11-4.6-1.7-8-6-8-11V5z"/></svg>',
 'drop': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3s6 6.6 6 11a6 6 0 0 1-12 0c0-4.4 6-11 6-11z"/></svg>',
 'broom': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 3l7 7M12.5 8.5l3 3M4 20l7-9 2 2-9 7z"/></svg>',
}

def jsonld_business():
    return json.dumps({"@context": "https://schema.org", "@type": "HomeAndConstructionBusiness", "name": "Groupe Murco",
        "legalName": "9568-5590 Québec inc.", "url": SITE, "telephone": TELH, "email": "info@groupemurco.com",
        "image": SITE + "assets/icone-murco.png", "logo": SITE + "assets/icone-murco.png",
        "address": {"@type": "PostalAddress", "addressLocality": "Sherrington", "addressRegion": "QC", "addressCountry": "CA"},
        "areaServed": [n for _, n in VILLES] + ["Rive-Sud de Montréal"], "priceRange": "$$",
        "description": "Entrepreneur licencié RBQ : calfeutrage, peinture de revêtement extérieur et lavage de brique à pression sur la Rive-Sud.",
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s['nom']}} for s in SVC]}}, ensure_ascii=False)

NAV = [('index.html', 'Accueil'), ('services.html', 'Services'), ('estimation.html', 'Estimation'), ('a-propos.html', 'À propos'), ('contact.html', 'Contact')]

def head(fname, title, desc, canonical=True, noindex=False, extra=''):
    pre = '/' if fname == '404.html' else ''
    url = SITE + ('' if fname == 'index.html' else fname)
    cur = ' aria-current="page"'
    nav = ''.join(f'<a href="{pre}{h}"{cur if h == fname else ""}>{t}</a>' for h, t in NAV)
    t = H.escape(title, quote=True); d = H.escape(desc, quote=True)
    return f'''<!doctype html>
<html lang="fr-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>document.documentElement.classList.add('js')</script>
<meta name="google-site-verification" content="JprTaUYPd07KYgobUB6DsRmsi9oZLU_cRQrrOe29ooU">
{'<meta name="robots" content="noindex">' + chr(10) if noindex else ''}<title>{t}</title>
<meta name="description" content="{d}">
{f'<link rel="canonical" href="{url}">' + chr(10) if canonical else ''}<meta property="og:type" content="website">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:image" content="{SITE}assets/partage.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
{f'<meta property="og:url" content="{url}">' + chr(10) if canonical else ''}<meta property="og:site_name" content="Groupe Murco">
<meta name="twitter:card" content="summary_large_image">
<meta property="og:locale" content="fr_CA">
<meta name="theme-color" content="#1B1F22">
<link rel="icon" href="/favicon.ico" sizes="48x48 96x96 192x192">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="{pre}assets/fonts/anton-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{pre}assets/fonts/archivo-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{pre}assets/styles.v2.css">
<script type="application/ld+json">{jsonld_business()}</script>
{extra}</head>
<body>
<div class="progress" aria-hidden="true"></div>
<a class="skip" href="#contenu">Aller au contenu</a>
<div class="season-bar" data-season="9,10,11" hidden><div class="wrap"><span><strong>Calfeutrage d'automne :</strong> on scelle tant qu'il fait plus de 5 °C. Réservez avant le gel.</span><a href="tel:+15142321837">Appeler</a></div></div>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="{pre}index.html" aria-label="Groupe Murco, accueil"><img src="{pre}assets/logo-murco.svg" alt="Groupe Murco" width="200" height="56"></a>
    <nav class="nav" aria-label="Menu principal">{nav}</nav>
    <div class="header-actions">
      <a class="header-phone" href="tel:{TELH}">{TEL}</a>
      <a class="btn" href="{pre}contact.html">Soumission gratuite</a>
    </div>
    <button class="menu-toggle" aria-label="Ouvrir le menu" aria-expanded="false"><span></span><span></span><span></span></button>
  </div>
</header>
<main id="contenu">
'''

def foot(fname, scripts=''):
    pre = '/' if fname == '404.html' else ''
    svc = ''.join(f'<li><a href="{pre}services.html#{s["id"]}">{s["nom"]}</a></li>' for s in SVC)
    vil = ''.join(f'<li><a href="{pre}{vurl(sl)}">{n}</a></li>' for sl, n in VILLES)
    return f'''</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <img src="{pre}assets/logo-murco-blanc.svg" alt="Groupe Murco" width="190" height="52">
        <p>Calfeutrage, peinture extérieure et lavage de brique à Sherrington et sur la Rive-Sud de Montréal.</p>
        <p><a href="tel:{TELH}">{TEL}</a><br><a href="mailto:info@groupemurco.com">info@groupemurco.com</a></p>
        <p class="footer-rbq" data-rbq-footer>Entrepreneur détenteur d'une licence RBQ</p>
      </div>
      <div>
        <h2>Services</h2>
        <ul>{svc}</ul>
      </div>
      <div>
        <h2>Secteur</h2>
        <ul>{vil}</ul>
      </div>
      <div>
        <h2>Entreprise</h2>
        <ul>
          <li><a href="{pre}a-propos.html">À propos</a></li>
          <li><a href="{pre}avis.html">Laisser un avis</a></li>
          <li><a href="{pre}estimation.html">Estimation en ligne</a></li>
          <li><a href="{pre}contact.html">Demander une soumission</a></li>
          <li><a href="{pre}confidentialite.html">Politique de confidentialité</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© <span data-year>2026</span> Groupe Murco, une dénomination de 9568-5590 Québec inc.</span>
      <span>Sherrington (Québec)</span>
    </div>
  </div>
</footer>
<nav class="mbar" aria-label="Nous joindre rapidement"><a href="tel:{TELH}">{PHONE_SVG} Appeler</a><a href="sms:{TELH}">{SMS_SVG} Texto</a><a class="mbar-main" href="{pre}contact.html">Soumission</a></nav>
{scripts}<script src="{pre}assets/config.js"></script>
<script src="{pre}assets/main.v2.js"></script>
</body>
</html>
'''

def page_head(img, title, lead, extra=''):
    return f'''<section class="page-head has-photo">
  <picture class="head-img"><source media="(max-width: 900px)" srcset="{img}-1100.jpg"><img src="{img}.jpg" alt="" width="1920" height="620"></picture>
  <div class="wrap">
    <h1>{title}</h1>
    <p class="lead">{lead}</p>{extra}
  </div>
</section>
'''

def cta_band(title='Parlons de votre maison.', text='Décrivez-nous le travail, nous vous revenons avec un prix écrit.'):
    return f'''<section class="cta-band has-photo">
  <picture class="band-img"><source media="(max-width: 900px)" srcset="photos/maquette/bande-maison-soir-1100.jpg"><img src="photos/maquette/bande-maison-soir.jpg" alt="" loading="lazy" width="1920" height="900"></picture>
  <div class="wrap">
    <div>
      <h2>{title}</h2>
      <p>{text}</p>
    </div>
    <div class="actions">
      <a class="btn" href="contact.html">Demander une soumission</a>
      <a class="btn btn-light" href="tel:{TELH}">{PHONE_SVG} {TEL}</a>
    </div>
  </div>
</section>
'''

JOINT_PATHS = '<path class="jt-line" pathLength="1" d="M331 0 L284 848"/><path class="jt-line" pathLength="1" d="M1120 0 L1163 548"/><path class="jt-line" pathLength="1" d="M232 918 L1198 598"/>'
JOINT_FIG = '''<div class="step-pair step-pair-sm">
    <figure class="step-vid" data-step-video>
      <div class="step-frame">
        <video muted loop playsinline preload="none" poster="photos/calfeutrage/arracher.jpg?v=4" aria-label="Retrait du vieux calfeutrage entre un cadre de porte et la brique">
          <source src="photos/calfeutrage/arracher.webm" type="video/webm">
          <source src="photos/calfeutrage/arracher.mp4" type="video/mp4">
        </video>
        <span class="step-tag">1 · On arrache</span>
      </div>
    </figure>
    <span class="step-arrow" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span>
    <figure class="step-vid" data-step-video>
      <div class="step-frame">
        <video muted loop playsinline preload="none" poster="photos/calfeutrage/refaire.jpg?v=4" aria-label="Joints neufs, lisses et blancs, autour d'une fenêtre dans la brique">
          <source src="photos/calfeutrage/refaire.webm" type="video/webm">
          <source src="photos/calfeutrage/refaire.mp4" type="video/mp4">
        </video>
        <span class="step-tag">2 · On refait</span>
      </div>
    </figure>
  </div>'''
JOINT_SECTION = '''<section class="section joint-section" id="calfeutrage-de-pres">
  <div class="wrap steps-grid">
    <div class="joint-copy">
      <p class="eyebrow"><b>01</b> Calfeutrage</p>
      <h2>On arrache le vieux. On refait propre.</h2>
      <p>Un joint fendillé ne se recouvre pas : il s'enlève au complet, jusqu'à la brique et au cadre. Seulement après, on scelle de nouveau, d'une ligne continue et lisse.</p>
      <ol class="joint-steps">
        <li><b>1</b><span><strong>On retire le vieux calfeutrage</strong> Tout, pas juste par-dessus.</span></li>
        <li><b>2</b><span><strong>On refait le joint</strong> Surfaces propres, scellant extérieur haute performance, fini lisse.</span></li>
      </ol>
      <a class="btn" href="services.html#calfeutrage">Voir le calfeutrage</a>
    </div>
    <div class="step-pair">
      <figure class="step-vid" data-step-video>
        <div class="step-frame">
          <video muted loop playsinline preload="none" poster="photos/calfeutrage/arracher.jpg?v=4" aria-label="Retrait du vieux calfeutrage entre un cadre de porte et la brique">
            <source src="photos/calfeutrage/arracher.webm" type="video/webm">
            <source src="photos/calfeutrage/arracher.mp4" type="video/mp4">
          </video>
          <span class="step-tag">1 · On arrache</span>
        </div>
      </figure>
      <span class="step-arrow" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span>
      <figure class="step-vid" data-step-video>
        <div class="step-frame">
          <video muted loop playsinline preload="none" poster="photos/calfeutrage/refaire.jpg?v=4" aria-label="Joints neufs, lisses et blancs, autour d'une fenêtre dans la brique">
            <source src="photos/calfeutrage/refaire.webm" type="video/webm">
            <source src="photos/calfeutrage/refaire.mp4" type="video/mp4">
          </video>
          <span class="step-tag">2 · On refait</span>
        </div>
      </figure>
    </div>
  </div>
</section>
'''

def svc_cards(cta_title='Plusieurs travaux à faire?', cta_text='Calfeutrage, peinture et brique peuvent se faire dans le même chantier : une seule soumission.'):
    out = []
    for s in SVC:
        if s['hover'] == 'video':
            extra = f'<video class="svc-vid" muted loop playsinline preload="none" aria-hidden="true" tabindex="-1" data-src="photos/metiers/video-{s["id"]}"></video><span class="svc-hint">{s["hint"]}</span>'
            cls = 'svc-photo'
        elif s['hover'] == 'trace':
            extra = '<svg class="svc-trace" viewBox="0 0 1600 1000" preserveAspectRatio="xMidYMid slice" aria-hidden="true">' + JOINT_PATHS + f'</svg><span class="svc-hint">{s["hint"]}</span>'
            cls = 'svc-photo'
        elif s['hover'] == 'zoom':
            extra = f'<span class="svc-hint">{s["hint"]}</span>'; cls = 'svc-photo svc-zoom'
        else:
            extra = f'<img class="svc-after" src="{s["after"]}" width="640" height="400" loading="lazy" alt="" aria-hidden="true"><span class="svc-hint">{s["hint"]}</span>'
            cls = 'svc-photo'
        out.append(f'''<a class="svc" href="services.html#{s["id"]}">
  <span class="{cls}"><img src="{s["img"]}" width="640" height="400" loading="lazy" alt="{H.escape(s["alt"], quote=True)}">{extra}</span>
  <h3>{s["nom"]}</h3>
  <p>{s["carte"]}</p>
  <span class="from">Dès {s["prix"]}&nbsp;$</span>
  <span class="go">Voir le détail</span>
</a>''')
    return f'''<div class="svc-grid svc-grid-3">{''.join(out)}
      <div class="svc-cta">
        <div>
          <h3>{cta_title}</h3>
          <p>{cta_text}</p>
        </div>
        <a class="btn" href="estimation.html">Estimer mon prix</a>
      </div>
    </div>'''

def faq_block(qa, title="Ce qu'on nous demande souvent", cls='section section-mist'):
    det = ''.join(f'<details><summary>{H.escape(q, quote=False)}</summary><p>{H.escape(a, quote=False)}</p></details>' for q, a in qa)
    ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa]}, ensure_ascii=False)
    return f'''<section class="{cls}">
  <div class="wrap">
    <div class="section-head center">
      <h2>{title}</h2>
    </div>
    <div class="faq">{det}</div>
  </div>
</section>
<script type="application/ld+json">{ld}</script>
'''

SIMULATEUR = '''<section class="section sim-section" id="couleurs">
  <div class="wrap">
    <div class="section-head center">
      <h2>Essayez une couleur</h2>
      <p>Choisissez une teinte et voyez tout de suite l'effet sur un revêtement. On vous aide ensuite à choisir la bonne peinture pour votre maison.</p>
    </div>
    <div class="sim" data-simulateur data-sim-photo="photos/simulation/maison.jpg" data-masque="photos/simulation/maison-masque.png">
      <div class="sim-stage">
        <img class="sim-base" src="photos/simulation/maison.jpg" width="1280" height="853" loading="lazy" alt="Maison à revêtement de bois peint">
        <canvas class="sim-canvas" width="1280" height="853" aria-hidden="true"></canvas>
        <span class="sim-tag">Simulation</span>
      </div>
      <div class="sim-panel">
        <p class="sim-label">Couleur du revêtement</p>
        <div class="sim-swatches" role="radiogroup" aria-label="Couleurs">
          <button type="button" role="radio" aria-checked="true" data-color="" style="--c:#5a5f6e" title="Couleur d'origine"><span>Origine</span></button>
          <button type="button" role="radio" aria-checked="false" data-color="#E4DCCB" style="--c:#E4DCCB" title="Blanc cassé"><span>Blanc cassé</span></button>
          <button type="button" role="radio" aria-checked="false" data-color="#2F3437" style="--c:#2F3437" title="Charbon"><span>Charbon</span></button>
          <button type="button" role="radio" aria-checked="false" data-color="#7F8C76" style="--c:#7F8C76" title="Vert sauge"><span>Vert sauge</span></button>
          <button type="button" role="radio" aria-checked="false" data-color="#3E5670" style="--c:#3E5670" title="Bleu marine"><span>Bleu marine</span></button>
          <button type="button" role="radio" aria-checked="false" data-color="#B9A890" style="--c:#B9A890" title="Grège"><span>Grège</span></button>
          <button type="button" role="radio" aria-checked="false" data-color="#8C3B2E" style="--c:#8C3B2E" title="Rouge grange"><span>Rouge grange</span></button>
        </div>
        <label class="sim-custom">Ou votre couleur : <input type="color" value="#C9B79C" data-custom></label>
        <p class="sim-note">Simulation à titre indicatif. Le rendu réel dépend de la peinture, du fini et de la lumière.</p>
        <a class="btn" href="contact.html?service=peinture">Parler de mon projet de peinture</a>
      </div>
    </div>
  </div>
</section>
'''

pages = {}

# ===================== ACCUEIL =====================
marq_items = ['Calfeutrage', 'Peinture extérieure', 'Lavage de brique', 'Licence RBQ'] + [n for _, n in VILLES]
marq = ''.join(f'<span>{w}</span>' for w in marq_items * 2)
index_main = f'''
<section class="hero hero-bg">
  <picture class="hero-bg-img">
    <source media="(max-width: 900px)" srcset="photos/metiers/entete-peinture-1100.jpg">
    <img src="photos/metiers/entete-peinture.jpg" alt="" width="1920" height="620" fetchpriority="high">
  </picture>
  <!-- Vidéo d arrière-plan : peinture extérieure (Pexels 13372330, 9182402). À remplacer par une vraie vidéo de Groupe Murco. -->
  <video class="hero-video" muted loop playsinline preload="none" aria-hidden="true" tabindex="-1"
         data-src="photos/video-accueil-exterieur" data-src-mobile="photos/video-accueil-exterieur-mobile"></video>
  <div class="wrap hero-inner">
    <div class="hero-copy">
      <h1 class="hero-title">Calfeutrage, peinture et brique, faits comme il faut.</h1>
      <p class="lead">Entrepreneur licencié RBQ basé à Sherrington. On scelle, on repeint et on redonne vie à l'extérieur de votre maison sur la Rive-Sud. Soumission écrite et gratuite.</p>
      <div class="hero-actions">
        <a class="btn" href="contact.html">Demander une soumission</a>
        <a class="btn btn-light" href="estimation.html">Estimer mon prix</a>
        <a class="btn btn-light hero-tel" href="tel:{TELH}">{PHONE_SVG} {TEL}</a>
      </div>
      <div class="trust">
        <div>{ICON['badge']} Licence RBQ</div>
        <div>{ICON['ruler']} Calfeutrage dès 350&nbsp;$</div>
        <div>{ICON['pin']} Basé à Sherrington</div>
      </div>
    </div>
  </div>
  <a class="scroll-cue" href="#avant-apres" aria-label="Voir la suite"><span></span></a>
</section>

<div class="trust-bar">
  <div class="wrap trust-bar-inner" data-badges>
    <span><b>✓</b> Licence RBQ</span>
    <span><b>✓</b> Soumission gratuite et écrite</span>
    <span><b>✓</b> Garantie 2 ans main-d'œuvre</span>
    <span><b>✓</b> Paiement après les travaux</span>
  </div>
</div>
<div class="marquee" aria-hidden="true"><div class="marquee-track">{marq}</div></div>

<section class="scrub" id="avant-apres" aria-label="Simulation : la même maison avant et après la peinture">
  <div class="scrub-sticky">
    <div class="scrub-media">
      <img class="scrub-before" src="photos/simulation/facade-avant.jpg" width="1280" height="853" loading="lazy" alt="Maison au revêtement terni, délavé et taché">
      <img class="scrub-after" src="photos/simulation/facade-apres.jpg" width="1280" height="853" loading="lazy" alt="La même maison repeinte : revêtement bleu ardoise et moulures blanches (simulation)">
      <span class="scrub-line" aria-hidden="true"></span>
    </div>
    <div class="wrap scrub-copy">
      <p class="scrub-kicker">Une peinture fraîche, la même maison · simulation</p>
      <ol class="scrub-steps">
        <li class="on"><h2>Avant</h2><p>Un revêtement terni, des joints qui fendillent : la maison a l'air plus vieille qu'elle ne l'est.</p></li>
        <li><h2>Préparation</h2><p>Lavage, grattage, calfeutrage des joints et apprêt. C'est là que se joue la durée d'une peinture.</p></li>
        <li><h2>Après</h2><p>Deux couches appliquées proprement, des lignes nettes. Une façade qui fait honneur au quartier.</p></li>
      </ol>
      <div class="scrub-bar" aria-hidden="true"><span></span></div>
    </div>
  </div>
</section>

<section class="section section-mist">
  <div class="wrap">
    <div class="section-head">
      <h2>Nos trois métiers</h2>
      <p>Tout ce qui protège et embellit l'extérieur de votre maison, du joint de fenêtre jusqu'à la façade complète.</p>
    </div>
    {svc_cards()}
  </div>
</section>

{JOINT_SECTION}{SIMULATEUR}
<section class="section section-dark on-dark">
  <div class="wrap">
    <div class="section-head">
      <h2>Un entrepreneur, pas un amateur</h2>
    </div>
    <div class="reasons">
      <div class="reason"><div class="ic">{ICON['badge']}</div><h3>Licencié RBQ</h3><p>Groupe Murco détient sa licence de la Régie du bâtiment du Québec. Vous faites affaire avec une entreprise en règle.</p></div>
      <div class="reason"><div class="ic">{ICON['shield']}</div><h3>Préparation d'abord</h3><p>Lavage, grattage, scellant retiré au complet : une peinture ou un joint dure seulement si la surface est bien préparée.</p></div>
      <div class="reason"><div class="ic">{ICON['ruler']}</div><h3>Un prix clair</h3><p>Mesuré sur place et écrit sur la soumission. Vous savez exactement ce que vous payez avant qu'on commence.</p></div>
    </div>
  </div>
</section>

<section class="garantie">
  <div class="wrap garantie-inner">
    <div class="garantie-badge" aria-hidden="true"><span>2</span>ans</div>
    <div>
      <h2>Garantie 2 ans sur la main-d'œuvre</h2>
      <p>Un joint qui décolle ou une peinture qui pèle à cause de notre application? On revient corriger, sans frais, pendant deux ans.</p>
    </div>
  </div>
</section>

<section class="proof">
  <picture class="proof-img"><source media="(max-width: 900px)" srcset="photos/maquette/bande-maison-bleue-1100.jpg"><img src="photos/maquette/bande-maison-bleue.jpg" alt="" loading="lazy" width="1920" height="900"></picture>
  <div class="wrap proof-inner">
    <blockquote>
      <p>Une maison se protège par ses détails.</p>
      <p class="proof-sub">Un joint bien scellé, une peinture qui tient, une brique qui respire.</p>
      <cite>Samuel Michea, fondateur</cite>
    </blockquote>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head center">
      <h2>Quatre étapes, c'est tout</h2>
    </div>
    <ol class="steps">
      <li><h3>Vous nous écrivez</h3><p>Par le formulaire, par texto ou par téléphone, avec l'adresse et le travail à faire.</p></li>
      <li><h3>On mesure sur place</h3><p>Visite gratuite, puis une soumission écrite avec le détail des travaux.</p></li>
      <li><h3>On fait le travail</h3><p>À la date convenue, chantier protégé et nettoyé chaque jour.</p></li>
      <li><h3>Vous payez à la fin</h3><p>Facture par courriel. Virement Interac, comptant ou chèque.</p></li>
    </ol>
  </div>
</section>

<section class="section section-mist">
  <div class="wrap">
    <div class="section-head">
      <h2>Où nous travaillons</h2>
      <p>Sherrington, Napierville, Saint-Rémi, Châteauguay, La Prairie, Candiac et les environs. Un peu plus loin? Appelez-nous, on regarde ça ensemble.</p>
    </div>
    <nav class="svc-nav city-links" aria-label="Nos villes">{''.join(f'<a href="{vurl(sl)}">{n}</a>' for sl, n in VILLES)}</nav>
    <div class="stats">
      <div class="stat"><div class="n"><span data-count="3">3</span></div><p>métiers de la construction, un seul entrepreneur.</p></div>
      <div class="stat"><div class="n"><span>RBQ</span></div><p>licence de la Régie du bâtiment du Québec.</p></div>
      <div class="stat"><div class="n"><span data-count="2">2</span><span>&nbsp;ans</span></div><p>de garantie sur la main-d'œuvre.</p></div>
      <div class="stat"><div class="n"><span data-count="24">24</span><span>h</span></div><p>c'est le délai que nous visons pour vous répondre.</p></div>
    </div>
  </div>
</section>
{cta_band()}'''
pages['index.html'] = head('index.html', 'Groupe Murco | Calfeutrage, peinture extérieure et lavage de brique, Rive-Sud',
    'Entrepreneur licencié RBQ à Sherrington : calfeutrage de fenêtres et de portes, peinture de revêtement extérieur et lavage de brique à pression sur la Rive-Sud. Soumission gratuite.') + (lambda s: s[s.index('<main id="contenu">') + len('<main id="contenu">\n'):s.index('</main>')])(open('index.html', encoding='utf-8').read()) + foot('index.html')  # l'accueil est maintenant retouché à la main : on reprend son contenu

# ===================== SERVICES =====================
DETAIL = {
 'calfeutrage': dict(
   intro="Un joint fissuré laisse entrer l'eau, l'air froid et les insectes. Avec le temps, il fait pourrir les cadres et les bas de revêtement. Un bon calfeutrage, c'est la protection la moins chère de votre maison.",
   liste=["Retrait complet du vieux scellant, pas juste par-dessus", "Nettoyage et préparation des surfaces", "Fond de joint au besoin, pour un joint qui travaille bien", "Scellant extérieur haute performance, de la couleur de vos cadres", "Fenêtres, portes, coins de revêtement, solins et passages de fils"],
   ideal="Joints qui craquent, infiltrations d'air, avant de repeindre, maisons de 10 ans et plus.",
   prixnote="Prix à l'ouverture (fenêtre ou porte) ou au pied linéaire de joint, indiqué sur votre soumission.",
   media=('img', 'photos/metiers/calfeutrage-joint.jpg', "Gros plan d'un joint blanc net et continu entre le cadre de fenêtre et la brique"),
   media2=('trace', '', '')),
 'peinture': dict(
   intro="Une peinture extérieure dure aussi longtemps que sa préparation. On lave, on gratte, on calfeutre et on applique un apprêt avant les deux couches de finition, au pistolet ou au rouleau selon la surface.",
   liste=["Lavage du revêtement et grattage de la peinture qui lève", "Calfeutrage des joints avant la peinture", "Apprêt adapté : bois, vinyle, aluminium ou fibrociment", "Deux couches de finition, au pistolet airless ou au rouleau", "Protection des fenêtres, du terrain et des plates-bandes"],
   ideal="Revêtement terni ou écaillé, changement de couleur, maison à vendre, boiseries et soffites.",
   prixnote="Prix au pied carré de surface peinte (préparation incluse), indiqué sur votre soumission.",
   media=('video', 'photos/metiers/video-peinture', 'Peintre au pistolet airless'),
   media2=('img', 'photos/metiers/peinture-1.jpg', 'Peintre en nacelle sur un mur extérieur')),
 'brique': dict(
   intro="La brique et la pierre accumulent mousse, saleté, efflorescence blanche et coulisses noires. Un lavage bien dosé leur redonne leur couleur d'origine, sans gruger les joints de mortier.",
   liste=["Pression et buse ajustées à la brique et au mortier", "Nettoyant adapté : mousse, efflorescence, taches de rouille", "Rinçage complet de la façade et du terrain", "Inspection des joints de mortier et signalement des réparations", "Option scellant hydrofuge après le lavage"],
   ideal="Façades de brique ou de pierre ternies, côté nord verdâtre, avant une vente.",
   prixnote="Prix au pied carré de brique lavée, indiqué sur votre soumission.",
   media=('img', 'photos/metiers/brique-1.jpg', 'Façade de brique rouge'),
   media2=('ba', 'brique', 'Brique encrassée avant, brique propre après le lavage (simulation)')),
}
def media_html(m):
    if m[0] == 'trace':
        return JOINT_FIG
    if m[0] == 'ba':
        return f'''<div class="ba-shell svc-ba">
  <div class="ba is-photo" role="group" aria-label="Comparateur avant et après">
    <span class="ba-tag before">Avant</span>
    <span class="ba-tag after">Après</span>
    <img class="ba-img" src="photos/avant-apres/{m[1]}-avant.jpg" width="1280" height="800" loading="lazy" alt="{H.escape(m[2], quote=True)}">
    <div class="ba-after" aria-hidden="true"><img class="ba-img" src="photos/avant-apres/{m[1]}-apres.jpg" width="1280" height="800" loading="lazy" alt=""></div>
    <div class="ba-handle"><span class="ba-grip"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M8 7l-5 5 5 5M16 7l5 5-5 5"/></svg></span></div>
    <input class="ba-range" type="range" min="0" max="100" value="50" aria-label="Glisser pour comparer avant et après">
  </div>
</div>'''
    if m[0] == 'video':
        return f'<div class="svc-shot svc-shot-video"><video muted loop playsinline autoplay preload="metadata" poster="photos/metiers/peinture-video.jpg" aria-label="{m[2]}"><source src="{m[1]}.webm" type="video/webm"><source src="{m[1]}.mp4" type="video/mp4"></video></div>'
    return f'<div class="svc-shot"><img src="{m[1]}" width="1600" height="1000" loading="lazy" alt="{H.escape(m[2], quote=True)}"></div>'
arts = []
for s in SVC:
    d = DETAIL[s['id']]
    li = ''.join(f'<li>{x}</li>' for x in d['liste'])
    arts.append(f'''<article class="svc-detail" id="{s["id"]}">
  <div>
    <h2>{s["nom"]}</h2>
    <p>{d["intro"]}</p>
    <ul>{li}</ul>
    <p><strong>Idéal pour :</strong> {d["ideal"]}</p>
    {media_html(d["media2"])}
  </div>
  <div class="svc-aside">
    {media_html(d["media"])}
    <div class="price-note">
      <h3>Prix</h3>
      <p class="price-from">À partir de <strong>{s["prix"]}&nbsp;$</strong></p>
      <p>{d["prixnote"]}</p>
      <a class="btn" href="contact.html?service={s["id"]}">Demander un prix</a>
    </div>
  </div>
</article>''')
svc_faq = [
 ("Quand faut-il refaire le calfeutrage?", "En général aux 8 à 12 ans, ou dès qu'un joint fendille, décolle ou durcit. On le refait aussi toujours avant de repeindre un revêtement."),
 ("Peut-on peindre un revêtement de vinyle ou d'aluminium?", "Oui, avec une préparation et une peinture conçues pour ces surfaces. On vous conseille une teinte adaptée pour éviter la déformation du vinyle au soleil."),
 ("Quelle est la meilleure période pour peindre l'extérieur?", "De la fin du printemps au début de l'automne, quand il fait plus de 10 °C le jour comme la nuit et que le temps est sec."),
 ("Le lavage à pression abîme-t-il la brique?", "Pas quand la pression et la buse sont ajustées. On adapte la méthode à l'âge de la brique et à l'état des joints de mortier."),
 ("Êtes-vous licenciés et assurés?", "Oui, Groupe Murco détient sa licence de la Régie du bâtiment du Québec (RBQ)."),
 ("La soumission est-elle gratuite?", "Oui. On mesure sur place et on vous envoie un prix écrit, sans engagement."),
]
services_main = page_head('photos/metiers/entete-peinture', 'Nos services', "Trois métiers, un seul entrepreneur licencié RBQ. <a href=\"estimation.html\">Estimez votre prix en 30 secondes</a>.",
    '\n    <nav class="svc-nav" aria-label="Liste des services">' + ''.join(f'<a href="#{s["id"]}">{s["nom"]}</a>' for s in SVC) + '<a href="#couleurs">Essayer une couleur</a></nav>') + \
    '<section class="section" style="padding-top:2rem">\n  <div class="wrap">' + '\n'.join(arts) + '</div>\n</section>\n' + SIMULATEUR + \
    '''<section class="section est-teaser">
  <div class="wrap est-teaser-inner">
    <div><h2>Combien ça coûte?</h2><p>Faites une estimation en ligne en 30 secondes, sans donner vos coordonnées.</p></div>
    <a class="btn" href="estimation.html">Estimer mon prix</a>
  </div>
</section>
''' + faq_block(svc_faq) + cta_band()
pages['services.html'] = head('services.html', 'Services : calfeutrage, peinture extérieure, lavage de brique | Groupe Murco',
    'Calfeutrage de fenêtres et de portes, peinture de revêtement extérieur et lavage de brique à pression sur la Rive-Sud. Entrepreneur licencié RBQ.') + services_main + foot('services.html')

# ===================== VILLES =====================
LEADS = {
 'sherrington': "C'est chez nous. À Sherrington, on calfeutre, on repeint et on lave la brique des maisons de nos voisins, sans frais de déplacement.",
 'napierville': "Napierville est à quelques minutes de notre base. Calfeutrage, peinture de revêtement et lavage de brique pour les maisons, plex et commerces.",
 'saint-remi': "À Saint-Rémi, beaucoup de maisons ont un revêtement de bois ou de brique qui mérite un coup de neuf. On s'en occupe de A à Z.",
 'chateauguay': "À Châteauguay, on travaille autant sur les bungalows de brique que sur les maisons à étages en vinyle ou en bois.",
 'la-prairie': "À La Prairie, du Vieux-La Prairie aux quartiers récents, on refait les joints, on repeint et on lave la brique proprement.",
 'candiac': "À Candiac, on entretient des maisons récentes comme des propriétés établies : joints de fenêtres, peinture de revêtement et brique.",
}
CTA_VILLE = "Dites-nous ce qu'il y a à faire, on vous revient avec un prix écrit."
for sl, nom in VILLES:
    tiles = ''.join(f'<a class="job-tile" href="services.html#{s["id"]}"><img src="photos/villes/{sl}-{s["id"]}.jpg" width="800" height="600" loading="lazy" alt="{s["nom"]}"><span>{s["court"]}</span></a>' for s in SVC)
    qa = [
     (f"Vous déplacez-vous partout à {nom}?", f"Oui. Nous travaillons partout à {nom} et dans les environs, pour les maisons, les plex et les petits commerces."),
     (f"Combien coûte le calfeutrage d'une maison à {nom}?", "Le prix dépend du nombre de fenêtres et de portes et de la longueur des joints. Comptez à partir de 350 $; vous recevez une soumission écrite et gratuite avant les travaux."),
     ("Quand repeindre un revêtement extérieur?", "Dès que la peinture pèle, farine au toucher ou a pâli au soleil. La meilleure période va de la fin du printemps au début de l'automne."),
     ("Pouvez-vous combiner plusieurs travaux?", "Oui. On calfeutre souvent avant de peindre, et on lave la brique dans la même visite : une seule soumission, un seul chantier."),
    ]
    others = ''.join(f'<a href="{vurl(o)}">{n}</a>' for o, n in VILLES if o != sl)
    main = page_head(f'photos/metiers/{["entete-brique","entete-calfeutrage","entete-peinture","entete-brique-2","entete-calfeutrage","entete-peinture"][[v for v,_ in VILLES].index(sl)]}',
        f'Calfeutrage, peinture et brique à {nom}', LEADS[sl],
        f'\n    <div class="hero-actions">\n      <a class="btn" href="contact.html">Demander une soumission</a>\n      <a class="btn btn-ghost" href="tel:{TELH}">{PHONE_SVG} {TEL}</a>\n    </div>') + f'''
<section class="section city-jobs">
  <div class="wrap">
    <div class="section-head">
      <h2>Nos services à {nom}</h2>
      <p>Calfeutrage, peinture de revêtement et lavage de brique : un seul entrepreneur pour l'extérieur de votre maison.</p>
    </div>
    <div class="job-grid job-grid-3">{tiles}</div>
    <p class="photo-note">Photos d'illustration.</p>
  </div>
</section>

<section class="section section-mist">
  <div class="wrap">
    <div class="section-head">
      <h2>Du joint jusqu'à la façade</h2>
      <p>Une seule soumission pour plusieurs travaux.</p>
    </div>
    {svc_cards(f'Vous êtes à {nom}?', CTA_VILLE)}
  </div>
</section>
''' + faq_block(qa, f'Questions fréquentes à {nom}', 'section') + f'''
<section class="section section-mist">
  <div class="wrap">
    <div class="section-head">
      <h2>Les autres villes que nous desservons</h2>
    </div>
    <nav class="svc-nav" aria-label="Autres villes">{others}</nav>
  </div>
</section>
<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@type": "Service", "serviceType": "Calfeutrage et peinture extérieure", "provider": {"@type": "HomeAndConstructionBusiness", "name": "Groupe Murco", "telephone": TELH, "url": SITE}, "areaServed": {"@type": "City", "name": nom, "addressRegion": "QC", "addressCountry": "CA"}}, ensure_ascii=False)}</script>
''' + cta_band()
    f = vurl(sl)
    pages[f] = head(f, f'Calfeutrage et peinture extérieure à {nom} | Groupe Murco',
        f'Calfeutrage de fenêtres, peinture de revêtement extérieur et lavage de brique à {nom}. Entrepreneur licencié RBQ basé à Sherrington. Soumission gratuite.') + main + foot(f)

# ===================== PAGES CONSERVÉES (contenu principal repris) =====================
def keep_main(fname):
    s = open(fname, encoding='utf-8').read()
    return s[s.index('<main id="contenu">') + len('<main id="contenu">\n'):s.index('</main>')]

def svc_checks():
    return '<div class="checks">' + ''.join(f'<label><input type="checkbox" name="services" value="{s["nom"]}" data-svc="{s["id"]}"> <span>{s["nom"]}</span></label>' for s in SVC) + '</div>'

# Contact
m = keep_main('contact.html')
m = re.sub(r'<div class="checks">.*?</div>', svc_checks(), m, count=1, flags=re.S)
m = m.replace("Ex. maison de 2 étages, environ 120 pieds de gouttières, beaucoup d'arbres autour.", "Ex. 14 fenêtres à calfeutrer, revêtement de bois à repeindre en gris, façade de brique côté rue.")
m = re.sub(r'<picture class="head-img">.*?</picture>', '<picture class="head-img"><source media="(max-width: 900px)" srcset="photos/maquette/entete-maison-soir-1100.jpg"><img src="photos/maquette/entete-maison-soir.jpg" alt="" width="1920" height="620"></picture>', m, count=1, flags=re.S)
m = m.replace("avec une photo de vos gouttières, c'est souvent le plus rapide.", "avec une photo de votre maison, c'est souvent le plus rapide.")
m = re.sub(r'<p>Sherrington, Napierville.*?</p>', '<p>Sherrington, Napierville, Saint-Rémi, Châteauguay, La Prairie, Candiac et les environs. Maisons, plex et petits commerces.</p>', m, count=1, flags=re.S)
pages['contact.html'] = head('contact.html', 'Soumission gratuite | Groupe Murco', 'Demandez une soumission gratuite pour du calfeutrage, de la peinture extérieure ou du lavage de brique. Sherrington et Rive-Sud.') + m + foot('contact.html')

# Avis
m = keep_main('avis.html')
m = re.sub(r'(<select id="a-service" name="service">).*?(</select>)', lambda x: x.group(1) + '<option value="">Choisir</option>' + ''.join(f'<option>{s["nom"]}</option>' for s in SVC) + x.group(2), m, count=1, flags=re.S)
pages['avis.html'] = head('avis.html', 'Avis clients | Groupe Murco', 'Avis de clients de Groupe Murco : calfeutrage, peinture extérieure et lavage de brique sur la Rive-Sud.') + m + foot('avis.html', '<script src="assets/avis.js"></script>\n')

# À propos
m = keep_main('a-propos.html')
m = m.replace("Groupe Murco, c'est Samuel Michea et le souci du travail bien fait, du toit jusqu'au terrain.", "Groupe Murco, c'est Samuel Michea, une licence RBQ et le souci du travail bien fait, du joint de fenêtre jusqu'à la façade.")
m = re.sub(r'<p>Des années sur les échafauds.*?</p>', "<p>Des années sur les échafauds et les échelles lui ont appris qu'une maison se protège par ses détails : un joint bien scellé, une peinture bien préparée, une brique propre qui respire. C'est ce travail-là que Groupe Murco offre aux propriétaires de la Rive-Sud.</p>", m, count=1, flags=re.S)
m = m.replace('<p class="legal-line">Groupe Murco est une dénomination de 9568-5590 Québec inc.</p>', '<p class="legal-line">Groupe Murco est une dénomination de 9568-5590 Québec inc., entrepreneur détenteur d\'une licence de la Régie du bâtiment du Québec (RBQ)<span data-rbq-num></span>.</p>')
m = m.replace('<li><strong>Un terrain propre</strong>Feuilles, boue et débris repartent avec nous.</li>', '<li><strong>Un chantier propre</strong>Bâches, ruban et nettoyage chaque jour, avant de partir.</li>')
m = m.replace('<li><strong>Un prix clair</strong>', '<li><strong>Licence RBQ</strong>Une entreprise en règle, avec une garantie écrite.</li>\n        <li><strong>Un prix clair</strong>')
m = re.sub(r'data-photo="[^"]*" data-alt="[^"]*"', 'data-photo="photos/metiers/peinture-1.jpg" data-alt="Peintre en nacelle sur un mur extérieur"', m, count=1)
m = re.sub(r'<picture class="head-img">.*?</picture>', '<picture class="head-img"><source media="(max-width: 900px)" srcset="photos/metiers/entete-brique-1100.jpg"><img src="photos/metiers/entete-brique.jpg" alt="" width="1920" height="620"></picture>', m, count=1, flags=re.S)
m = re.sub(r'<section class="cta-band has-photo">.*?</section>', cta_band().strip(), m, count=1, flags=re.S)
pages['a-propos.html'] = head('a-propos.html', 'À propos | Groupe Murco, Sherrington', 'Groupe Murco : entrepreneur licencié RBQ de Sherrington en calfeutrage, peinture extérieure et lavage de brique. Fondé par Samuel Michea.') + m + foot('a-propos.html')

# Estimation (calculateur)
m = keep_main('estimation.html')
rows = [('calfeutrage', 'Calfeutrage (fenêtres et portes)', 12, 1, 'ouvertures', 'Nombre de fenêtres et de portes', True),
        ('peinture', 'Peinture de revêtement extérieur', 1200, 100, 'pi² de revêtement', 'Pieds carrés de revêtement', False),
        ('brique', 'Lavage de brique à pression', 800, 100, 'pi² de brique', 'Pieds carrés de brique', False)]
rowh = ''.join(f'<div class="calc-row" data-svc-row="{k}"><label><input type="checkbox"{" checked" if c else ""}> <span>{t}</span></label><div class="calc-qty"><input type="number" min="0" step="{st}" value="{v}" inputmode="numeric" aria-label="{al}"><small>{u}</small></div></div>' for k, t, v, st, u, al, c in rows)
m = re.sub(r'(<div class="field"><label for="k-etages">.*?</div>)\s*(<div class="calc-row".*?)(\s*</div>\s*<aside class="calc-result")', lambda x: x.group(1) + '\n        ' + rowh + x.group(3), m, count=1, flags=re.S)
m = re.sub(r'<div class="est-tips">.*?</div>\s*</div>\s*</section>', '''<div class="est-tips">
      <div class="est-tip"><h3>Fenêtres et portes</h3><p>Comptez chaque fenêtre et chaque porte extérieure. Une porte-fenêtre ou une porte de garage compte pour deux.</p></div>
      <div class="est-tip"><h3>Pieds carrés de revêtement</h3><p>Largeur × hauteur de chaque mur à peindre, moins les grandes ouvertures. Une maison à étages fait souvent de 1 200 à 2 000 pi².</p></div>
      <div class="est-tip"><h3>Pieds carrés de brique</h3><p>Souvent seulement la façade : comptez environ 300 à 600 pi² pour un bungalow, le double pour une maison à étages.</p></div>
      <div class="est-tip"><h3>Pas sûr de vos mesures?</h3><p>Envoyez une estimation approximative : on mesure toujours sur place avant de confirmer le prix.</p></div>
    </div>
  </div>
</section>''', m, count=1, flags=re.S)
m = m.replace('photos/maquette/entete-maison-soir', 'photos/metiers/entete-calfeutrage', 1)
pages['estimation.html'] = head('estimation.html', 'Estimation de prix en ligne | Groupe Murco', 'Estimez en 30 secondes le prix de votre calfeutrage, de votre peinture extérieure ou de votre lavage de brique. Sherrington et Rive-Sud.') + m + foot('estimation.html')

# Merci, confidentialité, 404
for f, t, d, extra in [('merci.html', 'Merci | Groupe Murco', 'Merci, nous avons bien reçu votre message.', dict(noindex=True, canonical=False)),
                       ('confidentialite.html', 'Politique de confidentialité | Groupe Murco', 'Comment Groupe Murco protège vos renseignements personnels.', {}),
                       ('404.html', 'Page introuvable | Groupe Murco', 'Cette page est introuvable.', dict(noindex=True, canonical=False))]:
    m = keep_main(f)
    m = m.replace('photos/entete-page', 'photos/metiers/entete-calfeutrage').replace('/photos/entete-page', '/photos/metiers/entete-calfeutrage')
    m = m.replace('Mesuré au pied, au pied carré ou à la fenêtre.', "Mesuré sur place, détaillé par travaux.")
    pages[f] = head(f, t, d, **extra) + m + foot(f)

# Version des photos : change PHOTOS_V quand tu remplaces une photo par une autre du même nom,
# pour que les navigateurs qui ont gardé l'ancienne en mémoire chargent la nouvelle.
PHOTOS_V = '3'
for f, s in pages.items():
    s = re.sub(r'(photos/[A-Za-z0-9_\-/]+\.(?:jpg|jpeg|png|webp|svg))(\?v=\w+)?', r'\1?v=' + PHOTOS_V, s)
    open(f, 'w', encoding='utf-8').write(s)
print('pages écrites :', len(pages))
