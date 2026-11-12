(function () {
  "use strict";

  // Année courante dans le pied de page
  var annee = document.getElementById("annee");
  if (annee) {
    annee.textContent = new Date().getFullYear();
  }

  // Menu mobile
  var toggle = document.querySelector(".menu-toggle");
  var menu = document.getElementById("menu");

  if (toggle && menu) {
    toggle.addEventListener("click", function () {
      var ouvert = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!ouvert));
      toggle.setAttribute("aria-label", ouvert ? "Ouvrir le menu" : "Fermer le menu");
      menu.classList.toggle("open", !ouvert);
    });

    // Ferme le menu après un clic sur un lien
    menu.querySelectorAll("a").forEach(function (lien) {
      lien.addEventListener("click", function () {
        toggle.setAttribute("aria-expanded", "false");
        toggle.setAttribute("aria-label", "Ouvrir le menu");
        menu.classList.remove("open");
      });
    });
  }

  // Formulaire de contact (démonstration : pas d'envoi réel)
  var form = document.querySelector(".contact-form");
  var statut = document.querySelector(".form-status");

  if (form && statut) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }
      statut.textContent = "Merci ! Votre message a bien été envoyé.";
      form.reset();
    });
  }
})();
