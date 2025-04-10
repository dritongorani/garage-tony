// Ajoute un écouteur d'événement sur le bouton
document.querySelector('.cta-btn').addEventListener('click', function(e) {
    e.preventDefault(); // Empêche le comportement par défaut du lien
    const target = document.querySelector(this.getAttribute('href')); // Cible la section à atteindre
  
    // Fait défiler la page jusqu'à la section cible avec un effet doux
    target.scrollIntoView({
      behavior: 'smooth',
      block: 'start'
    });
  });
  