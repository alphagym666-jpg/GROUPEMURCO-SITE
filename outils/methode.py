# -*- coding: utf-8 -*-
"""Méthode de travail étape par étape : texte unique, utilisé par la page Services et l'accueil.
Pour changer une étape, modifie ce fichier puis relance l'outil de construction (ou dis-le à Claude).
Étiquette « sauté » = étape qu'on laisse souvent tomber quand on veut aller vite."""
import html as H

METHODES = {
 'calfeutrage': dict(
   nom='Calfeutrage', titre='Calfeutrage : étape par étape',
   intro="Un joint de calfeutrage ne dure que si chaque étape est faite dans l'ordre. Voici exactement comment on procède.",
   pied="Un joint qui décolle à cause de notre application : on revient le corriger, sans frais, pendant deux ans.",
   etapes=[
    ("Inspection de tous les joints", "On fait le tour de la maison : fenêtres, portes, coins de revêtement, solins, passages de fils. On note chaque joint fendillé, décollé ou durci.", False),
    ("Protection des surfaces", "Ruban de masquage de chaque côté du joint : la ligne sort parfaitement droite et votre revêtement reste propre.", False),
    ("Retrait complet du vieux scellant", "On enlève l'ancien joint au complet, jusqu'à la brique ou au cadre. Calfeutrer par-dessus du vieux scellant, c'est la meilleure façon de le voir décoller.", True),
    ("Nettoyage et séchage", "Brossage, dépoussiérage et dégraissage. Un scellant n'adhère que sur une surface propre et sèche.", False),
    ("Fond de joint dans les joints profonds", "On insère un cordon de mousse au fond du joint. Le scellant travaille mieux, fait moins de fissures et dure plus longtemps.", True),
    ("Scellant extérieur haute performance", "Application au pistolet en un seul passage continu, avec un scellant de qualité extérieure, de la couleur de vos cadres.", False),
    ("Lissage et finition", "Le joint est lissé à l'outil pour bien pousser le scellant dans le joint et obtenir une surface nette et étanche. Le ruban est retiré au bon moment.", False),
    ("Nettoyage et inspection finale", "On ramasse tout, on repasse chaque joint avec vous et on s'assure que rien n'a été oublié.", False),
   ]),
 'peinture': dict(
   nom='Peinture extérieure', titre='Peinture de revêtement : étape par étape',
   intro="Une peinture extérieure dure aussi longtemps que sa préparation. C'est pour ça que la peinture elle-même vient presque à la fin.",
   pied="Une peinture qui pèle à cause de notre application : on revient la corriger, sans frais, pendant deux ans.",
   etapes=[
    ("Visite et soumission écrite", "On mesure sur place, on regarde l'état du revêtement et on vous remet un prix écrit et détaillé, sans surprise.", False),
    ("Choix de la couleur et du produit", "On vous conseille une teinte et une peinture adaptées à votre revêtement : bois, vinyle, aluminium ou fibrociment.", False),
    ("Protection du chantier", "Fenêtres, portes, luminaires, plantes et terrasse sont couverts. Votre maison reste propre.", False),
    ("Lavage du revêtement", "On enlève la saleté, la mousse et la poudre de l'ancienne peinture. La peinture tient sur une surface propre.", False),
    ("Grattage, sablage et réparations", "On gratte ce qui lève, on sable et on répare le bois abîmé avant de peindre.", True),
    ("Calfeutrage des joints", "Les joints fissurés sont refaits avant la peinture, pour que l'eau reste dehors.", False),
    ("Apprêt adapté à la surface", "Un apprêt choisi pour votre revêtement fait adhérer la peinture et uniformise la couleur.", True),
    ("Deux couches de finition", "Au pistolet airless ou au rouleau selon la surface, avec le temps de séchage nécessaire entre les couches.", False),
    ("Retouches, nettoyage et inspection", "On inspecte la façade avec vous, on fait les retouches, on retire toutes les protections et on nettoie le terrain.", False),
   ]),
 'brique': dict(
   nom='Lavage de brique', titre='Lavage de brique : étape par étape',
   intro="La brique se lave, elle ne se décape pas. Chaque étape sert à nettoyer à fond sans abîmer la brique ni le mortier.",
   pied="",
   etapes=[
    ("Inspection de la brique", "On évalue l'état de la brique et du mortier, et on repère ce qu'il faut enlever : mousse, efflorescence blanche, coulisses noires ou rouille.", False),
    ("Test sur une petite zone", "Avant de laver la façade, on essaie le nettoyant et la pression à un endroit discret. Chaque brique réagit différemment.", True),
    ("Protection", "Fenêtres, portes, prises électriques, plantes et aménagements sont protégés avant de commencer.", False),
    ("Pré-mouillage et nettoyant adapté", "On mouille la brique, puis on applique le nettoyant choisi selon la tache : mousse, efflorescence ou rouille.", False),
    ("Temps de contact et brossage", "Le nettoyant travaille le temps qu'il faut. Les endroits tenaces sont brossés à la main.", False),
    ("Lavage à pression contrôlée", "Pression et buse ajustées à la brique et au mortier. Trop fort, on mange les joints : on lave sans abîmer.", True),
    ("Rinçage complet", "On rince toute la façade et le terrain, de haut en bas, pour ne laisser aucun résidu.", False),
    ("Inspection des joints de mortier", "On vous signale les joints de mortier à réparer. En option : scellant hydrofuge une fois la brique sèche.", False),
    ("Nettoyage final et inspection", "On retire les protections, on nettoie le terrain et on regarde le résultat avec vous.", False),
   ]),
}
ORDRE = ['calfeutrage', 'peinture']   # + 'brique' quand le lavage de brique reviendra (le texte est prêt plus haut)
LEGENDE = "L'étiquette « Souvent sauté » marque les étapes qu'on laisse facilement tomber quand on veut aller vite."

