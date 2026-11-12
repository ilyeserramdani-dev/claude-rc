(function () {
  "use strict";

  // ---------- Utilitaires ----------
  function euros(montant) {
    return montant.toLocaleString("fr-FR", { style: "currency", currency: "EUR" });
  }

  function dateISO(d) {
    var y = d.getFullYear();
    var m = String(d.getMonth() + 1).padStart(2, "0");
    var j = String(d.getDate()).padStart(2, "0");
    return y + "-" + m + "-" + j;
  }

  function ajouterJours(d, n) {
    var copie = new Date(d);
    copie.setDate(copie.getDate() + n);
    return copie;
  }

  function nombreDeJours(debut, fin) {
    // Location facturée par tranche de 24 h, minimum 1 jour
    var ms = fin - debut;
    return Math.max(1, Math.ceil(ms / (24 * 3600 * 1000)));
  }

  function remplirSelectAgences(select, valeurDefaut) {
    if (!select) return;
    select.innerHTML = "";
    var pays = {};
    AGENCES.forEach(function (a) {
      if (!pays[a.pays]) pays[a.pays] = document.createElement("optgroup");
      pays[a.pays].label = a.pays;
      var opt = document.createElement("option");
      opt.value = a.id;
      opt.textContent = a.nom;
      if (a.id === valeurDefaut) opt.selected = true;
      pays[a.pays].appendChild(opt);
    });
    Object.keys(pays).forEach(function (p) { select.appendChild(pays[p]); });
  }

  function trouverAgence(id) {
    return AGENCES.filter(function (a) { return a.id === id; })[0];
  }

  function trouverVehicule(id) {
    return VEHICULES.filter(function (v) { return v.id === id; })[0];
  }

  function carteVehicule(v) {
    var article = document.createElement("article");
    article.className = "vehicule-card";
    article.innerHTML =
      '<div class="vehicule-visuel" style="background:' + v.couleur + '"><span>' + v.marque + "</span></div>" +
      '<div class="vehicule-corps">' +
        "<h3>" + v.marque + " " + v.modele + "</h3>" +
        '<ul class="specs">' +
          "<li>" + v.places + " places</li>" +
          "<li>" + v.portes + " portes</li>" +
          "<li>" + capitaliser(v.transmission) + "</li>" +
          "<li>" + capitaliser(v.carburant) + "</li>" +
        "</ul>" +
        '<div class="vehicule-prix"><strong>' + euros(v.prixJour) + "</strong> / jour</div>" +
        '<a class="btn btn-small" href="reservation.html?vehicule=' + encodeURIComponent(v.id) + '">Réserver</a>' +
      "</div>";
    return article;
  }

  function capitaliser(s) {
    return s.charAt(0).toUpperCase() + s.slice(1);
  }

  // ---------- Menu mobile et année ----------
  function initCommon() {
    var annee = document.getElementById("annee");
    if (annee) annee.textContent = new Date().getFullYear();

    var toggle = document.querySelector(".menu-toggle");
    var menu = document.getElementById("menu");
    if (toggle && menu) {
      toggle.addEventListener("click", function () {
        var ouvert = toggle.getAttribute("aria-expanded") === "true";
        toggle.setAttribute("aria-expanded", String(!ouvert));
        menu.classList.toggle("open", !ouvert);
      });
    }

    // Marque la page courante dans la navigation
    var page = location.pathname.split("/").pop() || "index.html";
    document.querySelectorAll(".main-nav a").forEach(function (a) {
      if (a.getAttribute("href") === page) a.classList.add("active");
    });
  }

  // ---------- Accueil : formulaire de recherche ----------
  function initRecherche() {
    var form = document.getElementById("form-recherche");
    if (!form) return;

    remplirSelectAgences(document.getElementById("retrait"), "paris-gare-lyon");

    var aujourdhui = new Date();
    var dateDebut = document.getElementById("date-debut");
    var dateFin = document.getElementById("date-fin");
    dateDebut.min = dateISO(aujourdhui);
    dateFin.min = dateISO(aujourdhui);
    dateDebut.value = dateISO(ajouterJours(aujourdhui, 1));
    dateFin.value = dateISO(ajouterJours(aujourdhui, 4));

    dateDebut.addEventListener("change", function () {
      dateFin.min = dateDebut.value;
      if (dateFin.value < dateDebut.value) dateFin.value = dateDebut.value;
    });

    var autreRetour = document.getElementById("autre-retour");
    var blocRetour = document.getElementById("bloc-retour");
    autreRetour.addEventListener("change", function () {
      blocRetour.hidden = !autreRetour.checked;
    });
    remplirSelectAgences(document.getElementById("restitution"), "paris-gare-lyon");

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var params = new URLSearchParams({
        retrait: document.getElementById("retrait").value,
        restitution: autreRetour.checked
          ? document.getElementById("restitution").value
          : document.getElementById("retrait").value,
        debut: dateDebut.value + "T" + document.getElementById("heure-debut").value,
        fin: dateFin.value + "T" + document.getElementById("heure-fin").value
      });
      window.location.href = "reservation.html?" + params.toString();
    });
  }

  // ---------- Page véhicules : filtres ----------
  function initVehicules() {
    var grille = document.getElementById("grille-vehicules");
    if (!grille) return;

    var filtreCategorie = document.getElementById("filtre-categorie");
    var filtreTransmission = document.getElementById("filtre-transmission");
    var compteur = document.getElementById("compteur");

    function afficher() {
      grille.innerHTML = "";
      var cat = filtreCategorie.value;
      var trans = filtreTransmission.value;
      var liste = VEHICULES.filter(function (v) {
        return (cat === "tous" || v.categorie === cat) &&
               (trans === "tous" || v.transmission === trans);
      });
      liste.forEach(function (v) { grille.appendChild(carteVehicule(v)); });
      compteur.textContent = liste.length + " véhicule(s) disponible(s)";
      if (liste.length === 0) {
        grille.innerHTML = '<p class="vide">Aucun véhicule ne correspond à ces critères.</p>';
      }
    }

    filtreCategorie.addEventListener("change", afficher);
    filtreTransmission.addEventListener("change", afficher);
    afficher();
  }

  // ---------- Page agences : recherche ----------
  function initAgences() {
    var liste = document.getElementById("liste-agences");
    if (!liste) return;

    var champ = document.getElementById("recherche-agence");
    var filtrePays = document.getElementById("filtre-pays");

    var pays = AGENCES.map(function (a) { return a.pays; })
      .filter(function (p, i, t) { return t.indexOf(p) === i; });
    pays.forEach(function (p) {
      var opt = document.createElement("option");
      opt.value = p;
      opt.textContent = p;
      filtrePays.appendChild(opt);
    });

    function afficher() {
      var terme = champ.value.trim().toLowerCase();
      var p = filtrePays.value;
      liste.innerHTML = "";
      AGENCES.filter(function (a) {
        var texte = (a.nom + " " + a.ville + " " + a.adresse).toLowerCase();
        return (p === "tous" || a.pays === p) && texte.indexOf(terme) !== -1;
      }).forEach(function (a) {
        var art = document.createElement("article");
        art.className = "agence-card";
        art.innerHTML =
          "<h3>" + a.nom + "</h3>" +
          "<p>" + a.adresse + "</p>" +
          "<ul class=\"specs\">" +
            "<li>Horaires : " + a.horaires + "</li>" +
            "<li>Tél : " + a.telephone + "</li>" +
            (a.aeroport ? "<li>Aéroport</li>" : "") +
            (a.gare ? "<li>Gare</li>" : "") +
          "</ul>" +
          '<a class="btn btn-small" href="reservation.html?retrait=' + a.id + '">Réserver ici</a>';
        liste.appendChild(art);
      });
      if (!liste.children.length) {
        liste.innerHTML = '<p class="vide">Aucune agence trouvée.</p>';
      }
    }

    champ.addEventListener("input", afficher);
    filtrePays.addEventListener("change", afficher);
    afficher();
  }

  // ---------- Page FAQ : accordéon ----------
  function initFaq() {
    document.querySelectorAll(".faq-question").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var reponse = btn.nextElementSibling;
        var ouvert = btn.getAttribute("aria-expanded") === "true";
        btn.setAttribute("aria-expanded", String(!ouvert));
        reponse.hidden = ouvert;
      });
    });
  }

  // ---------- Page contact ----------
  function initContact() {
    var form = document.getElementById("form-contact");
    if (!form) return;
    var statut = document.getElementById("statut-contact");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      statut.textContent = "Merci, votre message a bien été envoyé. Nous vous répondrons sous 24 h.";
      form.reset();
    });
  }

  // ---------- Page réservation : étapes ----------
  function initReservation() {
    var etapes = document.querySelectorAll(".etape");
    if (!etapes.length) return;

    var params = new URLSearchParams(location.search);
    var etat = {
      etape: 1,
      retrait: params.get("retrait") || "paris-gare-lyon",
      restitution: params.get("restitution") || params.get("retrait") || "paris-gare-lyon",
      debut: params.get("debut") || "",
      fin: params.get("fin") || "",
      vehicule: params.get("vehicule") || "",
      options: [],
      client: {}
    };

    // Dates par défaut si absentes
    var maintenant = new Date();
    if (!etat.debut) etat.debut = dateISO(ajouterJours(maintenant, 1)) + "T10:00";
    if (!etat.fin) etat.fin = dateISO(ajouterJours(maintenant, 4)) + "T10:00";

    var elDebut = document.getElementById("res-debut");
    var elFin = document.getElementById("res-fin");
    var elRetrait = document.getElementById("res-retrait");
    var elRestitution = document.getElementById("res-restitution");
    var elVehicules = document.getElementById("res-vehicules");
    var elOptions = document.getElementById("res-options");
    var elRecap = document.getElementById("res-recap");
    var elConfirm = document.getElementById("res-confirmation");

    remplirSelectAgences(elRetrait, etat.retrait);
    remplirSelectAgences(elRestitution, etat.restitution);
    elDebut.value = etat.debut;
    elFin.value = etat.fin;
    elDebut.min = dateISO(maintenant) + "T00:00";

    function aller(n) {
      etat.etape = n;
      etapes.forEach(function (s, i) { s.hidden = i + 1 !== n; });
      document.querySelectorAll(".progression li").forEach(function (li, i) {
        li.classList.toggle("actif", i + 1 <= n);
      });
      window.scrollTo({ top: 0, behavior: "smooth" });
      if (n === 2) afficherVehicules();
      if (n === 3) afficherOptions();
      if (n === 4) afficherRecap();
    }

    function lireDates() {
      etat.debut = elDebut.value;
      etat.fin = elFin.value;
      etat.retrait = elRetrait.value;
      etat.restitution = elRestitution.value;
      var d1 = new Date(etat.debut);
      var d2 = new Date(etat.fin);
      if (!etat.debut || !etat.fin || d2 <= d1) return "La date de retour doit être postérieure à la date de départ.";
      return "";
    }

    function dureeEtPrix() {
      var jours = nombreDeJours(new Date(etat.debut), new Date(etat.fin));
      return jours;
    }

    function afficherVehicules() {
      elVehicules.innerHTML = "";
      var jours = dureeEtPrix();
      VEHICULES.forEach(function (v) {
        var label = document.createElement("label");
        label.className = "choix-vehicule";
        var checked = etat.vehicule === v.id ? "checked" : "";
        label.innerHTML =
          '<input type="radio" name="vehicule" value="' + v.id + '" ' + checked + ">" +
          '<span class="choix-corps"><strong>' + v.marque + " " + v.modele + "</strong>" +
          "<span>" + capitaliser(v.categorie) + " · " + capitaliser(v.transmission) + " · " + v.places + " places</span>" +
          "<span>" + euros(v.prixJour * jours) + " pour " + jours + " jour(s)</span></span>";
        elVehicules.appendChild(label);
      });
      elVehicules.querySelectorAll("input").forEach(function (r) {
        r.addEventListener("change", function () { etat.vehicule = r.value; });
      });
    }

    function afficherOptions() {
      elOptions.innerHTML = "";
      OPTIONS.forEach(function (o) {
        var label = document.createElement("label");
        label.className = "choix-option";
        var checked = etat.options.indexOf(o.id) !== -1 ? "checked" : "";
        label.innerHTML =
          '<input type="checkbox" value="' + o.id + '" ' + checked + ">" +
          '<span class="choix-corps"><strong>' + o.nom + " (+" + euros(o.prixJour) + " / jour)</strong>" +
          "<span>" + o.description + "</span></span>";
        elOptions.appendChild(label);
      });
      elOptions.querySelectorAll("input").forEach(function (c) {
        c.addEventListener("change", function () {
          etat.options = Array.from(elOptions.querySelectorAll("input:checked"))
            .map(function (x) { return x.value; });
        });
      });
    }

    function calculerTotal() {
      var jours = dureeEtPrix();
      var v = trouverVehicule(etat.vehicule);
      var lignes = [];
      var total = 0;
      if (v) {
        var base = v.prixJour * jours;
        total += base;
        lignes.push([v.marque + " " + v.modele + " (" + jours + " j × " + euros(v.prixJour) + ")", base]);
      }
      etat.options.forEach(function (id) {
        var o = OPTIONS.filter(function (x) { return x.id === id; })[0];
        if (o) {
          var m = o.prixJour * jours;
          total += m;
          lignes.push([o.nom, m]);
        }
      });
      if (etat.restitution !== etat.retrait) {
        total += FRAIS_RETOUR_AUTRE_AGENCE;
        lignes.push(["Retour dans une autre agence", FRAIS_RETOUR_AUTRE_AGENCE]);
      }
      return { lignes: lignes, total: total };
    }

    function afficherRecap() {
      var v = trouverVehicule(etat.vehicule);
      var ag1 = trouverAgence(etat.retrait);
      var ag2 = trouverAgence(etat.restitution);
      var t = calculerTotal();
      var html = "<h3>Récapitulatif</h3>" +
        "<p><strong>Départ :</strong> " + (ag1 ? ag1.nom : "-") + " — " + formaterDate(etat.debut) + "</p>" +
        "<p><strong>Retour :</strong> " + (ag2 ? ag2.nom : "-") + " — " + formaterDate(etat.fin) + "</p>" +
        "<p><strong>Véhicule :</strong> " + (v ? v.marque + " " + v.modele : "Non choisi") + "</p>" +
        "<ul class=\"recap-lignes\">";
      t.lignes.forEach(function (l) {
        html += "<li><span>" + l[0] + "</span><span>" + euros(l[1]) + "</span></li>";
      });
      html += "</ul><p class=\"recap-total\"><span>Total estimé</span><strong>" + euros(t.total) + "</strong></p>" +
        "<p class=\"note\">Tarif indicatif. Le prix définitif est confirmé à l'agence (carburant, frais de dossier et taxes éventuels non inclus).</p>";
      elRecap.innerHTML = html;
    }

    function formaterDate(s) {
      if (!s) return "-";
      var d = new Date(s);
      if (isNaN(d)) return s;
      return d.toLocaleString("fr-FR", { dateStyle: "medium", timeStyle: "short" });
    }

    // Navigation entre les étapes
    document.getElementById("btn-etape1").addEventListener("click", function () {
      var erreur = lireDates();
      var msg = document.getElementById("erreur-etape1");
      if (erreur) { msg.textContent = erreur; return; }
      msg.textContent = "";
      aller(2);
    });

    document.getElementById("btn-etape2").addEventListener("click", function () {
      var msg = document.getElementById("erreur-etape2");
      if (!etat.vehicule) { msg.textContent = "Veuillez choisir un véhicule."; return; }
      msg.textContent = "";
      aller(3);
    });

    document.getElementById("btn-etape3").addEventListener("click", function () {
      aller(4);
    });

    document.querySelectorAll(".btn-retour").forEach(function (b) {
      b.addEventListener("click", function () { aller(Number(b.dataset.vers)); });
    });

    var formClient = document.getElementById("form-client");
    formClient.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!formClient.checkValidity()) { formClient.reportValidity(); return; }
      etat.client = {
        nom: document.getElementById("client-nom").value,
        email: document.getElementById("client-email").value
      };
      var ref = "M59-" + Math.random().toString(36).slice(2, 8).toUpperCase();
      document.querySelector(".etapes-wrap").hidden = true;
      document.querySelector(".progression").hidden = true;
      elConfirm.hidden = false;
      elConfirm.innerHTML = "<h2>Réservation enregistrée</h2>" +
        "<p>Merci " + etat.client.nom + ". Votre numéro de réservation est <strong>" + ref + "</strong>.</p>" +
        "<p>Un récapitulatif sera envoyé à <strong>" + etat.client.email + "</strong>.</p>" +
        '<p class="note">Démonstration : aucune réservation réelle n\'a été créée.</p>' +
        '<a class="btn" href="index.html">Retour à l\'accueil</a>';
      window.scrollTo({ top: 0, behavior: "smooth" });
    });

    aller(1);
  }

  // ---------- Démarrage ----------
  document.addEventListener("DOMContentLoaded", function () {
    initCommon();
    initRecherche();
    initVehicules();
    initAgences();
    initFaq();
    initContact();
    initReservation();
  });
})();
