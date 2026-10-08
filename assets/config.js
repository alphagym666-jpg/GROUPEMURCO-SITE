// ============================================================
//  CONFIGURATION DU SITE — Groupe Murco
//  Modifie seulement les valeurs entre guillemets ou les nombres.
// ============================================================

// ---- Calculateur de prix (page Services) ----
// À CONFIRMER : ce sont des valeurs de départ pour la maquette.
// "min" = prix minimum facturé ; l'estimation affichée est une fourchette.
const PRIX = {
  calfeutrage: { unite: "ouverture",          taux: 40,   min: 350 },   // par fenêtre ou porte
  peinture:    { unite: "pied carré",         taux: 2.75, min: 2500 },  // revêtement peint
  // brique:   { unite: "pied carré",         taux: 0.60, min: 400 },   // lavage de brique : désactivé pour le moment
  // Multiplicateur selon la hauteur de la maison
  etages: { 1: 1.00, 2: 1.15, 3: 1.35 }
};

// ---- Badges de confiance ----
// Laisse "" tant que tu n'as pas l'info : le badge ne s'affiche pas.
const NUMERO_RBQ = "5885-4050"; // ton numéro de licence RBQ
const ASSURANCE = "";           // ex. "Assuré responsabilité civile 2 M$"

// ---- Suivi des visites (pour tes pubs) ----
// Laisse "" pour désactiver. Une bannière de consentement (Loi 25)
// s'affiche automatiquement dès qu'un identifiant est rempli.
const GOOGLE_ANALYTICS_ID = ""; // ex. "G-XXXXXXXXXX"
const META_PIXEL_ID = "";       // ex. "123456789012345"
