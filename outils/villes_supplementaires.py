# -*- coding: utf-8 -*-
"""Crée les pages des grandes villes à partir de la page de Candiac (déjà nettoyée),
avec un texte propre à chaque ville. À lancer depuis le dossier du site :
    python3 outils/villes_supplementaires.py
Les photos sont des photos d'illustration d'autres villes : remplace-les par tes jobs
(photos/villes/<ville>-calfeutrage.jpg et -peinture.jpg) quand tu les as."""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import retirer_brique as RB

SITE = 'https://groupemurco.com/'
# slug, nom affiché, photos de remplacement (slug existant), image d'en-tête, texte d'intro unique
VILLES = [
 ('longueuil', 'Longueuil', 'napierville', 'entete-calfeutrage',
  "À Longueuil, on calfeutre et on repeint des maisons de tous les âges, des bungalows aux maisons à étages. Un joint refait à temps évite l'eau, l'air froid et les mauvaises surprises au dégel."),
 ('brossard', 'Brossard', 'la-prairie', 'entete-peinture',
  "À Brossard, on s'occupe de l'extérieur de votre maison : joints de fenêtres et de portes refaits au complet, et peinture de revêtement bien préparée."),
 ('boucherville', 'Boucherville', 'saint-remi', 'entete-calfeutrage',
  "À Boucherville, des joints propres et un revêtement bien peint font toute la différence : on refait l'extérieur de votre maison, étape par étape, avec une soumission écrite."),
 ('saint-jean-sur-richelieu', 'Saint-Jean-sur-Richelieu', 'chateauguay', 'entete-peinture',
  "À Saint-Jean-sur-Richelieu, on calfeutre les fenêtres et les portes et on repeint les revêtements de bois, de vinyle ou d'aluminium. Même méthode, même qualité qu'à Sherrington."),
 ('valleyfield', 'Salaberry-de-Valleyfield', 'sherrington', 'entete-calfeutrage',
  "On se déplace à Salaberry-de-Valleyfield pour le calfeutrage et la peinture extérieure. Appelez-nous : on regroupe les travaux pour que le déplacement vaille la peine."),
 ('granby', 'Granby', 'candiac', 'entete-peinture',
  "On se rend aussi dans les Cantons-de-l'Est, à Granby et aux alentours, pour le calfeutrage et la peinture de revêtement extérieur. Appelez-nous pour planifier la visite."),
]
# Questions générales, tournées d'une page à l'autre pour que chaque ville ait son propre contenu
QR = [
 ("Quand faut-il refaire le calfeutrage?", "En général aux 8 à 12 ans, ou dès qu'un joint fendille, décolle ou durcit. On le refait aussi toujours avant de repeindre un revêtement."),
 ("Pourquoi enlever le vieux calfeutrage au lieu de passer par-dessus?", "Un nouveau scellant n'adhère pas bien à un vieux joint qui travaille. On enlève tout jusqu'à la brique ou au cadre, on nettoie, puis on refait le joint : il dure beaucoup plus longtemps."),
 ("Peut-on calfeutrer l'hiver?", "Oui, avec un scellant adapté au froid et une surface propre et sèche. On choisit le produit selon la météo du jour; appelez-nous pour valider votre cas."),
 ("Combien de temps dure une peinture de revêtement?", "Bien préparée (lavage, grattage, apprêt, deux couches), une peinture extérieure tient plusieurs années. La préparation compte autant que la peinture."),
 ("Est-ce que vous protégez mon terrain pendant les travaux?", "Oui. Fenêtres, portes, plantes et terrasse sont protégés, et on nettoie le chantier chaque jour."),
 ("Comment se passe la soumission?", "On mesure sur place, gratuitement, puis on vous remet un prix écrit et détaillé. Aucun engagement."),
 ("Le calfeutrage fait-il vraiment économiser du chauffage?", "Des joints étanches limitent les infiltrations d'air froid autour des fenêtres et des portes. Vous sentez la différence aux endroits qui laissaient passer le courant d'air."),
 ("Faites-vous les deux travaux dans la même visite?", "Oui. On calfeutre toujours avant de peindre, dans la même visite : une seule soumission, un seul chantier."),
]
COMMUN = [
 lambda v: (f"Vous déplacez-vous partout à {v}?", f"Oui. Nous travaillons partout à {v} et dans les environs, pour les maisons, les plex et les petits commerces."),
 lambda v: (f"Combien coûte le calfeutrage d'une maison à {v}?", "Le prix dépend du nombre de fenêtres et de portes et de la longueur des joints. Comptez à partir de 350 $; vous recevez une soumission écrite et gratuite avant les travaux."),
]

def esc(t): return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

def main():
    src = RB.retirer(open('calfeutrage-peinture-candiac.html', encoding='utf-8').read())
    sm = open('sitemap.xml', encoding='utf-8').read()
    for idx, (slug, nom, ph, head, intro) in enumerate(VILLES):
        s, pied = src.split('<footer', 1)   # le pied de page reste identique d'une page à l'autre
        s = s.replace('calfeutrage-peinture-candiac.html', f'calfeutrage-peinture-{slug}.html')
        s = s.replace('photos/villes/candiac-', f'photos/villes/{ph}-')
        s = s.replace('photos/metiers/entete-peinture-1100.jpg', f'photos/metiers/{head}-1100.jpg').replace('photos/metiers/entete-peinture.jpg', f'photos/metiers/{head}.jpg')
        s = re.sub(r'(<p class="lead">).*?(</p>)', lambda m: m.group(1) + esc(intro).replace('&#x27;', "'") + m.group(2), s, count=1, flags=re.S)
        # FAQ : 2 questions communes + 2 propres à la ville (tournent d'une ville à l'autre)
        qa = [f(nom) for f in COMMUN] + [QR[(idx * 2 + k) % len(QR)] for k in range(2)]
        faq = ''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in qa)
        s = re.sub(r'<div class="faq">.*?</div>\n', '<div class="faq">' + faq + '</div>\n', s, count=1, flags=re.S)
        import json
        ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa]}
        s = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "FAQPage".*?</script>', '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>', s, count=1, flags=re.S)
        s = s.replace('Candiac', nom)
        s = s + '<footer' + pied
        out = f'calfeutrage-peinture-{slug}.html'
        open(out, 'w', encoding='utf-8').write(s)
        entry = f'  <url><loc>{SITE}{out}</loc><lastmod>2026-10-08</lastmod></url>\n'
        if out not in sm: sm = sm.replace('</urlset>', entry + '</urlset>')
        print('page créée :', out)
    open('sitemap.xml', 'w', encoding='utf-8').write(sm)

if __name__ == '__main__': main()
