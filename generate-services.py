#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate SEO service pages for mecanolyon.fr"""

from pathlib import Path

BASE = Path(__file__).parent
SITE = "https://mecanolyon.fr"

HEAD = """<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8" />
  <script src="assets/canonical-host.js"></script>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-6NPKTDZMM4"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-6NPKTDZMM4');
  </script>
  <!-- Google Tag Manager -->
  <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-TMZK9J9X');</script>
  <!-- End Google Tag Manager -->
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="{description}" />
  <meta name="keywords" content="{keywords}" />
  <meta name="author" content="Mecanoo Lyon" />
  <meta name="robots" content="index, follow, max-image-preview:large" />
  <meta name="geo.region" content="FR-69" />
  <meta name="geo.placename" content="Lyon" />
  <title>{title}</title>
  <link rel="canonical" href="{canonical}" />
  <link rel="alternate" hreflang="fr-FR" href="{canonical}" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:title" content="{og_title}" />
  <meta property="og:description" content="{og_description}" />
  <meta property="og:locale" content="fr_FR" />
  <meta property="og:site_name" content="Mecanoo Lyon" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="theme-color" content="#0a0c0f" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: { racing: '#FF5733', ink: '#0a0c0f' },
          fontFamily: { sans: ['Inter', 'system-ui', 'sans-serif'] },
        },
      },
    };
  </script>
  <style>
    html { scroll-behavior: smooth; }
    .glass-nav {
      background: rgba(10, 12, 15, 0.72);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    }
    .noise-bg::before {
      content: '';
      position: absolute;
      inset: 0;
      background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
      pointer-events: none;
    }
  </style>
  <script type="application/ld+json">{schema}</script>
</head>
<body class="bg-ink font-sans text-zinc-100 antialiased">
  <!-- Google Tag Manager (noscript) -->
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-TMZK9J9X"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
  <!-- End Google Tag Manager (noscript) -->
"""

NAV = """
  <header class="glass-nav sticky top-0 z-50">
    <nav class="mx-auto flex max-w-6xl items-center justify-between gap-4 px-4 py-4 sm:px-6" aria-label="Navigation principale">
      <a href="/" class="flex items-center gap-2 text-lg font-bold tracking-tight text-white">
        <span class="inline-flex h-9 w-9 items-center justify-center rounded-lg bg-racing/15 text-racing ring-1 ring-racing/30" aria-hidden="true"><i data-lucide="wrench" class="h-5 w-5"></i></span>
        Mecanoo Lyon
      </a>
      <ul class="hidden flex-wrap items-center justify-end gap-x-3 gap-y-1 text-xs font-medium text-zinc-300 lg:flex xl:gap-x-5 xl:text-sm">
        <li><a href="/#services" class="transition hover:text-racing">Services</a></li>
        <li><a href="service-cles.html" class="transition hover:text-racing">Clés Lyon</a></li>
        <li><a href="service-mecanique.html" class="transition hover:text-racing">Entretien</a></li>
        <li><a href="service-reprogrammation.html" class="{reprog_class}">Reprog ECU</a></li>
        <li><a href="zone-intervention.html" class="transition hover:text-racing">Zone</a></li>
        <li><a href="/#faq" class="transition hover:text-racing">FAQ</a></li>
        <li><a href="/#contact" class="transition hover:text-racing">Contact</a></li>
      </ul>
      <div class="flex items-center gap-2 sm:gap-3">
        <a href="https://wa.me/33603439954" target="_blank" rel="noopener noreferrer" class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-[#25D366] text-white shadow-lg shadow-black/30 ring-2 ring-black/30 transition hover:scale-105" aria-label="WhatsApp">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="h-6 w-6"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.435 9.884-9.883 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
        </a>
        <a href="/#contact" class="rounded-lg bg-racing px-4 py-2 text-sm font-semibold text-white shadow-lg shadow-racing/25 transition hover:bg-racing/90">Devis gratuit</a>
      </div>
      <button type="button" id="mobile-menu-btn" class="inline-flex rounded-md p-2 text-zinc-300 lg:hidden" aria-expanded="false" aria-controls="mobile-menu" aria-label="Menu"><i data-lucide="menu" class="h-6 w-6"></i></button>
    </nav>
    <div id="mobile-menu" class="hidden border-t border-white/5 bg-ink/95 px-4 py-4 lg:hidden">
      <ul class="flex flex-col gap-3 text-sm font-medium">
        <li><a href="/#services" class="block py-2 text-zinc-300 hover:text-racing">Services</a></li>
        <li><a href="service-cles.html" class="block py-2 text-zinc-300 hover:text-racing">Clés Lyon</a></li>
        <li><a href="service-mecanique.html" class="block py-2 text-zinc-300 hover:text-racing">Freins &amp; entretien</a></li>
        <li><a href="service-reprogrammation.html" class="block py-2 {mobile_reprog_class}">Reprog ECU</a></li>
        <li><a href="zone-intervention.html" class="block py-2 text-zinc-300 hover:text-racing">Zone</a></li>
        <li><a href="/#contact" class="block py-2 text-zinc-300 hover:text-racing">Contact</a></li>
      </ul>
    </div>
  </header>
"""

FOOTER = """
  <footer class="border-t border-white/10 bg-black/40 py-12 pb-28 sm:pb-12">
    <div class="mx-auto flex max-w-6xl flex-col items-start justify-between gap-6 px-4 sm:flex-row sm:items-start sm:px-6">
      <div>
        <p class="text-sm text-zinc-500">© <span id="year"></span> Mecanoo Lyon. Tous droits réservés.</p>
        <p class="mt-2 text-sm text-zinc-600"><a href="service-cles.html" class="text-racing hover:underline">Clés Lyon</a> · <a href="service-mecanique.html" class="hover:text-zinc-400 hover:underline">Entretien</a> · <a href="service-reprogrammation.html" class="hover:text-zinc-400 hover:underline">Reprog ECU</a> · <a href="zone-intervention.html" class="hover:text-zinc-400 hover:underline">Zone</a> · <a href="/#contact" class="hover:text-zinc-400 hover:underline">Contact</a>.</p>
      </div>
      <div class="flex flex-col items-start gap-3 sm:items-end">
        <p class="text-xs uppercase tracking-wide text-zinc-600 text-left sm:text-right">Mécanique · clés · reprogrammation ECU sur devis</p>
        <a href="https://wa.me/33603439954" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-2 rounded-full border border-[#25D366]/35 bg-[#25D366]/15 px-4 py-2 text-sm font-medium text-emerald-300 transition hover:bg-[#25D366]/25">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="h-5 w-5" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.435 9.884-9.883 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
          WhatsApp +33&nbsp;6&nbsp;03&nbsp;43&nbsp;99&nbsp;54
        </a>
      </div>
    </div>
  </footer>
  <a href="https://wa.me/33603439954?text={wa_text}" target="_blank" rel="noopener noreferrer" class="fixed bottom-5 right-5 z-[60] flex h-14 w-14 items-center justify-center rounded-full bg-[#25D366] text-white shadow-2xl ring-2 ring-black/40 transition hover:scale-105 md:bottom-8 md:right-8" aria-label="WhatsApp"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="h-8 w-8"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.435 9.884-9.883 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg></a>
  <script src="https://unpkg.com/lucide@latest"></script>
  <script>
    lucide.createIcons();
    document.getElementById('year').textContent = new Date().getFullYear();
    var menuBtn = document.getElementById('mobile-menu-btn');
    var mobileMenu = document.getElementById('mobile-menu');
    if (menuBtn && mobileMenu) {{
      menuBtn.addEventListener('click', function () {{
        mobileMenu.classList.toggle('hidden');
        menuBtn.setAttribute('aria-expanded', String(!mobileMenu.classList.contains('hidden')));
      }});
    }}
  </script>
</body>
</html>
"""

