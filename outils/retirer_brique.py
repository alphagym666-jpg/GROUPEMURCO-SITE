# -*- coding: utf-8 -*-
"""Retire le « lavage de brique à pression » du site (pour le moment : l'accent est sur
le calfeutrage, puis la peinture extérieure résidentielle).
Idempotent : on peut l'appliquer plusieurs fois. Le générateur l'appelle avant d'écrire les pages.
Pour remettre le lavage de brique plus tard : `git log --oneline` puis retourner à la version
« avant le retrait du lavage de brique » (voir lisez-moi.txt)."""
import re

TEXTES = [
 ("Calfeutrage, peinture extérieure et lavage de brique, Rive-Sud", "Calfeutrage et peinture extérieure, Rive-Sud"),
 ("calfeutrage de fenêtres et de portes, peinture de revêtement extérieur et lavage de brique à pression sur", "calfeutrage de fenêtres et de portes et peinture de revêtement extérieur sur"),
 ("calfeutrage, peinture de revêtement extérieur et lavage de brique à pression sur", "calfeutrage et peinture de revêtement extérieur sur"),
 ("Calfeutrage de fenêtres et de portes, peinture de revêtement extérieur et lavage de brique à pression sur", "Calfeutrage de fenêtres et de portes et peinture de revêtement extérieur sur"),
 ("Calfeutrage, peinture extérieure et lavage de brique à Sherrington,", "Calfeutrage et peinture extérieure à Sherrington,"),
 ("calfeutrage, peinture extérieure et lavage de brique. Fondé", "calfeutrage et peinture extérieure. Fondé"),
 ("calfeutrage, peinture extérieure et lavage de brique sur la Rive-Sud", "calfeutrage et peinture extérieure sur la Rive-Sud"),
 ("Services : calfeutrage, peinture extérieure, lavage de brique | Groupe Murco", "Services : calfeutrage et peinture extérieure | Groupe Murco"),
 ("du calfeutrage, de la peinture extérieure ou du lavage de brique.", "du calfeutrage ou de la peinture extérieure."),
 ("votre calfeutrage, de votre peinture extérieure ou de votre lavage de brique.", "votre calfeutrage ou de votre peinture extérieure."),
 ("Calfeutrage, peinture et brique, faits comme il faut.", "Calfeutrage et peinture extérieure, faits comme il faut."),
 ("Calfeutrage, peinture et brique peuvent se faire dans le même chantier : une seule soumission.", "Calfeutrage et peinture extérieure peuvent se faire dans le même chantier : une seule soumission."),
 ("Calfeutrage, peinture de revêtement et lavage de brique : un seul entrepreneur pour l'extérieur de votre maison.", "Calfeutrage et peinture de revêtement : un seul entrepreneur pour l'extérieur de votre maison."),
 ("Calfeutrage, peinture de revêtement et lavage de brique pour les maisons, plex et commerces.", "Calfeutrage et peinture de revêtement pour les maisons, plex et commerces."),
 ("joints de fenêtres, peinture de revêtement et brique.", "joints de fenêtres et peinture de revêtement."),
 ("on refait les joints, on repeint et on lave la brique proprement.", "on refait les joints et on repeint proprement."),
 ("on calfeutre, on repeint et on lave la brique des maisons de nos voisins", "on calfeutre et on repeint les maisons de nos voisins"),
 ("On calfeutre souvent avant de peindre, et on lave la brique dans la même visite : une seule soumission, un seul chantier.", "On calfeutre toujours avant de peindre, dans la même visite : une seule soumission, un seul chantier."),
 ("une peinture bien préparée, une brique propre qui respire.", "une peinture bien préparée, une maison qui reste étanche."),
 ("Un joint bien scellé, une peinture qui tient, une brique qui respire.", "Un joint bien scellé, une peinture qui tient, une maison qui reste étanche."),
 ("calfeutrage de fenêtres, peinture de revêtement extérieur et lavage de brique à ", "calfeutrage de fenêtres et peinture de revêtement extérieur à "),
 ("Calfeutrage de fenêtres, peinture de revêtement extérieur et lavage de brique à ", "Calfeutrage de fenêtres et peinture de revêtement extérieur à "),
 ("calfeutrage, peinture extérieure et lavage de brique à Sherrington, sur toute", "calfeutrage et peinture extérieure à Sherrington, sur toute"),
 ("qu'une peinture dure et qu'une brique redevient belle.", "qu'une peinture dure et que la maison reste protégée."),
 ("On lave la brique", "On protège la maison"),
 ('<span data-count="3">3</span></div><p>métiers de la construction, un seul entrepreneur.</p>', '<span data-count="2">2</span></div><p>métiers de l\'extérieur, un seul entrepreneur.</p>'),
]
H1 = re.compile(r'(<h1[^>]*>)Calfeutrage, peinture et brique à ([^<]+)(</h1>)')
STRUCT = [
 r'<li><a href="/?services\.html#brique">Lavage de brique à pression</a></li>',
 r'<a href="#brique">Lavage de brique à pression</a>',
 r',\s*\{"@type": "Offer", "itemOffered": \{"@type": "Service", "name": "Lavage de brique à pression"\}\}',
 r'<option>Lavage de brique à pression</option>',
 r'<label><input type="checkbox" name="services" value="Lavage de brique à pression" data-svc="brique">\s*<span>Lavage de brique à pression</span></label>',
 r'<div class="calc-row" data-svc-row="brique">.*?</div></div>',
 r'<div class="est-tip"><h3>Pieds carrés de brique</h3>.*?</div>',
 r'<a class="svc" href="services\.html#brique">.*?</a>(?=<div class="svc-cta">|\s*<div class="svc-cta">)',
 r'<a class="job-tile" href="services\.html#brique">.*?</a>',
 r'<span>Lavage de brique</span>',
 r'<section class="section brick-section[^"]*" id="brique-avant-apres">.*?</section>\n?',
 r'<article class="svc-detail" id="brique">.*?</article>\n?',
 r'<div class="process" id="methode-brique">.*?\n</div>\n?',
 r'<details><summary>Le lavage à pression abîme-t-il la brique\?</summary>.*?</details>',
 r',\s*\{"@type": "Question", "name": "Le lavage à pression abîme-t-il la brique\?", "acceptedAnswer": \{[^}]*\}\}',
 r'<button type="button" role="tab" id="pt-brique".*?</button>',
 r'<div class="ptabs-panel" role="tabpanel" id="pp-brique".*?<p class="ptabs-more">.*?</p></div>',
]

def retirer(s):
    for a, b in TEXTES: s = s.replace(a, b)
    s = H1.sub(lambda m: m.group(1) + 'Calfeutrage et peinture à ' + m.group(2) + m.group(3), s)
    for p in STRUCT: s = re.sub(p, '', s, flags=re.S)
    s = s.replace('svc-grid svc-grid-3', 'svc-grid svc-grid-2').replace('job-grid job-grid-3', 'job-grid job-grid-2')
    return s

if __name__ == '__main__':
    import glob, sys
    for f in glob.glob('*.html'):
        t = open(f, encoding='utf-8').read(); u = retirer(t)
        if u != t: open(f, 'w', encoding='utf-8').write(u); print('modifié :', f)
