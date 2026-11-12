// Données Moveo 59.
// Les valeurs marquées « À CONFIRMER » sont des emplacements à compléter.

const AGENCES = [
  {
    id: "bruay-sur-escaut",
    ville: "Bruay-sur-l'Escaut",
    pays: "France",
    nom: "Moveo 59 Bruay-sur-l'Escaut",
    adresse: "ADRESSE À CONFIRMER, 59860 Bruay-sur-l'Escaut",
    horaires: "À CONFIRMER",
    telephone: "À CONFIRMER",
    aeroport: false,
    gare: false
  }
];

// Catégories : "mini", "citadine", "compacte"
const VEHICULES = [
  {
    id: "opel-corsa-2021",
    marque: "Opel",
    modele: "Corsa",
    annee: 2021,
    categorie: "citadine",
    transmission: "manuelle",    // À CONFIRMER
    places: 5,
    portes: 5,
    carburant: "essence",        // À CONFIRMER
    prixJour: 35,                // À CONFIRMER (tarif indicatif)
    couleur: "#0ea5e9"
  }
];

const OPTIONS = [
  { id: "assurance-plus", nom: "Protection étendue", description: "Réduit votre franchise à 0 €.", prixJour: 12 },
  { id: "siege-enfant", nom: "Siège enfant", description: "Siège homologué, de 9 à 36 kg.", prixJour: 6 },
  { id: "conducteur-supp", nom: "Conducteur supplémentaire", description: "Ajoute un second conducteur désigné.", prixJour: 5 }
];

const FRAIS_RETOUR_AUTRE_AGENCE = 45; // forfait en euros