LEGAL = """
    <section class="border-b border-white/5 bg-zinc-950 py-10 sm:py-12" aria-label="Mention légale">
      <div class="mx-auto max-w-3xl px-4 sm:px-6">
        <p class="text-xs leading-relaxed text-zinc-600">
          <strong class="font-medium text-zinc-500">Mention légale&nbsp;:</strong> la modification ou la désactivation de systèmes antipollution (AdBlue, SCR, FAP, EGR…) et toute reprogrammation moteur (stage, flexfuel) est strictement réservée à un usage <strong class="font-medium text-zinc-500">hors voie publique</strong> — circuit, piste privée ou usage professionnel hors route ouverte à la circulation. L'utilisation d'un véhicule modifié sur la voie publique est interdite par la réglementation en vigueur. Mecanoo informe ses clients de ces contraintes légales avant toute intervention.
        </p>
      </div>
    </section>
"""

SERVICES = [
    {
        "file": "service-adblue.html",
        "slug": "service-adblue",
        "active": "adblue",
        "breadcrumb": "AdBlue / SCR — Lyon",
        "badge": "problème AdBlue Lyon — Rhône 69",
        "icon": "alert-triangle",
        "h1": "Dépannage &amp; solution électronique AdBlue / SCR à Lyon",
        "hero": "<strong class=\"font-semibold text-zinc-200\">Problème AdBlue Lyon</strong>, <strong class=\"font-semibold text-zinc-200\">défaut antipollution Peugeot Citroën</strong> ou voyant SCR récurrent&nbsp;? Reprogrammation logicielle définitive avec outils <strong class=\"font-semibold text-zinc-200\">FoxFlash</strong> — alternative aux devis exorbitants en concession sur Lyon et le <strong class=\"font-semibold text-zinc-200\">69</strong>.",
        "title": "Dépannage AdBlue / SCR Lyon — Problème AdBlue & défaut antipollution | Mecanoo",
        "description": "Problème AdBlue Lyon : dépannage SCR, défaut antipollution Peugeot Citroën, suppression AdBlue 69. Reprogrammation FoxFlash — Mecanoo Rhône.",
        "keywords": "problème AdBlue Lyon, défaut antipollution Peugeot Citroën Lyon, suppression AdBlue 69, dépannage SCR Lyon",
        "og_title": "Dépannage AdBlue / SCR Lyon | Mecanoo",
        "og_description": "Problème AdBlue Lyon, défaut antipollution Peugeot Citroën, solution SCR sur le Rhône (69).",
        "service_name": "Dépannage AdBlue / SCR Lyon",
        "problem_title": "Le problème AdBlue / SCR",
        "problem_intro": "Compteur bloqué, réservoir déformé, injecteur bouché ou devis concession à plusieurs milliers d'euros — le système SCR touche surtout les diesel récents.",
        "problems": [
            ("Compteur kilométrique bloqué", "Message « démarrage impossible dans X km », mode dégradé, véhicule immobilisé.", "gauge"),
            ("Réservoir AdBlue déformé", "Fissures, fuites, remplacement seul &gt; 1 500 € en concession.", "droplets"),
            ("Injecteur AdBlue bouché", "Cristallisation urée, sonde NOx HS, défaut antipollution permanent.", "syringe"),
            ("Frais exorbitants concession", "Devis 2 000 à 4 000 € sans garantie de fiabilité long terme.", "euro"),
        ],
        "solution_title": "Reprogrammation définitive FoxFlash",
        "solution_intro": "Suppression AdBlue 69 par reprogrammation calculateur — plus de voyants, compteur débloqué, fin des recharges d'urée.",
        "solution_points": [
            "Suppression AdBlue 69 par reprogrammation définitive",
            "Outils officiels FoxFlash — pas un simple effacement de défauts",
            "Peugeot, Citroën, DS, Renault, VW, BMW, Mercedes…",
            "Intervention Lyon, Villeurbanne, Vénissieux, métropole 69",
        ],
        "faq_intro": "« problème AdBlue Lyon », « défaut antipollution Peugeot Citroën Lyon », « suppression AdBlue 69 »",
        "faqs": [
            ("Quels symptômes d'un problème AdBlue sur Peugeot ou Citroën à Lyon ?", "Voyant antipollution, compteur bloqué, mode dégradé, injecteur bouché. Très fréquent sur BlueHDi / HDi PSA après 80 000 km."),
            ("Combien coûte une réparation AdBlue en concession vs solution électronique 69 ?", "Concession : 2 000 à 4 000 €. Mecanoo : reprogrammation FoxFlash bien plus économique sur devis."),
            ("Proposez-vous une suppression AdBlue définitive sur Lyon et le 69 ?", "Oui : reprogrammation définitive via FoxFlash, intervention métropole lyonnaise. Devis après diagnostic."),
        ],
        "wa_text": "Bonjour%2C%20probl%C3%A8me%20AdBlue%20Lyon",
        "img_alt": "Problème AdBlue Lyon — diagnostic SCR Rhône 69",
    },
    {
        "file": "service-ecu-clonage.html",
        "slug": "service-ecu-clonage",
        "active": "ecu",
        "breadcrumb": "Clonage ECU — Lyon",
        "badge": "clonage ECU Lyon — calculateur 69",
        "icon": "cpu",
        "h1": "Clonage ECU &amp; copie calculateur à Lyon",
        "hero": "<strong class=\"font-semibold text-zinc-200\">Clonage ECU Lyon</strong>, calculateur HS, ECU noyé ou véhicule ne démarre plus&nbsp;? Copie intégrale du firmware sur un calculateur neuf ou d'occasion avec outils <strong class=\"font-semibold text-zinc-200\">FoxFlash</strong> — intervention sur Lyon et le Rhône <strong class=\"font-semibold text-zinc-200\">(69)</strong>.",
        "title": "Clonage ECU Lyon — Copie calculateur & reprogrammation | Mecanoo",
        "description": "Clonage ECU Lyon : copie calculateur moteur, ECU cloning 69, transfert firmware BSI/ECU. FoxFlash — Mecanoo métropole lyonnaise.",
        "keywords": "clonage ECU Lyon, copie calculateur Lyon, ECU cloning 69, reprogrammation calculateur Rhône",
        "og_title": "Clonage ECU Lyon | Mecanoo",
        "og_description": "Copie calculateur moteur et clonage ECU sur Lyon et le Rhône (69).",
        "service_name": "Clonage ECU Lyon",
        "problem_title": "Quand faut-il cloner un calculateur ?",
        "problem_intro": "ECU endommagé par l'eau, surtension, panne électronique ou remplacement nécessaire sans reprogrammation concession.",
        "problems": [
            ("Calculateur moteur HS", "ECU noyé, court-circuit, composants grillés — véhicule ne démarre plus.", "cpu"),
            ("Remplacement ECU d'occasion", "Calculateur d'occasion non codé à votre véhicule — immobilisation ou défauts.", "refresh-cw"),
            ("Perte données origine", "Effacement accidentel, mise à jour ratée, ECU vierge après panne.", "hard-drive"),
            ("Devis concession élevé", "Codage + main-d'œuvre concession souvent très coûteux et délais longs.", "euro"),
        ],
        "solution_title": "Clonage ECU avec FoxFlash",
        "solution_intro": "Lecture du calculateur d'origine, copie complète du firmware (Flash + EEPROM) sur ECU de remplacement, synchronisation immo si nécessaire.",
        "solution_points": [
            "Lecture complète ECU d'origine (Flash, EEPROM, OTP)",
            "Transfert sur calculateur neuf ou d'occasion compatible",
            "Codage VIN, immo, kilométrage selon besoin",
            "Peugeot, Citroën, Renault, VW, BMW, Mercedes… sur Lyon 69",
        ],
        "faq_intro": "« clonage ECU Lyon », « copie calculateur Lyon », « ECU cloning 69 »",
        "faqs": [
            ("Qu'est-ce que le clonage ECU et dans quels cas l'utiliser à Lyon ?", "Copie intégrale du firmware d'un calculateur HS vers un ECU de remplacement. Indispensable si l'ECU d'origine est irréparable."),
            ("Peut-on cloner un calculateur Peugeot ou Citroën sans aller en concession ?", "Oui, avec outils FoxFlash sur Lyon et le 69 — lecture, copie et codage sur place selon modèle."),
            ("Combien de temps dure un clonage ECU chez Mecanoo ?", "Selon marque et accès calculateur : généralement quelques heures. Devis après marque, modèle et motorisation."),
        ],
        "wa_text": "Bonjour%2C%20clonage%20ECU%20Lyon",
        "img_alt": "Clonage ECU Lyon — copie calculateur moteur Rhône 69",
    },
    {
        "file": "service-fap.html",
        "slug": "service-fap",
        "active": "fap",
        "breadcrumb": "Suppression FAP — Lyon",
        "badge": "suppression FAP Lyon — FAP 69",
        "icon": "filter",
        "h1": "Suppression FAP &amp; solution filtre à particules à Lyon",
        "hero": "<strong class=\"font-semibold text-zinc-200\">Suppression FAP Lyon</strong>, filtre à particules saturé ou régénération impossible&nbsp;? Reprogrammation logicielle définitive du FAP / DPF avec <strong class=\"font-semibold text-zinc-200\">FoxFlash</strong> — évitez le remplacement à 1 500 €+ en concession sur Lyon et le <strong class=\"font-semibold text-zinc-200\">69</strong>.",
        "title": "Suppression FAP Lyon — Filtre à particules & décalaminage | Mecanoo",
        "description": "Suppression FAP Lyon, filtre à particules saturé 69, reprogrammation DPF Rhône. Solution électronique FoxFlash — Mecanoo métropole.",
        "keywords": "suppression FAP Lyon, filtre à particules Lyon, décalaminage FAP 69, reprogrammation DPF Rhône",
        "og_title": "Suppression FAP Lyon | Mecanoo",
        "og_description": "Filtre à particules saturé ? Solution électronique FAP / DPF sur Lyon et le 69.",
        "service_name": "Suppression FAP Lyon",
        "problem_title": "Les problèmes de filtre à particules (FAP / DPF)",
        "problem_intro": "Voyant FAP, perte de puissance, régénération ratée ou conduite urbaine qui colmate le filtre rapidement.",
        "problems": [
            ("FAP saturé / colmaté", "Régénération impossible, mode dégradé, perte de puissance importante.", "filter"),
            ("Voyant FAP allumé", "Défaut antipollution récurrent malgré nettoyage ou décalaminage.", "alert-triangle"),
            ("Conduite urbaine", "Trajets courts empêchent la régénération — colmatage rapide du DPF.", "map-pin"),
            ("Remplacement coûteux", "Nouveau FAP + capteurs : 1 200 à 2 500 € en concession.", "euro"),
        ],
        "solution_title": "Suppression FAP par reprogrammation FoxFlash",
        "solution_intro": "Désactivation logicielle définitive du FAP dans le calculateur — plus de régénération, plus de voyant, conduite normale.",
        "solution_points": [
            "Suppression FAP 69 par reprogrammation calculateur",
            "Fin des cycles de régénération et voyants récurrents",
            "Diesel Peugeot, Citroën, Renault, VW, BMW, Mercedes…",
            "Intervention Lyon, métropole et Rhône sur rendez-vous",
        ],
        "faq_intro": "« suppression FAP Lyon », « filtre à particules saturé 69 », « décalaminage FAP Lyon »",
        "faqs": [
            ("Mon voyant FAP est allumé sur Lyon : que faire ?", "Diagnostic OBD d'abord. Si FAP colmaté ou HS, reprogrammation définitive souvent plus économique que remplacement."),
            ("La suppression FAP est-elle définitive ?", "Oui : modification gravée dans le calculateur via FoxFlash — pas un simple effacement temporaire."),
            ("Intervenez-vous sur diesel Peugeot et Citroën pour le FAP dans le 69 ?", "Oui : BlueHDi, HDi, et autres motorisations diesel courantes sur Lyon et métropole."),
        ],
        "wa_text": "Bonjour%2C%20suppression%20FAP%20Lyon",
        "img_alt": "Suppression FAP Lyon — filtre à particules diesel Rhône 69",
    },
    {
        "file": "service-egr.html",
        "slug": "service-egr",
        "active": "egr",
        "breadcrumb": "Suppression EGR — Lyon",
        "badge": "suppression EGR Lyon — vanne EGR 69",
        "icon": "wind",
        "h1": "Suppression EGR &amp; vanne EGR bloquée à Lyon",
        "hero": "<strong class=\"font-semibold text-zinc-200\">Suppression EGR Lyon</strong>, vanne EGR bloquée ou encrassée&nbsp;? Reprogrammation logicielle définitive + option démontage vanne — solution durable avec <strong class=\"font-semibold text-zinc-200\">FoxFlash</strong> sur Lyon et le <strong class=\"font-semibold text-zinc-200\">69</strong>.",
        "title": "Suppression EGR Lyon — Vanne EGR bloquée & reprogrammation | Mecanoo",
        "description": "Suppression EGR Lyon, vanne EGR bloquée 69, reprogrammation EGR Rhône. Solution FoxFlash — Mecanoo métropole lyonnaise.",
        "keywords": "suppression EGR Lyon, vanne EGR bloquée Lyon, reprogrammation EGR 69, dépannage EGR Rhône",
        "og_title": "Suppression EGR Lyon | Mecanoo",
        "og_description": "Vanne EGR bloquée ? Suppression EGR par reprogrammation sur Lyon et le 69.",
        "service_name": "Suppression EGR Lyon",
        "problem_title": "Les problèmes de vanne EGR",
        "problem_intro": "Encrassement, blocage en position ouverte/fermée, perte de puissance et surconsommation sur diesel.",
        "problems": [
            ("Vanne EGR bloquée", "Encrassement carbone, vanne grippée — perte de puissance et fumée noire.", "wind"),
            ("Voyant antipollution", "Défaut EGR récurrent, mode dégradé, ratés à l'accélération.", "alert-triangle"),
            ("Nettoyage temporaire", "Démontage/nettoyage vanne — problème revient en quelques mois.", "refresh-cw"),
            ("Remplacement vanne EGR", "Pièce + main-d'œuvre : 400 à 900 €, sans traiter la cause.", "euro"),
        ],
        "solution_title": "Suppression EGR par reprogrammation FoxFlash",
        "solution_intro": "Désactivation logicielle de la vanne EGR dans le calculateur — plus de défauts, plus d'encrassement EGR.",
        "solution_points": [
            "Suppression EGR 69 — reprogrammation définitive calculateur",
            "Option démontage / obturation vanne EGR",
            "Diesel toutes marques : PSA, Renault, VAG, BMW…",
            "Intervention Lyon, Villeurbanne, Vénissieux, Rhône",
        ],
        "faq_intro": "« suppression EGR Lyon », « vanne EGR bloquée Lyon », « reprogrammation EGR 69 »",
        "faqs": [
            ("Ma vanne EGR est bloquée : reprogrammation ou remplacement à Lyon ?", "La reprogrammation définitive traite la cause logicielle. Souvent plus durable et économique que remplacer la vanne."),
            ("La suppression EGR améliore-t-elle les performances ?", "Oui : moins d'encrassement admission, meilleure réponse moteur — surtout sur diesel encrassés."),
            ("Intervenez-vous sur Peugeot 308 / Citroën C4 EGR dans le 69 ?", "Oui : HDi, BlueHDi et autres diesel PSA très courants sur Lyon et métropole."),
        ],
        "wa_text": "Bonjour%2C%20suppression%20EGR%20Lyon",
        "img_alt": "Suppression EGR Lyon — vanne EGR bloquée Rhône 69",
    },
    {
        "file": "service-stage1.html",
        "slug": "service-stage1",
        "active": "stage1",
        "breadcrumb": "Reprogrammation Stage 1 — Lyon",
        "badge": "stage 1 Lyon — reprog moteur 69",
        "icon": "zap",
        "h1": "Reprogrammation Stage 1 &amp; gain de puissance à Lyon",
        "hero": "<strong class=\"font-semibold text-zinc-200\">Reprogrammation stage 1 Lyon</strong>, reprog moteur ou gain de puissance/couple&nbsp;? Cartographie optimisée avec outils <strong class=\"font-semibold text-zinc-200\">FoxFlash</strong> — diesel et essence sur Lyon et le Rhône <strong class=\"font-semibold text-zinc-200\">(69)</strong>.",
        "title": "Reprogrammation Stage 1 Lyon — Reprog moteur & gain puissance | Mecanoo",
        "description": "Reprogrammation stage 1 Lyon, reprog moteur 69, gain puissance Rhône. Tuning FoxFlash — Mecanoo métropole lyonnaise.",
        "keywords": "reprogrammation stage 1 Lyon, reprog moteur Lyon, gain puissance 69, tuning automobile Rhône",
        "og_title": "Reprogrammation Stage 1 Lyon | Mecanoo",
        "og_description": "Stage 1 : gain de puissance et couple sur Lyon et le 69 avec FoxFlash.",
        "service_name": "Reprogrammation Stage 1 Lyon",
        "problem_title": "Pourquoi une reprogrammation Stage 1 ?",
        "problem_intro": "Les constructeurs laissent une marge dans la cartographie d'origine — exploitable en toute sécurité avec les bons outils.",
        "problems": [
            ("Manque de reprise", "Accélération fade, manque de couple à bas régime en usage quotidien.", "gauge"),
            ("Consommation élevée", "Moteur sous-exploité — consommation non optimale en conduite normale.", "fuel"),
            ("Marge constructeur", "Carto d'origine volontairement bridée pour normes et fiabilité marketing.", "cpu"),
            ("Reprog générique risquée", "Fichiers bas de gamme = risque moteur. FoxFlash = cartographies fiables.", "shield-alert"),
        ],
        "solution_title": "Stage 1 FoxFlash — puissance & couple optimisés",
        "solution_intro": "Modification cartographie injection, turbo, couple — gains typiques +20 à +40 ch selon motorisation.",
        "solution_points": [
            "Stage 1 sur mesure — pas de fichier générique",
            "Gains puissance ET couple, meilleure réponse",
            "Essence et diesel : PSA, VAG, BMW, Mercedes, Renault…",
            "Lyon, métropole, Rhône (69) — devis après modèle",
        ],
        "faq_intro": "« reprogrammation stage 1 Lyon », « reprog moteur Lyon », « gain puissance 69 »",
        "faqs": [
            ("Combien de chevaux gagne-t-on avec un stage 1 à Lyon ?", "Typiquement +20 à +40 ch et +40 à +80 Nm selon motorisation. Devis personnalisé après modèle."),
            ("La reprogrammation stage 1 est-elle fiable ?", "Oui avec FoxFlash et cartographies adaptées — paramètres dans les limites mécaniques du moteur."),
            ("Proposez-vous stage 1 sur diesel Peugeot / Citroën dans le 69 ?", "Oui : BlueHDi, HDi, TDI, dCi… intervention sur Lyon et métropole."),
        ],
        "wa_text": "Bonjour%2C%20stage%201%20Lyon",
        "img_alt": "Reprogrammation stage 1 Lyon — gain puissance moteur Rhône 69",
    },
    {
        "file": "service-flexfuel.html",
        "slug": "service-flexfuel",
        "active": "flexfuel",
        "breadcrumb": "Reprogrammation Flexfuel E85 — Lyon",
        "badge": "flexfuel E85 Lyon — conversion ethanol 69",
        "icon": "fuel",
        "h1": "Reprogrammation Flexfuel E85 &amp; conversion éthanol à Lyon",
        "hero": "<strong class=\"font-semibold text-zinc-200\">Reprogrammation E85 Lyon</strong>, conversion flexfuel ou passage à l'éthanol&nbsp;? Cartographie Flex Fuel avec <strong class=\"font-semibold text-zinc-200\">FoxFlash</strong> — roulez SP95/E85 indifféremment, économies à la pompe sur Lyon et le <strong class=\"font-semibold text-zinc-200\">69</strong>.",
        "title": "Reprogrammation Flexfuel E85 Lyon — Conversion éthanol 69 | Mecanoo",
        "description": "Reprogrammation E85 Lyon, flexfuel 69, conversion éthanol Rhône. Cartographie Flex Fuel FoxFlash — Mecanoo métropole.",
        "keywords": "reprogrammation E85 Lyon, flexfuel Lyon, conversion éthanol 69, passage E85 Rhône",
        "og_title": "Reprogrammation Flexfuel E85 Lyon | Mecanoo",
        "og_description": "Flexfuel E85 : conversion éthanol par reprogrammation sur Lyon et le 69.",
        "service_name": "Reprogrammation Flexfuel E85 Lyon",
        "problem_title": "Pourquoi passer en Flexfuel E85 ?",
        "problem_intro": "L'E85 coûte ~40 % moins cher que le SP95-10 — la reprogrammation Flex Fuel permet de rouler indifféremment E85 ou essence.",
        "problems": [
            ("Carburant cher", "SP95/SP98 en hausse constante — E85 ~0,85 €/L en station.", "euro"),
            ("Kit flexfuel classique", "Boîtier additif = coût pièce + pose + parfois défauts sonde.", "box"),
            ("Compatibilité moteur", "Tous moteurs essence ne supportent pas l'E85 sans reprogrammation.", "cpu"),
            ("Reprog nécessaire", "Cartographie adaptée pour démarrage à froid et mélange optimal E85/SP95.", "settings"),
        ],
        "solution_title": "Flex Fuel FoxFlash — E85 + essence sans boîtier",
        "solution_intro": "Reprogrammation calculateur pour détection automatique E85/essence — pas de boîtier additif, solution intégrée.",
        "solution_points": [
            "Reprog Flex Fuel intégrée au calculateur",
            "Roulez E85, SP95 ou mélange indifféremment",
            "Économies significatives à la pompe",
            "Essence turbo et atmo : PSA, VAG, BMW, Ford… Lyon 69",
        ],
        "faq_intro": "« reprogrammation E85 Lyon », « flexfuel Lyon », « conversion éthanol 69 »",
        "faqs": [
            ("Mon véhicule peut-il passer en E85 à Lyon ?", "La plupart des essence turbo et certains atmo — faisabilité après marque, modèle, année. Devis gratuit."),
            ("Faut-il un boîtier flexfuel en plus de la reprogrammation ?", "Non : la reprog FoxFlash intègre la gestion Flex Fuel directement dans le calculateur."),
            ("Quelle économie avec l'E85 dans le Rhône (69) ?", "E85 ~40 % moins cher que SP95. Surconsommation ~15-25 % — économie nette significative."),
        ],
        "wa_text": "Bonjour%2C%20flexfuel%20E85%20Lyon",
        "img_alt": "Reprogrammation flexfuel E85 Lyon — conversion éthanol Rhône 69",
    },
    {
        "file": "service-immo-off.html",
        "slug": "service-immo-off",
        "active": "immo",
        "breadcrumb": "Immo Off — Lyon",
        "badge": "immo off Lyon — antidémarrage 69",
        "icon": "lock",
        "h1": "Immo Off &amp; suppression antidémarrage à Lyon",
        "hero": "<strong class=\"font-semibold text-zinc-200\">Immo off Lyon</strong>, problème antidémarrage, ECU ou BSI verrouillé&nbsp;? Suppression immobiliseur par reprogrammation avec <strong class=\"font-semibold text-zinc-200\">FoxFlash</strong> — dépannage sur Lyon et le Rhône <strong class=\"font-semibold text-zinc-200\">(69)</strong>.",
        "title": "Immo Off Lyon — Suppression antidémarrage & reprogrammation immo | Mecanoo",
        "description": "Immo off Lyon, suppression antidémarrage 69, reprogrammation immo Rhône. FoxFlash — Mecanoo métropole lyonnaise.",
        "keywords": "immo off Lyon, suppression antidémarrage Lyon, reprogrammation immo 69, dépannage immobiliseur Rhône",
        "og_title": "Immo Off Lyon | Mecanoo",
        "og_description": "Suppression antidémarrage et immo off sur Lyon et le 69.",
        "service_name": "Immo Off Lyon",
        "problem_title": "Les problèmes d'antidémarrage (immo)",
        "problem_intro": "Véhicule qui ne démarre plus, clé non reconnue, ECU/BSI remplacé sans codage ou panne circuit immobiliseur.",
        "problems": [
            ("Véhicule ne démarre plus", "Clé reconnue mais moteur coupé immédiatement — voyant immo.", "lock"),
            ("ECU / BSI remplacé", "Calculateur neuf non synchronisé avec clés et immobiliseur.", "cpu"),
            ("Panne circuit immo", "Transpondeur, antenne, câblage ou BSI défaillant.", "alert-triangle"),
            ("Codage concession", "Devis élevé et délais pour simple synchronisation immo.", "euro"),
        ],
        "solution_title": "Immo Off par reprogrammation FoxFlash",
        "solution_intro": "Suppression logicielle de l'immobiliseur dans ECU/BSI — démarrage sans blocage immo, solution définitive.",
        "solution_points": [
            "Immo off ECU et/ou BSI selon architecture",
            "Dépannage après remplacement calculateur",
            "Peugeot, Citroën, Renault, VAG, BMW…",
            "Intervention Lyon, métropole, Rhône (69)",
        ],
        "faq_intro": "« immo off Lyon », « suppression antidémarrage Lyon », « reprogrammation immo 69 »",
        "faqs": [
            ("Mon véhicule ne démarre plus à cause de l'immo : que faire à Lyon ?", "Diagnostic OBD d'abord. Si immo HS ou ECU remplacé, immo off par reprogrammation souvent la solution la plus rapide."),
            ("L'immo off est-il définitif ?", "Oui : suppression gravée dans le calculateur — le véhicule démarre sans vérification immobiliseur."),
            ("Faites-vous l'immo off sur Peugeot et Citroën dans le 69 ?", "Oui : PSA (ECU + BSI), Renault, VAG et autres — sur Lyon et métropole."),
        ],
        "wa_text": "Bonjour%2C%20immo%20off%20Lyon",
        "img_alt": "Immo off Lyon — suppression antidémarrage Rhône 69",
    },
]


