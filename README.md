# Moveo 59 — site de location de citadines

Site statique (HTML / CSS / JavaScript, sans dépendance) pour la location de véhicules citadins dans le Nord de la France.

## Pages

- `index.html` : accueil, formulaire de recherche, atouts, véhicules populaires
- `vehicules.html` : toute la flotte, filtres par catégorie et boîte de vitesses
- `agences.html` : agences par ville, gare et aéroport, recherche et filtre par pays
- `reservation.html` : réservation en 4 étapes (dates et lieux, véhicule, options, informations et récapitulatif)
- `contact.html` : foire aux questions et formulaire de contact

## Structure

- `css/style.css` : styles responsives (mobile, tablette, ordinateur)
- `js/data.js` : **agences, véhicules, options et tarifs** (données de démonstration à remplacer)
- `js/app.js` : logique du site (recherche, filtres, réservation, FAQ, formulaires)

## Utilisation

Ouvrez `index.html` dans un navigateur, ou servez le dossier avec un serveur statique :

```bash
python3 -m http.server 8000
```

## À faire avant la mise en ligne

- Remplacer les agences, adresses, horaires et numéros de téléphone (`js/data.js`, `contact.html`) par les vrais.
- Remplacer les véhicules et tarifs (`js/data.js`).
- Brancher les formulaires (recherche, réservation, contact) sur un vrai back-end ou un service d'envoi. Actuellement ils sont en démonstration : aucune réservation n'est enregistrée.
- Relire les conditions de location et la FAQ avec le service juridique.
