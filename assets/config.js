// ============================================================
//  CONFIGURATION DU SITE — Groupe Murco
//  Modifie seulement les valeurs entre guillemets ou les nombres.
// ============================================================

// ---- Calculateur de prix (page Services) ----
// À CONFIRMER : ce sont des valeurs de départ pour la maquette.
// "min" = prix minimum facturé ; l'estimation affichée est une fourchette.
const PRIX = {
  gouttieres: { unite: "pied linéaire", taux: 2.00, min: 200 },
  protege:    { unite: "pied linéaire", taux: 9.00, min: 650 },
  pression:   { unite: "pied carré",    taux: 0.30, min: 250 },
  vitres:     { unite: "fenêtre",       taux: 12,   min: 150 },
  feuilles:   { unite: "pied carré",    taux: 0.04, min: 175 },
  // Multiplicateur selon la hauteur de la maison
  etages: { 1: 1.00, 2: 1.15, 3: 1.35 }
};

// ---- Badges de confiance ----
// Laisse "" tant que tu n'as pas l'info : le badge ne s'affiche pas.
const NUMERO_RBQ = "";          // ex. "5812-3456-01"
const ASSURANCE = "";           // ex. "Assuré responsabilité civile 2 M$"

// ---- Suivi des visites (pour tes pubs) ----
// Laisse "" pour désactiver. Une bannière de consentement (Loi 25)
// s'affiche automatiquement dès qu'un identifiant est rempli.
const GOOGLE_ANALYTICS_ID = ""; // ex. "G-XXXXXXXXXX"
const META_PIXEL_ID = "";       // ex. "123456789012345"