def schema_json(s):
    import json
    faqs = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in s["faqs"]]
    graph = [
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Accueil", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": s["service_name"], "item": f"{SITE}/{s['file']}"},
        ]},
        {"@type": "Service", "name": s["service_name"], "description": s["description"],
         "provider": {"@id": f"{SITE}/#localbusiness"}, "areaServed": {"@type": "AdministrativeArea", "name": "Rhône"},
         "url": f"{SITE}/{s['file']}"},
        {"@type": "FAQPage", "mainEntity": faqs},
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)


def problem_cards(problems):
    cards = []
    for title, desc, icon in problems:
        cards.append(f"""          <li class="rounded-2xl border border-white/10 bg-white/[0.02] p-5">
            <div class="mb-3 inline-flex h-10 w-10 items-center justify-center rounded-lg bg-racing/10 text-racing ring-1 ring-racing/20"><i data-lucide="{icon}" class="h-5 w-5"></i></div>
            <h3 class="font-semibold text-white">{title}</h3>
            <p class="mt-2 text-sm text-zinc-400">{desc}</p>
          </li>""")
    return "\n".join(cards)


def solution_points(points):
    icons = ["cpu", "shield-check", "car", "map-pin"]
    rows = []
    for i, p in enumerate(points):
        icon = icons[i % len(icons)]
        rows.append(f'            <li class="flex gap-3"><i data-lucide="{icon}" class="mt-1 h-5 w-5 shrink-0 text-racing"></i><span>{p}</span></li>')
    return "\n".join(rows)


