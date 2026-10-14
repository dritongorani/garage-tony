/* ---------------------------------------------------------------------------
 * Barre de navigation Mecanoo Lyon — assets/nav.js
 *
 * Dropdown « Nos services » (desktop ≥ lg) + menu mobile et son accordéon.
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

  var dd = document.getElementById('nav-dd');
  var ddBtn = document.getElementById('nav-dd-btn');
  var ddPanel = document.getElementById('nav-dd-panel');
  var ddChev = document.getElementById('nav-dd-chev');

  var burger = document.getElementById('mobile-menu-btn');
  var menu = document.getElementById('mobile-menu');
  var burgerOpen = burger ? burger.querySelector('[data-burger="open"]') : null;
  var burgerClose = burger ? burger.querySelector('[data-burger="close"]') : null;

  var accItem = document.getElementById('m-services-item');
  var accBtn = document.getElementById('m-services-btn');
  var accPanel = document.getElementById('m-services-panel');
  var accChev = document.getElementById('m-services-chev');

  if (!burger || !menu) return;

  var ddOpen = false;
  var menuOpen = false;
  var accOpen = false;
  var hoverTimer = null;
  var touchUsed = false; // tactile : le survol n'ouvre pas, le clic seul commande

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

  function setDropdown(open) {
    ddOpen = open;
    show(ddPanel, ddChev, ddBtn, open);
  }

  function setAccordion(open) {
    accOpen = open;
    if (!accPanel) return;
    show(accPanel, accChev, accBtn, open);
    accPanel.style.maxHeight = open ? accPanel.scrollHeight + 'px' : '';
    if (accItem) accItem.classList.toggle('is-open', open);
  }

  function setMenu(open) {
    menuOpen = open;
    menu.classList.remove('hidden'); // neutralise l'ancien listener inline
    show(menu, null, burger, open);
    menu.style.maxHeight = open ? 'calc(100vh - 4.75rem)' : '';
    if (burgerOpen) burgerOpen.classList.toggle('hidden', open);
    if (burgerClose) burgerClose.classList.toggle('hidden', !open);
    burger.setAttribute('aria-label', open ? 'Fermer le menu' : 'Ouvrir le menu');
    if (!open) setAccordion(false);
  }

  /* -- Dropdown desktop : survol, clic, clavier -------------------------- */

  if (dd && ddBtn && ddPanel) {
    // Sur écran tactile ≥ lg (iPad), le premier tap déclenche aussi
    // `mouseenter` : on verrouille le survol pour que le clic reste maître.
    dd.addEventListener('touchstart', function () {
      touchUsed = true;
    }, { passive: true });

    dd.addEventListener('mouseenter', function () {
      if (touchUsed || !DESKTOP.matches) return;
      clearTimeout(hoverTimer);
      setDropdown(true);
    });

    dd.addEventListener('mouseleave', function () {
      if (touchUsed || !DESKTOP.matches) return;
      clearTimeout(hoverTimer);
      hoverTimer = setTimeout(function () {
        setDropdown(false);
      }, 140);
    });

    ddBtn.addEventListener('click', function () {
      clearTimeout(hoverTimer);
      setDropdown(!ddOpen);
    });

    // Fermeture quand le focus quitte le composant (navigation au clavier).
    dd.addEventListener('focusout', function (e) {
      if (!dd.contains(e.relatedTarget)) setDropdown(false);
    });

    // Un clic sur un lien du panneau referme (utile pour les ancres #…).
    ddPanel.addEventListener('click', function (e) {
      if (e.target.closest && e.target.closest('a[href]')) setDropdown(false);
    });
  }

  /* -- Menu mobile ------------------------------------------------------- */

  burger.addEventListener('click', function () {
    setMenu(!menuOpen);
  });

  menu.addEventListener('click', function (e) {
    if (e.target.closest && e.target.closest('a[href]')) setMenu(false);
  });

  if (accBtn && accPanel) {
    accBtn.addEventListener('click', function () {
      setAccordion(!accOpen);
    });
  }

  /* -- Global : clic extérieur, Échap, passage en desktop ---------------- */

  document.addEventListener('click', function (e) {
    if (ddOpen && dd && !dd.contains(e.target)) setDropdown(false);
  });

  document.addEventListener('keydown', function (e) {
    var key = e.key;
    if (key !== 'Escape' && key !== 'Esc') return;
    if (ddOpen && ddBtn) {
      setDropdown(false);
      ddBtn.focus();
    } else if (menuOpen) {
      setMenu(false);
      burger.focus();
    }
  });

  function onBreakpoint(e) {
    if (!e.matches) return;
    if (menuOpen) setMenu(false);
    if (ddOpen) setDropdown(false);
  }

  if (DESKTOP.addEventListener) DESKTOP.addEventListener('change', onBreakpoint);
  else if (DESKTOP.addListener) DESKTOP.addListener(onBreakpoint);

  /* -- État initial ------------------------------------------------------ */

  setMenu(false);
  setDropdown(false);
})();