def etapes_html(k):
    out = []
    for i, (t, p, saute) in enumerate(METHODES[k]['etapes'], 1):
        tag = '<span class="ps-tag">Souvent sauté</span>' if saute else ''
        out.append(f'<li><span class="ps-n" aria-hidden="true">{i}</span><div><h4>{H.escape(t)}</h4><p>{H.escape(p)}</p>{tag}</div></li>')
    return '<ol class="process-steps">' + ''.join(out) + '</ol>'

def bloc_service(k):
    m = METHODES[k]
    pied = f'<p class="process-foot"><strong>Garantie 2 ans.</strong> {H.escape(m["pied"])}</p>' if m['pied'] else ''
    return (f'<div class="process" id="methode-{k}">\n'
            f'  <div class="process-head"><p class="eyebrow"><b>✓</b> Notre méthode</p><h3>{H.escape(m["titre"])}</h3>'
            f'<p class="process-lead">{H.escape(m["intro"])}</p><p class="process-legend">{H.escape(LEGENDE)}</p></div>\n'
            f'  {etapes_html(k)}\n  {pied}\n</div>')

def tabs_html():
    tabs, panels = [], []
    for j, k in enumerate(ORDRE):
        sel = 'true' if j == 0 else 'false'
        tabs.append(f'<button type="button" role="tab" id="pt-{k}" aria-selected="{sel}" aria-controls="pp-{k}" tabindex="{0 if j == 0 else -1}">{H.escape(METHODES[k]["nom"])}</button>')
        panels.append(f'<div class="ptabs-panel" role="tabpanel" id="pp-{k}" aria-labelledby="pt-{k}">{etapes_html(k)}'
                      f'<p class="ptabs-more"><a class="btn btn-ghost" href="services.html#methode-{k}">Voir le détail du {H.escape(METHODES[k]["nom"].lower())}</a></p></div>')
    return ('<section class="section process-section bead-top" id="methode" aria-labelledby="methode-titre">\n  <div class="wrap">\n'
            '    <div class="section-head center">\n      <p class="eyebrow"><b>✓</b> Notre méthode</p>\n'
            '      <h2 id="methode-titre">Pas du bricolage : une méthode, étape par étape</h2>\n'
            "      <p>Chaque travail suit les mêmes étapes, dans le même ordre. C'est ce qui fait qu'un joint tient, qu'une peinture dure et qu'une brique redevient belle.</p>\n    </div>\n"
            f'    <div class="ptabs" data-ptabs>\n      <div class="ptabs-list" role="tablist" aria-label="Choisir un métier">{"".join(tabs)}</div>\n      {"".join(panels)}\n'
            f'      <p class="process-legend center">{H.escape(LEGENDE)}</p>\n    </div>\n  </div>\n</section>\n')