def faq_block(s):
    items = []
    for q, a in s["faqs"]:
        items.append(f"""          <div class="rounded-2xl border border-white/10 bg-white/[0.02] p-6">
            <dt class="font-semibold text-white">{q}</dt>
            <dd class="mt-2 text-zinc-400">{a}</dd>
          </div>""")
    return f"""    <section id="faq" class="border-b border-white/5 bg-ink py-20 sm:py-24" aria-labelledby="faq-heading">
      <div class="mx-auto max-w-3xl px-4 sm:px-6">
        <h2 id="faq-heading" class="text-3xl font-bold tracking-tight text-white sm:text-4xl">Questions fréquentes — {s['service_name']}</h2>
        <p class="mt-4 text-lg text-zinc-400">Recherche Google : {s['faq_intro']}.</p>
        <dl class="mt-10 space-y-6">
{chr(10).join(items)}
        </dl>
      </div>
    </section>"""


def render_head(meta):
    h = HEAD
    for k, v in meta.items():
        h = h.replace("{" + k + "}", v)
    return h


def build_page(s):
    canonical = f"{SITE}/{s['file']}"
    reprog_class = "font-semibold text-racing" if s.get("active") == "hub" else "transition hover:text-racing"
    mobile_reprog = reprog_class.replace("transition hover:text-racing", "text-zinc-300 hover:text-racing")

    head = render_head({
        "description": s["description"], "keywords": s["keywords"], "title": s["title"],
        "canonical": canonical, "og_title": s["og_title"], "og_description": s["og_description"],
        "schema": schema_json(s),
    })

    body = f"""{head}
{NAV.format(reprog_class=reprog_class, mobile_reprog_class=mobile_reprog)}
  <main>
    <nav class="border-b border-white/5 bg-zinc-950/80 px-4 py-3 text-sm text-zinc-500 sm:px-6" aria-label="Fil d'Ariane">
      <div class="mx-auto max-w-6xl">
        <ol class="flex flex-wrap items-center gap-2">
          <li><a href="/" class="text-zinc-400 transition hover:text-racing">Accueil</a></li>
          <li aria-hidden="true">/</li>
          <li><a href="service-reprogrammation.html" class="text-zinc-400 transition hover:text-racing">Reprog ECU</a></li>
          <li aria-hidden="true">/</li>
          <li class="text-zinc-300">{s['breadcrumb']}</li>
        </ol>
      </div>
    </nav>

    <section class="relative overflow-hidden bg-gradient-to-b from-zinc-950 to-ink pb-16 pt-12 sm:pb-24 sm:pt-16 noise-bg">
      <div class="absolute inset-x-0 top-0 h-96 bg-gradient-to-b from-racing/15 to-transparent blur-3xl" aria-hidden="true"></div>
      <div class="relative mx-auto max-w-6xl px-4 sm:px-6 lg:grid lg:grid-cols-5 lg:items-center lg:gap-12">
        <div class="lg:col-span-3">
          <p class="mb-4 inline-flex items-center gap-2 rounded-full border border-racing/30 bg-racing/10 px-3 py-1 text-xs font-semibold uppercase tracking-wider text-racing"><i data-lucide="{s['icon']}" class="h-3.5 w-3.5"></i>&nbsp;{s['badge']}</p>
          <h1 class="mb-6 text-4xl font-extrabold leading-tight tracking-tight text-white sm:text-5xl">{s['h1']}</h1>
          <p class="text-lg text-zinc-400">{s['hero']}</p>
          <div class="mt-8 flex flex-wrap gap-4">
            <a href="tel:+33603439954" class="inline-flex items-center gap-2 rounded-xl bg-racing px-6 py-3 font-semibold text-white shadow-xl shadow-racing/30 transition hover:bg-racing/90"><i data-lucide="phone" class="h-5 w-5"></i>06&nbsp;03&nbsp;43&nbsp;99&nbsp;54</a>
            <a href="/#contact" class="inline-flex items-center gap-2 rounded-xl border border-zinc-600 bg-white/5 px-6 py-3 font-semibold text-zinc-200 transition hover:bg-white/10">Demander un devis<i data-lucide="arrow-right" class="h-5 w-5"></i></a>
          </div>
        </div>
        <div class="mt-10 lg:col-span-2 lg:mt-0">
          <figure class="overflow-hidden rounded-2xl border border-white/10">
            <div class="aspect-[4/5] max-h-[520px] bg-zinc-900/80 sm:aspect-video sm:max-h-none">
              <img src="images/seo-reparation-voiture-lyon_1.jpg" alt="{s['img_alt']}" width="1200" height="800" loading="eager" decoding="async" class="size-full object-cover object-center" />
            </div>
          </figure>
        </div>
      </div>
    </section>

    <section class="border-y border-white/5 bg-zinc-950 py-14 sm:py-20">
      <div class="mx-auto max-w-6xl px-4 sm:px-6">
        <h2 class="text-2xl font-bold tracking-tight text-white sm:text-3xl">{s['problem_title']}</h2>
        <p class="mt-4 max-w-3xl text-zinc-400">{s['problem_intro']}</p>
        <ul class="mt-10 grid gap-6 sm:grid-cols-2">
{problem_cards(s['problems'])}
        </ul>
      </div>
    </section>

    <section class="border-b border-white/5 bg-ink py-14 sm:py-20">
      <div class="mx-auto grid max-w-6xl gap-10 px-4 sm:gap-14 sm:px-6 lg:grid-cols-2 lg:items-start">
        <div>
          <h2 class="text-2xl font-bold tracking-tight text-white sm:text-3xl">{s['solution_title']}</h2>
          <p class="mt-4 text-zinc-400">{s['solution_intro']}</p>
          <ul class="mt-6 space-y-4 text-zinc-300">
{solution_points(s['solution_points'])}
          </ul>
          <div class="mt-8 flex flex-wrap gap-4">
            <a href="https://wa.me/33603439954?text={s['wa_text']}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-2 rounded-xl bg-racing px-6 py-3 font-semibold text-white shadow-xl transition hover:bg-racing/90"><i data-lucide="message-circle" class="h-5 w-5"></i>WhatsApp</a>
            <a href="service-reprogrammation.html" class="inline-flex items-center gap-2 rounded-xl border border-zinc-600 bg-white/5 px-6 py-3 font-semibold text-zinc-200 transition hover:bg-white/10">Toutes nos reprogs<i data-lucide="arrow-right" class="h-5 w-5"></i></a>
          </div>
        </div>
        <div class="rounded-2xl border border-racing/20 bg-racing/5 p-6">
          <h3 class="flex items-center gap-2 font-semibold text-white"><i data-lucide="wrench" class="h-5 w-5 text-racing"></i>Déroulement</h3>
          <ol class="mt-4 space-y-3 text-sm text-zinc-400">
            <li class="flex gap-3"><span class="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-racing/20 text-xs font-bold text-racing">1</span><span>Diagnostic OBD — marque, modèle, motorisation, codes défaut.</span></li>
            <li class="flex gap-3"><span class="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-racing/20 text-xs font-bold text-racing">2</span><span>Devis transparent avant intervention.</span></li>
            <li class="flex gap-3"><span class="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-racing/20 text-xs font-bold text-racing">3</span><span>Reprogrammation FoxFlash — modification définitive.</span></li>
            <li class="flex gap-3"><span class="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-racing/20 text-xs font-bold text-racing">4</span><span>Contrôle et essai — véhicule opérationnel.</span></li>
          </ol>
        </div>
      </div>
    </section>

{faq_block(s)}
{LEGAL}
    <section class="py-14 sm:py-20">
      <div class="mx-auto max-w-3xl px-4 text-center sm:px-6">
        <p class="text-lg font-medium text-white">Besoin d'un devis {s['service_name']} ?</p>
        <p class="mt-3 text-zinc-400">Marque, modèle, année, motorisation — réponse sous 24 h en général.</p>
        <div class="mt-8 flex flex-col items-center justify-center gap-4 sm:flex-row">
          <a href="tel:+33603439954" class="inline-flex items-center gap-2 rounded-xl bg-racing px-8 py-3.5 font-semibold text-white transition hover:bg-racing/90"><i data-lucide="phone" class="h-5 w-5"></i>06&nbsp;03&nbsp;43&nbsp;99&nbsp;54</a>
          <a href="/#contact" class="inline-flex items-center gap-2 rounded-xl border border-zinc-600 bg-white/5 px-8 py-3.5 font-semibold text-zinc-200 transition hover:bg-white/10">Formulaire contact<i data-lucide="arrow-right" class="h-5 w-5"></i></a>
        </div>
      </div>
    </section>
  </main>
{FOOTER.format(wa_text=s['wa_text'])}
"""
    return body


