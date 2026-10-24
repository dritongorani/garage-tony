/* ---------------------------------------------------------------------------
 * Barre de navigation Mecanoo Lyon — assets/nav.js
 *
 * Dropdowns desktop ≥ lg (data-nav-dd) + menu mobile et ses accordéons
 * (data-nav-acc). Le script gère **N instances** : les IDs ne servent plus
 * qu'à l'accessibilité (aria-controls / aria-labelledby), le câblage se fait
 * par data-attributes.
 *
 * Principe : les états « fermé » sont portés par les classes Tailwind
 * STATIQUES de partials/navbar.html ; ce script écrit uniquement les styles
 * inline qui déclenchent la transition (`transition-all` du markup).
 * Aucune classe n'est générée à la volée → aucune dépendance au JIT du CDN
 * Tailwind, aucune CLS (le menu fermé occupe 0 px).
 *
 * Compatibilité : les pages générées embarquent encore l'ancien listener
 * inline qui bascule la classe `hidden` sur #mobile-menu. Il est neutralisé
 * ici (la classe est retirée pendant le même événement), l'état d'ouverture
 * étant désormais porté par ce fichier.
 * --------------------------------------------------------------------------- */
(function () {
  'use strict';

  if (window.__mecanooNav) return; // garde anti double inclusion
  window.__mecanooNav = true;

  var DESKTOP = window.matchMedia('(min-width: 1024px)');

  var burger = document.getElementById('mobile-menu-btn');
  var menu = document.getElementById('mobile-menu');
  var burgerOpen = burger ? burger.querySelector('[data-burger="open"]') : null;
  var burgerClose = burger ? burger.querySelector('[data-burger="close"]') : null;

  if (!burger || !menu) return;

  var menuOpen = false;
  var hoverTimer = null;
  var touchUsed = false; // tactile : le survol n'ouvre pas, le clic seul commande

  /* -- Instances (N dropdowns / N accordéons) ---------------------------- */

  function instances(attr) {
    var roots = document.querySelectorAll('[data-nav-' + attr + ']');
    var list = [];
    for (var i = 0; i < roots.length; i++) {
      list.push({
        root: roots[i],
        btn: roots[i].querySelector('[data-nav-' + attr + '-btn]'),
        panel: roots[i].querySelector('[data-nav-' + attr + '-panel]'),
        chev: roots[i].querySelector('[data-nav-' + attr + '-chev]'),
        open: false,
        lastFocus: null
      });
    }
    return list;
  }

  var dropdowns = instances('dd');
  var accordions = instances('acc');

  /* -- Primitives ------------------------------------------------------- */

  function show(el, chev, btn, open) {
    if (el) {
      el.style.opacity = open ? '1' : '';
      el.style.visibility = open ? 'visible' : '';
      el.style.pointerEvents = open ? 'auto' : '';
      el.style.transform = open ? 'none' : '';
    }
    if (chev) chev.style.transform = open ? 'rotate(180deg)' : '';
    if (btn) btn.setAttribute('aria-expanded', String(open));
  }

  function setDropdown(g, open) {
    g.open = open;
    if (open) g.lastFocus = g.btn;
    show(g.panel, g.chev, g.btn, open);
  }

  function closeDropdowns(except) {
    for (var i = 0; i < dropdowns.length; i++) {
      if (dropdowns[i] !== except && dropdowns[i].open) setDropdown(dropdowns[i], false);
    }
  }

  function setAccordion(g, open) {
    g.open = open;
    if (!g.panel) return;
    show(g.panel, g.chev, g.btn, open);
    g.panel.style.maxHeight = open ? g.panel.scrollHeight + 'px' : '';
    if (g.root) g.root.classList.toggle('is-open', open);
  }

  function closeAccordions() {
    for (var i = 0; i < accordions.length; i++) {
      if (accordions[i].open) setAccordion(accordions[i], false);
    }
  }

  function setMenu(open) {
    menuOpen = open;
    menu.classList.remove('hidden'); // neutralise l'ancien listener inline
    show(menu, null, burger, open);
    menu.style.maxHeight = open ? 'calc(100vh - 4.75rem)' : '';
    if (burgerOpen) burgerOpen.classList.toggle('hidden', open);
    if (burgerClose) burgerClose.classList.toggle('hidden', !open);
    burger.setAttribute('aria-label', open ? 'Fermer le menu' : 'Ouvrir le menu');
    if (!open) closeAccordions();
  }

  /* -- Dropdowns desktop : survol, clic, clavier ------------------------- */

  dropdowns.forEach(function (g) {
    if (!g.root || !g.btn || !g.panel) return;

    // Sur écran tactile ≥ lg (iPad), le premier tap déclenche aussi
    // `mouseenter` : on verrouille le survol pour que le clic reste maître.
    g.root.addEventListener('touchstart', function () {
      touchUsed = true;
    }, { passive: true });

    g.root.addEventListener('mouseenter', function () {
      if (touchUsed || !DESKTOP.matches) return;
      clearTimeout(hoverTimer);
      closeDropdowns(g);
      setDropdown(g, true);
    });

    g.root.addEventListener('mouseleave', function () {
      if (touchUsed || !DESKTOP.matches) return;
      clearTimeout(hoverTimer);
      hoverTimer = setTimeout(function () {
        setDropdown(g, false);
      }, 140);
    });

    g.btn.addEventListener('click', function () {
      clearTimeout(hoverTimer);
      var next = !g.open;
      closeDropdowns(g);
      setDropdown(g, next);
    });

    // Fermeture quand le focus quitte le composant (navigation au clavier).
    g.root.addEventListener('focusout', function (e) {
      if (!g.root.contains(e.relatedTarget)) setDropdown(g, false);
    });

    // Un clic sur un lien du panneau referme (utile pour les ancres #…).
    g.panel.addEventListener('click', function (e) {
      if (e.target.closest && e.target.closest('a[href]')) setDropdown(g, false);
    });
  });

  /* -- Menu mobile ------------------------------------------------------- */

  burger.addEventListener('click', function () {
    setMenu(!menuOpen);
  });

  menu.addEventListener('click', function (e) {
    if (e.target.closest && e.target.closest('a[href]')) setMenu(false);
  });

  accordions.forEach(function (g) {
    if (!g.btn || !g.panel) return;
    g.btn.addEventListener('click', function () {
      var next = !g.open;
      closeAccordions();
      setAccordion(g, next);
    });
  });

  /* -- Global : clic extérieur, Échap, passage en desktop ---------------- */

  document.addEventListener('click', function (e) {
    for (var i = 0; i < dropdowns.length; i++) {
      var g = dropdowns[i];
      if (g.open && g.root && !g.root.contains(e.target)) setDropdown(g, false);
    }
  });

  document.addEventListener('keydown', function (e) {
    var key = e.key;
    if (key !== 'Escape' && key !== 'Esc') return;
    var open = null;
    for (var i = 0; i < dropdowns.length; i++) if (dropdowns[i].open) open = dropdowns[i];
    if (open) {
      closeDropdowns(null);
      if (open.lastFocus) open.lastFocus.focus();
    } else if (menuOpen) {
      setMenu(false);
      burger.focus();
    }
  });

  function onBreakpoint(e) {
    if (!e.matches) return;
    if (menuOpen) setMenu(false);
    closeDropdowns(null);
  }

  if (DESKTOP.addEventListener) DESKTOP.addEventListener('change', onBreakpoint);
  else if (DESKTOP.addListener) DESKTOP.addListener(onBreakpoint);

  /* -- État initial ------------------------------------------------------ */

  setMenu(false);
  closeDropdowns(null);
})();
