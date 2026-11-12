// Données de démonstration Moveo 59.
// Remplacez ces valeurs par vos véritables agences, véhicules et tarifs.

const AGENCES = [
  { id: "paris-gare-lyon", ville: "Paris", pays: "France", nom: "Paris Gare de Lyon", adresse: "Place Louis-Armand, 75012 Paris", horaires: "7h00 – 21h00", telephone: "+33 1 00 00 00 01", aeroport: false, gare: true },
  { id: "paris-orly", ville: "Paris", pays: "France", nom: "Paris Orly Aéroport", adresse: "Aérogare Sud, 94390 Orly", horaires: "6h00 – 23h00", telephone: "+33 1 00 00 00 02", aeroport: true, gare: false },
  { id: "lyon-part-dieu", ville: "Lyon", pays: "France", nom: "Lyon Part-Dieu", adresse: "Centre commercial Part-Dieu, 69003 Lyon", horaires: "8h00 – 19h00", telephone: "+33 4 00 00 00 03", aeroport: false, gare: true },
  { id: "marseille-saint-charles", ville: "Marseille", pays: "France", nom: "Marseille Saint-Charles", adresse: "Place Victor-Hugo, 13001 Marseille", horaires: "7h30 – 20h00", telephone: "+33 4 00 00 00 04", aeroport: false, gare: true },
  { id: "bruxelles-midi", ville: "Bruxelles", pays: "Belgique", nom: "Bruxelles Midi", adresse: "Parvis de Saint-Gilles, 1060 Bruxelles", horaires: "7h00 – 20h00", telephone: "+32 2 000 00 05", aeroport: false, gare: true },
  { id: "amsterdam-centraal", ville: "Amsterdam", pays: "Pays-Bas", nom: "Amsterdam Centraal", adresse: "Stationsplein, 1012 AB Amsterdam", horaires: "7h00 – 21h00", telephone: "+31 20 000 00 06", aeroport: false, gare: true },
  { id: "berlin-hbf", ville: "Berlin", pays: "Allemagne", nom: "Berlin Hauptbahnhof", adresse: "Europaplatz, 10557 Berlin", horaires: "7h00 – 20h00", telephone: "+49 30 000 00 07", aeroport: false, gare: true },
  { id: "madrid-atocha", ville: "Madrid", pays: "Espagne", nom: "Madrid Atocha", adresse: "Glorieta del Emperador Carlos V, 28045 Madrid", horaires: "8h00 – 20h00", telephone: "+34 91 000 00 08", aeroport: false, gare: true },
  { id: "barcelone-sants", ville: "Barcelone", pays: "Espagne", nom: "Barcelone Sants", adresse: "Plaça dels Països Catalans, 08014 Barcelone", horaires: "8h00 – 20h00", telephone: "+34 93 000 00 09", aeroport: false, gare: true },
  { id: "milan-centrale", ville: "Milan", pays: "Italie", nom: "Milan Centrale", adresse: "Piazza Duca d'Aosta, 20124 Milan", horaires: "7h30 – 20h00", telephone: "+39 02 0000 0010", aeroport: false, gare: true },
  { id: "lisbonne-aeroport", ville: "Lisbonne", pays: "Portugal", nom: "Lisbonne Aéroport", adresse: "Aéroport Humberto Delgado, 1700-007 Lisbonne", horaires: "6h30 – 23h30", telephone: "+351 21 000 00 11", aeroport: true, gare: false }
];

// Catégories : "mini", "citadine", "compacte"
const VEHICULES = [
  { id: "fiat-500", marque: "Fiat", modele: "500", categorie: "mini", transmission: "manuelle", places: 4, portes: 3, carburant: "essence", prixJour: 29, couleur: "#e11d48" },
  { id: "kia-picanto", marque: "Kia", modele: "Picanto", categorie: "mini", transmission: "manuelle", places: 4, portes: 5, carburant: "essence", prixJour: 27, couleur: "#0ea5e9" },
  { id: "fiat-panda", marque: "Fiat", modele: "Panda", categorie: "mini", transmission: "manuelle", places: 4, portes: 5, carburant: "hybride", prixJour: 31, couleur: "#16a34a" },
  { id: "toyota-aygo-x", marque: "Toyota", modele: "Aygo X", categorie: "citadine", transmission: "automatique", places: 4, portes: 5, carburant: "essence", prixJour: 38, couleur: "#f59e0b" },
  { id: "peugeot-208", marque: "Peugeot", modele: "208", categorie: "citadine", transmission: "manuelle", places: 5, portes: 5, carburant: "essence", prixJour: 36, couleur: "#2563eb" },
  { id: "renault-clio", marque: "Renault", modele: "Clio", categorie: "citadine", transmission: "manuelle", places: 5, portes: 5, carburant: "hybride", prixJour: 39, couleur: "#eab308" },
  { id: "citroen-c3", marque: "Citroën", modele: "C3", categorie: "citadine", transmission: "manuelle", places: 5, portes: 5, carburant: "essence", prixJour: 34, couleur: "#64748b" },
  { id: "vw-polo", marque: "Volkswagen", modele: "Polo", categorie: "compacte", transmission: "automatique", places: 5, portes: 5, carburant: "essence", prixJour: 48, couleur: "#1e3a8a" },
  { id: "peugeot-208-electrique", marque: "Peugeot", modele: "e-208", categorie: "compacte", transmission: "automatique", places: 5, portes: 5, carburant: "électrique", prixJour: 52, couleur: "#06b6d4" },
  { id: "hyundai-i10", marque: "Hyundai", modele: "i10", categorie: "mini", transmission: "manuelle", places: 4, portes: 5, carburant: "essence", prixJour: 26, couleur: "#7c3aed" }
];

const OPTIONS = [
  { id: "assurance-plus", nom: "Protection étendue", description: "Réduit votre franchise à 0 €.", prixJour: 12 },
  { id: "siege-enfant", nom: "Siège enfant", description: "Siège homologué, de 9 à 36 kg.", prixJour: 6 },
  { id: "conducteur-supp", nom: "Conducteur supplémentaire", description: "Ajoute un second conducteur désigné.", prixJour: 5 }
];

const FRAIS_RETOUR_AUTRE_AGENCE = 45; // forfait en euros