def build_hub():
    cards = []
    hub_items = [
        ("service-adblue.html", "alert-triangle", "AdBlue / SCR", "Problème AdBlue, défaut antipollution Peugeot Citroën, suppression AdBlue 69."),
        ("service-ecu-clonage.html", "cpu", "Clonage ECU", "Copie calculateur moteur, ECU cloning, transfert firmware."),
        ("service-fap.html", "filter", "Suppression FAP", "Filtre à particules saturé, reprogrammation DPF définitive."),
        ("service-egr.html", "wind", "Suppression EGR", "Vanne EGR bloquée, reprogrammation EGR 69."),
        ("service-stage1.html", "zap", "Stage 1", "Reprog moteur, gain puissance et couple."),
        ("service-flexfuel.html", "fuel", "Flexfuel E85", "Conversion éthanol, reprogrammation Flex Fuel."),
        ("service-immo-off.html", "lock", "Immo Off", "Suppression antidémarrage, dépannage immobiliseur."),
    ]
    for href, icon, title, desc in hub_items:
        cards.append(f"""          <article class="group flex flex-col rounded-2xl border border-white/10 bg-gradient-to-br from-zinc-900/80 to-transparent p-6 transition duration-300 hover:-translate-y-1 hover:border-racing/40 hover:shadow-xl hover:shadow-racing/10">
            <div class="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-racing/15 text-racing ring-1 ring-racing/30 transition group-hover:scale-105 group-hover:bg-racing/25"><i data-lucide="{icon}" class="h-6 w-6"></i></div>
            <h3 class="text-lg font-bold text-white">{title}</h3>
            <p class="mt-2 text-sm text-zinc-400">{desc}</p>
            <div class="mt-auto pt-6"><a href="{href}" class="inline-flex items-center gap-1 text-sm font-semibold text-racing hover:underline">En savoir plus<i data-lucide="arrow-right" class="h-4 w-4"></i></a></div>
          </article>""")

    s = {
        "file": "service-reprogrammation.html",
        "description": "Reprogrammation moteur Lyon : AdBlue, FAP, EGR, stage 1, flexfuel E85, immo off, clonage ECU. FoxFlash — Mecanoo Rhône 69.",
        "keywords": "reprogrammation moteur Lyon, reprog ECU Lyon, tuning automobile 69, reprogrammation calculateur Rhône",
        "title": "Reprogrammation moteur Lyon — Reprog ECU & tuning | Mecanoo",
        "canonical": f"{SITE}/service-reprogrammation.html",
        "og_title": "Reprogrammation moteur Lyon | Mecanoo",
        "og_description": "AdBlue, FAP, EGR, stage 1, flexfuel, immo off, clonage ECU — reprog FoxFlash sur Lyon et le 69.",
    }
    import json
    schema = json.dumps({"@context": "https://schema.org", "@graph": [
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Accueil", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Reprogrammation ECU Lyon", "item": s["canonical"]},
        ]},
        {"@type": "Service", "name": "Reprogrammation moteur et ECU Lyon", "description": s["description"],
         "provider": {"@id": f"{SITE}/#localbusiness"}, "url": s["canonical"]},
    ]}, ensure_ascii=False)

    head = render_head({
        "description": s["description"], "keywords": s["keywords"], "title": s["title"],
        "canonical": s["canonical"], "og_title": s["og_title"], "og_description": s["og_description"],
        "schema": schema,
    })
    return f"""{head}
{NAV.format(reprog_class="font-semibold text-racing", mobile_reprog_class="font-semibold text-racing")}
  <main>
    <nav class="border-b border-white/5 bg-zinc-950/80 px-4 py-3 text-sm text-zinc-500 sm:px-6" aria-label="Fil d'Ariane">
      <div class="mx-auto max-w-6xl">
        <ol class="flex flex-wrap items-center gap-2">
          <li><a href="/" class="text-zinc-400 transition hover:text-racing">Accueil</a></li>
          <li aria-hidden="true">/</li>
          <li class="text-zinc-300">Reprogrammation ECU — Lyon</li>
        </ol>
      </div>
    </nav>
    <section class="relative overflow-hidden bg-gradient-to-b from-zinc-950 to-ink pb-16 pt-12 sm:pb-24 sm:pt-16 noise-bg">
      <div class="absolute inset-x-0 top-0 h-96 bg-gradient-to-b from-racing/15 to-transparent blur-3xl" aria-hidden="true"></div>
      <div class="relative mx-auto max-w-6xl px-4 sm:px-6">
        <p class="mb-4 inline-flex items-center gap-2 rounded-full border border-racing/30 bg-racing/10 px-3 py-1 text-xs font-semibold uppercase tracking-wider text-racing"><i data-lucide="cpu" class="h-3.5 w-3.5"></i>&nbsp;reprogrammation ECU Lyon — 69</p>
        <h1 class="mb-6 max-w-4xl text-4xl font-extrabold leading-tight tracking-tight text-white sm:text-5xl">Reprogrammation moteur &amp; solutions électroniques à Lyon</h1>
        <p class="max-w-3xl text-lg text-zinc-400"><strong class="font-semibold text-zinc-200">Reprog ECU Lyon</strong> : AdBlue, FAP, EGR, stage 1, flexfuel E85, immo off et clonage calculateur — outils officiels <strong class="font-semibold text-zinc-200">FoxFlash</strong>, intervention sur Lyon et le Rhône <strong class="font-semibold text-zinc-200">(69)</strong>.</p>
        <div class="mt-8 flex flex-col gap-4 sm:flex-row">
          <a href="/#contact" class="inline-flex items-center justify-center gap-2 rounded-xl bg-racing px-6 py-3 text-base font-semibold text-white shadow-xl shadow-racing/30 transition hover:bg-racing/90">Demander un devis reprog<i data-lucide="arrow-right" class="h-5 w-5"></i></a>
          <a href="https://wa.me/33603439954?text=Bonjour%2C%20reprog%20ECU%20Lyon" target="_blank" rel="noopener noreferrer" class="inline-flex items-center justify-center gap-2 rounded-xl border border-zinc-600 bg-white/5 px-6 py-3 font-semibold text-zinc-200 transition hover:bg-white/10">WhatsApp</a>
        </div>
      </div>
    </section>
    <section class="border-y border-white/5 bg-zinc-950 py-14 sm:py-20">
      <div class="mx-auto max-w-6xl px-4 sm:px-6">
        <h2 class="text-2xl font-bold tracking-tight text-white sm:text-3xl">Nos prestations reprogrammation</h2>
        <p class="mt-4 max-w-2xl text-zinc-400">Chaque service dispose d'une page dédiée optimisée SEO — cliquez pour en savoir plus.</p>
        <div class="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
{chr(10).join(cards)}
        </div>
      </div>
    </section>
    <section class="border-t border-white/5 bg-ink py-14 sm:py-20">
      <div class="mx-auto max-w-3xl px-4 text-center sm:px-6">
        <p class="text-lg font-medium text-white">Un projet de <strong class="font-semibold text-zinc-200">reprogrammation ECU</strong> sur Lyon ou le 69&nbsp;?</p>
        <p class="mt-3 text-zinc-400">Indiquez marque, modèle, motorisation et type de prestation — réponse sous 24&nbsp;h en général.</p>
        <a href="/#contact" class="mt-8 inline-flex items-center gap-2 rounded-xl bg-racing px-8 py-3.5 font-semibold text-white transition hover:bg-racing/90">Formulaire ou devis<i data-lucide="arrow-right" class="h-5 w-5"></i></a>
      </div>
    </section>
{LEGAL}
  </main>
{FOOTER.format(wa_text="Bonjour%2C%20reprog%20ECU%20Lyon")}
"""


if __name__ == "__main__":
    for svc in SERVICES:
        out = BASE / svc["file"]
        out.write_text(build_page(svc), encoding="utf-8")
        print(f"Generated {out.name}")
    hub = BASE / "service-reprogrammation.html"
    hub.write_text(build_hub(), encoding="utf-8")
    print(f"Generated {hub.name}")
