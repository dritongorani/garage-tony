#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate SEO service pages for mecanolyon.fr — Électronique Automobile & Diagnostic"""

from pathlib import Path

BASE = Path(__file__).parent
SITE = "https://mecanolyon.fr"

HEAD = """<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8" />
  <script src="{prefix}assets/canonical-host.js"></script>
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-6NPKTDZMM4"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-6NPKTDZMM4');</script>
  <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','GTM-TMZK9J9X');</script>
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="{description}" />
  <meta name="keywords" content="{keywords}" />
  <meta name="author" content="Mecanoo Lyon" />
  <meta name="robots" content="index, follow, max-image-preview:large" />
  <meta name="geo.region" content="FR-69" />
  <meta name="geo.placename" content="Lyon" />
  <meta name="geo.position" content="45.764;4.8357" />
  <meta name="ICBM" content="45.764, 4.8357" />
  <title>{title}</title>
  <link rel="canonical" href="{canonical}" />
  <link rel="alternate" hreflang="fr-FR" href="{canonical}" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:title" content="{og_title}" />
  <meta property="og:description" content="{og_description}" />
  <meta property="og:locale" content="fr_FR" />
  <meta property="og:site_name" content="Mecanoo Lyon" />
  <meta property="og:image" content="https://mecanolyon.fr/images/seo-reparation-voiture-lyon_1.jpg" />
  <meta property="og:image:width" content="1264" />
  <meta property="og:image:height" content="848" />
  <meta property="og:image:alt" content="Mecanoo Lyon — électronique automobile & diagnostic à Lyon" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:image" content="https://mecanolyon.fr/images/seo-reparation-voiture-lyon_1.jpg" />
  <meta name="twitter:image:alt" content="Mecanoo Lyon — électronique automobile & diagnostic à Lyon" />
  <meta name="theme-color" content="#0a0c0f" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
  <script src="https://cdn.tailwindcss.com"></script>
  <script>tailwind.config={theme:{extend:{colors:{racing:'#FF5733',racingStrong:'#D03F14',ink:'#0a0c0f'},fontFamily:{sans:['Inter','system-ui','sans-serif']}}}};</script>
  <style>
    html{scroll-behavior:smooth;}
    section[id]{scroll-margin-top:5rem;}
    :is(a,button,[tabindex]):focus-visible{outline:2px solid #FF5733;outline-offset:2px;border-radius:6px;}
    .glass-nav{background:rgba(10,12,15,0.72);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border-bottom:1px solid rgba(255,255,255,0.06);}
    .noise-bg::before{content:'';position:absolute;inset:0;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");pointer-events:none;}
  </style>
  <script type="application/ld+json">{schema}</script>
</head>
<body class="bg-ink font-sans text-zinc-100 antialiased">
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-TMZK9J9X" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
"""

# ---------------------------------------------------------------------------
# Composant de navigation — SOURCE UNIQUEE
# ---------------------------------------------------------------------------
# Le markup de la nav n'existe qu'à un seul endroit : partials/navbar.html.
# Il est injecté :
#   1. dans les pages générées par render_nav() / build_page() ;
#   2. dans les pages écrites à la main, entre les marqueurs
#      <!-- nav:begin --> ... <!-- nav:end --> (index, zone-intervention).
# Contrainte du partial : aucun accolade littérale (rendu via str.format),
# uniquement les tokens produits par nav_tokens().
NAV_PATH = BASE / "partials" / "navbar.html"
NAV = "\n" + NAV_PATH.read_text(encoding="utf-8")

NAV_BEGIN = "<!-- nav:begin — source : partials/navbar.html (généré, ne pas éditer ici) -->"
NAV_END = "<!-- nav:end -->"

# Pages écrites à la main dont la nav est injectée depuis le partial.
# `on_home=True` bascule les ancres vers la page courante (#faq au lieu de index.html#faq).
NAV_PAGES = {
    "index.html": {"active": None, "on_home": True},
    "zone-intervention.html": {"active": "zone", "on_home": False},
}


def nav_tokens(active=None, on_home=False, prefix=""):
    """Tokens du partial navbar.html : lien surligné par pilier + ancres de page.

    active   : pilier courant — "diagnostic" | "abs" | "ecu" | "reprog"
               | "antipollution" | "keys" | "zone" | None (aucun).
    on_home  : True sur index.html — les liens #services/#faq/#contact restent
               sur la page courante au lieu de rebondir vers index.html.
    prefix   : préfixe des liens internes — "" à la racine, "/" depuis un
               sous-dossier (services/…). Les pages d'un sous-dossier ne
               peuvent pas porter de liens relatifs (assets/, images/…).
    """
    def cls(key):
        return ACTIVE_CLASS if active == key else BASE_CLASS

    def mcls(key):
        return MOBILE_ACTIVE_CLASS if active == key else MOBILE_BASE_CLASS

    home_href = prefix + ("index.html#hero" if on_home else "index.html")
    anchor = "" if on_home else prefix + "index.html"

    return {
        "diag_class": cls("diagnostic"),
        "abs_class": cls("abs"),
        "ecu_class": cls("ecu"),
        "reprog_class": cls("reprog"),
        "anti_class": cls("antipollution"),
        "zone_class": cls("zone"),
        "mobile_diag_class": mcls("diagnostic"),
        "mobile_abs_class": mcls("abs"),
        "mobile_ecu_class": mcls("ecu"),
        "mobile_reprog_class": mcls("reprog"),
        "mobile_anti_class": mcls("antipollution"),
        "mobile_zone_class": mcls("zone"),
        # Pilier « Clés & électronique » : classe de remplacement (pas de
        # conflit de précédence avec la couleur statique du bouton).
        "keys_class": ACTIVE_CLASS if active == "keys" else "font-medium text-zinc-300",
        "mobile_keys_class": MOBILE_ACTIVE_CLASS if active == "keys" else "text-zinc-300",
        "keys_hub_href": f"{prefix}services/",
        "prefix": prefix,
        "home_href": home_href,
        "services_href": f"{anchor}#services",
        "faq_href": f"{anchor}#faq",
        "contact_href": f"{anchor}#contact",
    }


def render_nav(active=None, on_home=False, prefix=""):
    """Rend le partial de nav (str.format lève KeyError si un token manque)."""
    return NAV.format(**nav_tokens(active, on_home, prefix))


def sync_nav_pages():
    """Réinjecte partials/navbar.html dans les pages écrites à la main.

    Échoue brutalement si les marqueurs nav:begin / nav:end sont absents ou
    ambigus : jamais de réécriture silencieuse hors marqueurs.
    """
    import re

    pattern = re.compile(re.escape(NAV_BEGIN) + r".*?" + re.escape(NAV_END), re.S)
    for name, cfg in NAV_PAGES.items():
        path = BASE / name
        text = path.read_text(encoding="utf-8")
        nav_html = render_nav(**cfg).strip("\n")  # strip("\n") : strip() avalerait l'indentation du <header>
        block = f"{NAV_BEGIN}\n{nav_html}\n{NAV_END}"
        text, count = pattern.subn(lambda _m: block, text)
        if count != 1:
            raise SystemExit(
                f"ERREUR : {name} — marqueurs nav:begin / nav:end introuvables "
                f"ou ambigus (occurrences : {count}).\n"
                f"Reposer les marqueurs autour du <header> puis relancer."
            )
        if text != path.read_text(encoding="utf-8"):
            path.write_text(text, encoding="utf-8")
        print(f"Synced navbar → {name}")


FOOTER = """
  <footer class="border-t border-white/10 bg-black/40 py-12 pb-28 sm:pb-12">
    <div class="mx-auto flex max-w-6xl flex-col items-start justify-between gap-6 px-4 sm:flex-row sm:items-start sm:px-6">
      <div>
        <p class="text-sm text-zinc-400">© <span id="year"></span> Mecanoo Lyon. Tous droits réservés.</p>
        <p class="mt-2 text-sm text-zinc-400"><a href="{prefix}service-diagnostic.html" class="text-racing hover:underline">Diagnostic</a> · <a href="{prefix}service-abs.html" class="hover:text-zinc-300 hover:underline">Bloc ABS</a> · <a href="{prefix}service-airbag.html" class="hover:text-zinc-300 hover:underline">Airbag</a> · <a href="{prefix}service-ecu-clonage.html" class="hover:text-zinc-300 hover:underline">Calculateurs ECU/BSI</a> · <a href="{prefix}service-reprogrammation.html" class="hover:text-zinc-300 hover:underline">Reprog moteur</a> · <a href="{prefix}service-antipollution.html" class="hover:text-zinc-300 hover:underline">Anti-pollution</a> · <a href="{prefix}zone-intervention.html" class="hover:text-zinc-300 hover:underline">Zone Lyon &amp; Ain</a> · <a href="{prefix}index.html#contact" class="hover:text-zinc-300 hover:underline">Contact</a>.</p>
        <p class="mt-2 text-sm text-zinc-400"><span class="font-medium text-zinc-300">Services clés auto &amp; électronique&nbsp;:</span> <a href="{prefix}services/reproduction-cles-auto/" class="hover:text-zinc-300 hover:underline">Reproduction de clés</a> · <a href="{prefix}services/perte-totale-cles-lyon/" class="hover:text-zinc-300 hover:underline">Perte totale de clés</a> · <a href="{prefix}services/ouverture-vehicule-sans-cle/" class="hover:text-zinc-300 hover:underline">Ouverture de véhicule</a> · <a href="{prefix}services/programmation-electronique-ecu/" class="hover:text-zinc-300 hover:underline">Programmation ECU</a> · <a href="{prefix}services/" class="hover:text-zinc-300 hover:underline">Tous les services clés</a>.</p>
      </div>
      <div class="flex flex-col items-start gap-3 sm:items-end">
        <p class="text-xs text-zinc-400 uppercase tracking-wide text-left sm:text-right">Diagnostic &amp; électronique automobile — Lyon · 69 · Ain 01</p>
        <a href="https://wa.me/33603439954" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-2 rounded-full border border-[#25D366]/35 bg-[#25D366]/15 px-4 py-2 text-sm font-medium text-emerald-300 transition hover:bg-[#25D366]/25">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="h-5 w-5" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.435 9.884-9.883 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
          WhatsApp +33&nbsp;6&nbsp;03&nbsp;43&nbsp;99&nbsp;54
        </a>
      </div>
    </div>
  </footer>
  <a href="https://wa.me/33603439954?text={wa_text}" target="_blank" rel="noopener noreferrer" class="fixed {fab_pos} right-5 z-[60] flex h-14 w-14 items-center justify-center rounded-full bg-[#25D366] text-white shadow-2xl shadow-black/40 ring-2 ring-black/40 transition hover:scale-105 md:bottom-8 md:right-8" aria-label="WhatsApp"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="h-8 w-8"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.435 9.884-9.883 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg></a>
  <script src="https://unpkg.com/lucide@latest"></script>
  <script>lucide.createIcons();document.getElementById('year').textContent=new Date().getFullYear();var b=document.getElementById('mobile-menu-btn'),m=document.getElementById('mobile-menu');if(b&&m)b.addEventListener('click',function(){{m.classList.toggle('hidden');b.setAttribute('aria-expanded',String(!m.classList.contains('hidden')));}});</script>
</body>
</html>
"""

LEGAL = """
    <section class="border-b border-white/5 bg-zinc-950 py-10 sm:py-12" aria-label="Mention légale">
      <div class="mx-auto max-w-3xl px-4 sm:px-6">
        <p class="text-xs leading-relaxed text-zinc-400">
          <strong class="font-medium text-zinc-300">Mention légale&nbsp;:</strong> la modification ou la désactivation de systèmes antipollution (AdBlue, SCR, FAP, EGR…) et toute reprogrammation moteur (stage, flexfuel) est strictement réservée à un usage <strong class="font-medium text-zinc-300">hors voie publique</strong> — circuit, piste privée ou usage professionnel hors route ouverte à la circulation. L'utilisation d'un véhicule modifié sur la voie publique est interdite par la réglementation en vigueur. Mecanoo informe ses clients de ces contraintes légales avant toute intervention.
        </p>
      </div>
    </section>
"""

# ---------------------------------------------------------------------------
# Catalogue des services (feuilles) — chacun dispose d'une page dédiée SEO
# ---------------------------------------------------------------------------

SERVICES = [
    {
        "file": "service-diagnostic.html",
        "slug": "service-diagnostic",
        "active": "diagnostic",
        "parent_label": None,
        "parent_url": None,
        "hub_url": "index.html#services",
        "hub_label": "Toutes nos prestations",
        "breadcrumb": "Diagnostic électronique — Lyon",
        "badge": "diagnostic valise Lyon — OBD 69 / Ain 01",
        "icon": "scan-line",
        "h1": "Diagnostic électronique &amp; valise OBD à Lyon",
        "hero": "<strong class=\"font-semibold text-zinc-200\">Diagnostic électronique Lyon</strong>&nbsp;: lecture des codes défaut moteur, boîte, ABS et airbag avec <strong class=\"font-semibold text-zinc-200\">valise OBD multimarque</strong> — rapport complet et devis avant intervention sur Lyon, Rhône <strong class=\"font-semibold text-zinc-200\">(69)</strong> et Ain <strong class=\"font-semibold text-zinc-200\">(01)</strong>.",
        "title": "Diagnostic Électronique Lyon — Valise OBD | Mecanoo",
        "description": "Diagnostic électronique à Lyon : valise OBD multimarque, lecture codes défaut moteur, boîte, ABS et airbag. Rapport et devis — Rhône (69) et Ain (01).",
        "keywords": "diagnostic électronique Lyon, diagnostic valise Lyon, lecture codes défaut Lyon, diagnostic auto OBD 69, diagnostic automobile Ain 01",
        "og_title": "Diagnostic électronique Lyon — Valise OBD | Mecanoo",
        "og_description": "Diagnostic valise OBD multimarque à Lyon, Rhône (69) et Ain (01) — codes défaut moteur, boîte, ABS, airbag.",
        "service_name": "Diagnostic électronique Lyon",
        "step3": "Rapport détaillé des codes défaut et proposition de réparation chiffrée.",
        "problem_title": "Quand faire un diagnostic électronique automobile ?",
        "problem_intro": "Voyant moteur, mode dégradé, consommation anormale ou bruit suspect — la valise OBD identifie l'origine électronique avant toute réparation, évitant les devis à l'aveugle.",
        "problems": [
            ("Voyant moteur allumé", "Code défaut moteur (P0xxx) à lire et interpréter avant toute réparation.", "alert-triangle"),
            ("Mode dégradé", "Véhicule bridé, puissance limitée — origine électronique à identifier rapidement.", "gauge"),
            ("Voyants ABS / ESP / airbag", "Calculateurs annexes à diagnostiquer (freinage, stabilité, sécurité passive).", "shield-alert"),
            ("Devis aveugle", "Sans diagnostic valise, les réparations se font à l'aveugle et coûtent cher.", "euro"),
        ],
        "solution_title": "Diagnostic valise OBD multimarque",
        "solution_intro": "Lecture et interprétation de tous les calculateurs du véhicule, rapport détaillé avec préconisations et devis transparent avant toute intervention.",
        "solution_points": [
            "Valise OBD multimarque — essence, diesel, hybride",
            "Lecture et effacement codes défaut moteur, boîte, ABS, airbag",
            "Rapport écrit avec préconisations et devis",
            "Intervention à domicile Lyon, Rhône (69) et Ain (01)",
        ],
        "faq_intro": "« diagnostic valise Lyon », « voyant ABS allumé Lyon », « lecture codes défaut Lyon »",
        "faqs": [
            ("Que fait un diagnostic électronique automobile ?", "La valise OBD se connecte au calculateur, lit les codes défaut enregistrés (moteur, boîte, ABS, airbag), permet de cibler la panne puis d'effacer les codes après réparation."),
            ("Combien coûte un diagnostic valise à Lyon ?", "Tarif selon véhicule et périmètre (moteur seul ou diagnostic complet) — devis après marque et modèle. Souvent déduit du montant de la réparation."),
            ("Diagnostic sur Peugeot, Citroën, Renault, BMW à Lyon ?", "Oui, valise multimarque essence / diesel / hybride sur Lyon, la métropole, le Rhône (69) et l'Ain (01)."),
        ],
        "wa_text": "Bonjour%2C%20diagnostic%20%C3%A9lectronique%20Lyon",
        "img_alt": "Diagnostic électronique automobile à Lyon — valise OBD Rhône 69 et Ain 01",
        "related_links": [
            ("service-airbag.html", "Réparation airbag — voyant airbag allumé"),
            ("service-abs.html", "Réparation bloc ABS — voyant ABS allumé"),
            ("service-ecu-clonage.html", "Calculateurs ECU/BSI"),
        ],
    },
    {
        "file": "service-abs.html",
        "slug": "service-abs",
        "active": "abs",
        "parent_label": "Diagnostic électronique",
        "parent_url": "service-diagnostic.html",
        "hub_url": "service-diagnostic.html",
        "hub_label": "Diagnostic électronique",
        "breadcrumb": "Réparation bloc ABS — Lyon",
        "badge": "réparation bloc ABS Lyon — voyant ABS 69 / Ain 01",
        "icon": "shield-alert",
        "h1": "Réparation bloc ABS &amp; voyant ABS allumé à Lyon",
        "hero": "<strong class=\"font-semibold text-zinc-200\">Réparation bloc ABS Lyon</strong>&nbsp;: <strong class=\"font-semibold text-zinc-200\">voyant ABS allumé</strong>, capteur de roue défaillant ou pompe de frein — diagnostic du circuit antiblocage, test des capteurs et réparation à domicile sur Lyon, Rhône <strong class=\"font-semibold text-zinc-200\">(69)</strong> et Ain <strong class=\"font-semibold text-zinc-200\">(01)</strong>.",
        "title": "Réparation Bloc ABS Lyon — Voyant ABS allumé | Mecanoo",
        "description": "Voyant ABS allumé à Lyon ? Diagnostic et réparation du bloc ABS, capteurs de roues et pompe de frein — intervention à domicile, Rhône (69) et Ain (01).",
        "keywords": "réparation bloc ABS Lyon, voyant ABS allumé, bloc ABS Lyon, capteur de roue ABS 69, diagnostic freinage ABS Lyon, dépannage ABS Ain 01",
        "og_title": "Réparation bloc ABS Lyon — Voyant ABS allumé | Mecanoo",
        "og_description": "Voyant ABS allumé à Lyon ? Diagnostic et réparation bloc ABS, capteurs de roues — Rhône (69) et Ain (01).",
        "service_name": "Réparation bloc ABS Lyon",
        "service_type": "Réparation bloc ABS, capteurs de roue & diagnostic freinage (ABS/ESP/ESC)",
        "step3": "Réparation bloc ABS / capteur de roue — effacement des codes défaut et essai routier.",
        "problem_title": "Voyant ABS allumé — les causes fréquentes",
        "problem_intro": "Capteur de roue, bloc hydraulique ABS, connectique ou liquide de frein&nbsp;: le voyant ABS s'allume dès qu'un défaut est détecté sur le circuit antiblocage. Le diagnostic valise freinage passe avant le remplacement de toute pièce.",
        "problems": [
            ("Voyant ABS allumé", "Défaut enregistré sur le circuit antiblocage — codes C0xxx à lire en priorité.", "alert-triangle"),
            ("Capteur de roue défaillant", "Panne la plus fréquente : signal de vitesse de roue absent ou erratique.", "gauge"),
            ("Bloc / pompe ABS défaillant", "Bloc hydraulique calé ou moteur de pompe — remplacement onéreux en concession.", "settings"),
            ("ABS et ESP désactivés", "Freinage dégradé, pédale dure ou freinage inégal — sécurité à ne pas négliger.", "shield-alert"),
        ],
        "solution_title": "Réparation bloc ABS &amp; capteurs de roue",
        "solution_intro": "Diagnostic du système antiblocage, test des quatre capteurs de vitesse de roue, contrôle de la connectique et de la pompe — réparation ciblée avec devis avant intervention.",
        "solution_points": [
            "Lecture des codes défaut ABS / ESP / ESC (C0xxx)",
            "Test des capteurs de vitesse de roue un par un",
            "Réparation ou remplacement du bloc ABS / pompe hydraulique",
            "Intervention à domicile Lyon, Rhône (69) et Ain (01)",
        ],
        "faq_intro": "« réparation bloc ABS Lyon », « voyant ABS allumé », « capteur de roue ABS 69 »",
        "faqs": [
            ("Pourquoi mon voyant ABS est-il allumé à Lyon ?", "Un défaut sur le circuit antiblocage : capteur de roue, bloc ou pompe ABS, connectique ou liquide de frein. Le diagnostic valise freinage lit les codes C0xxx pour cibler la panne avant toute pièce."),
            ("Combien coûte une réparation de bloc ABS ?", "Capteur de roue : souvent modeste, une centaine d'euros posé. Bloc ou pompe ABS complet : plusieurs centaines d'euros, bien plus en concession — devis après diagnostic sur Lyon et le 69."),
            ("Peut-on rouler avec le voyant ABS allumé ?", "Le freinage classique reste fonctionnel, mais l'ABS et souvent l'ESP sont désactivés : sécurité réduite en freinage d'urgence. Intervention Mecanoo sur Lyon, Rhône (69) et Ain (01)."),
        ],
        "wa_text": "Bonjour%2C%20voyant%20ABS%20allum%C3%A9%20Lyon",
        "img_alt": "Réparation bloc ABS à Lyon — voyant ABS allumé, diagnostic freinage Rhône 69",
        "related_links": [
            ("service-airbag.html", "Réparation airbag — voyant airbag allumé"),
            ("service-diagnostic.html", "Diagnostic électronique &amp; valise OBD"),
            ("zone-intervention.html", "Zone d'intervention — Lyon, 69 &amp; Ain 01"),
        ],
        # --- Habillage UI spécifique à la page ABS (sections optionnelles) ---
        "cards_modern": True,
        "sticky_cta": True,
        "reassurance": [
            ("shield-check", "Garantie de réparation", "Pièces et main-d'œuvre — suivi assuré après l'intervention."),
            ("timer", "Intervention rapide", "Diagnostic ciblé le jour même si disponible, réponse sous 24 h."),
            ("file-text", "Devis gratuit", "Chiffrage validé par vous avant toute dépose de pièce."),
            ("map-pin", "Intervention à domicile", "Lyon, Rhône (69) et Ain (01) — on vient à vous."),
        ],
        "process_kicker": "Notre méthode",
        "process_title": "La réparation de bloc ABS en 4 étapes",
        "process_intro": "Aucune pièce remplacée à l'aveugle&nbsp;: le bloc ABS n'est déposé qu'après diagnostic, et chaque étape est validée avec vous avant de passer à la suivante.",
        "process": [
            ("Diagnostic freinage", "scan-line", "Lecture des codes défaut ABS / ESP / ESC (C0xxx) et test individuel des quatre capteurs de vitesse de roue&nbsp;: la cause réelle est identifiée avant toute dépose."),
            ("Démontage &amp; réparation", "wrench", "Dépose du bloc hydraulique ou du capteur défaillant, réparation ciblée ou remplacement compatible, connectique, raccordements et niveau de liquide contrôlés."),
            ("Test au banc", "activity", "Contrôle du bloc et des capteurs au banc, purge du circuit de freinage, effacement des codes défaut puis essai routier pour valider le freinage."),
            ("Garantie &amp; suivi", "shield-check", "Réparation couverte par notre garantie, compte-rendu des opérations remis et disponibilité par téléphone ou WhatsApp en cas de question."),
        ],
        "cta": {
            "kicker": "Voyant ABS allumé&nbsp;? Appelez maintenant",
            "title": "Un doute sur votre freinage&nbsp;? Un appel suffit pour cadrer la réparation.",
            "text": "Décrivez les symptômes (voyant ABS, pédale dure, code défaut affiché)&nbsp;: nous vous donnons une première orientation et un créneau d'intervention — <strong class=\"font-semibold text-zinc-200\">devis gratuit avant toute dépose</strong>.",
            "points": ["Devis gratuit", "Garantie de réparation", "Rapidité d'intervention", "À domicile Lyon &amp; 69"],
        },
    },
    {
        "file": "service-airbag.html",
        "slug": "service-airbag",
        "active": "diagnostic",
        "parent_label": "Diagnostic électronique",
        "parent_url": "service-diagnostic.html",
        "hub_url": "service-diagnostic.html",
        "hub_label": "Diagnostic électronique",
        "breadcrumb": "Réparation airbag — Lyon",
        "badge": "réparation airbag Lyon — voyant airbag 69 / Ain 01",
        "icon": "shield-check",
        "h1": "Réparation airbag &amp; voyant airbag allumé à Lyon",
        "hero": "<strong class=\"font-semibold text-zinc-200\">Réparation airbag Lyon</strong>&nbsp;: <strong class=\"font-semibold text-zinc-200\">voyant airbag allumé</strong>, contacteur rotatif de volant ou connecteur sous siège — diagnostic du système SRS, test des prétensionneurs et réparation à domicile sur Lyon, Rhône <strong class=\"font-semibold text-zinc-200\">(69)</strong> et Ain <strong class=\"font-semibold text-zinc-200\">(01)</strong>.",
        "title": "Réparation Airbag Lyon — Voyant airbag allumé | Mecanoo",
        "description": "Voyant airbag allumé à Lyon ? Diagnostic SRS, contacteur rotatif et prétensionneurs — réparation airbag à domicile, Rhône (69) et Ain (01).",
        "keywords": "réparation airbag Lyon, voyant airbag allumé, contacteur rotatif volant Lyon, prétensionneur 69, diagnostic SRS Lyon, airbag Ain 01",
        "og_title": "Réparation Airbag Lyon — Voyant airbag allumé | Mecanoo",
        "og_description": "Voyant airbag allumé à Lyon ? Diagnostic SRS et contacteur rotatif — réparation airbag à domicile, Rhône (69) et Ain (01).",
        "service_name": "Réparation airbag Lyon",
        "service_type": "Réparation airbag, contacteur rotatif & prétensionneurs — diagnostic système SRS",
        "step3": "Remplacement de la pièce défaillante, effacement des codes SRS et contrôle du voyant airbag.",
        "problem_title": "Voyant airbag allumé — les causes fréquentes",
        "problem_intro": "Contacteur rotatif, connecteur sous siège, prétensionneur ou capteur de choc&nbsp;: le témoin SRS s'allume dès qu'un défaut est enregistré dans le calculateur d'airbag. Le diagnostic valise SRS passe avant toute dépose.",
        "problems": [
            ("Voyant airbag allumé", "Défaut enregistré dans le calculateur SRS — codes B0xxx à lire en priorité.", "alert-triangle"),
            ("Contacteur rotatif de volant", "Courant porté sur les touchez-commandes et l'airbag volant : contact intermittent.", "rotate-cw"),
            ("Connecteur sous siège", "Connecteur mal positionné ou corrodé — cause la plus fréquente et la moins onéreuse.", "plug"),
            ("Capteur de choc / prétensionneur", "Élément pyrotechnique ou capteur hors service : remplacement pièce par pièce.", "shield-alert"),
        ],
        "solution_title": "Réparation airbag &amp; contrôle du système SRS",
        "solution_intro": "Lecture des codes défaut airbag, test des prétensionneurs et de la connectique (volant, sièges, portières), remplacement ciblé de la pièce défaillante — devis avant toute intervention.",
        "solution_points": [
            "Lecture et effacement des codes défaut airbag / SRS (B0xxx)",
            "Test du contacteur rotatif et de la connectique volant, sièges, portières",
            "Remplacement du contacteur, capteur ou prétensionneur défaillant",
            "Intervention à domicile Lyon, Rhône (69) et Ain (01)",
        ],
        "faq_intro": "« voyant airbag allumé Lyon », « réparation airbag 69 », « contacteur rotatif volant Lyon »",
        "faqs": [
            ("Pourquoi mon voyant airbag est-il allumé ?", "Défaut sur le système SRS : contacteur rotatif du volant, connecteur sous siège, prétensionneur, capteur de choc ou bougie pyrotechnique. La valise lit les codes B0xxx pour cibler la panne avant toute dépose."),
            ("Est-il risqué de rouler avec le voyant airbag allumé ?", "L'airbag peut ne pas se déclencher en cas de choc et certains prétensionneurs sont concernés : roulez prudemment et faites diagnostiquer le système SRS rapidement. Le circuit pyrotechnique n'est jamais manipulé sans consigne constructeur (batterie débranchée, délai de vidage respecté)."),
            ("Combien coûte une réparation d'airbag à Lyon ?", "Contacteur rotatif : pièce et pose généralement abordables. Capteur, déclencheur ou prétensionneur : selon la marque et la disponibilité de la pièce — devis après diagnostic sur Lyon, le 69 et l'Ain (01)."),
        ],
        "wa_text": "Bonjour%2C%20voyant%20airbag%20allum%C3%A9%20Lyon",
        "img_alt": "Réparation airbag à Lyon — voyant airbag allumé, diagnostic système SRS Rhône 69",
        "related_links": [
            ("service-diagnostic.html", "Diagnostic électronique &amp; valise OBD"),
            ("service-abs.html", "Réparation bloc ABS — voyant ABS allumé"),
        ],
        # --- Habillage UI spécifique à la page Airbag (sections optionnelles) ---
        "cards_modern": True,
        "sticky_cta": True,
        "reassurance": [
            ("shield-check", "Circuit pyrotechnique sécurisé", "Consignes constructeur appliquées — aucune pièce déposée sans précaution."),
            ("timer", "Intervention rapide", "Diagnostic SRS ciblé le jour même si disponible, réponse sous 24 h."),
            ("file-text", "Devis gratuit", "Chiffrage validé par vous avant toute dépose de pièce."),
            ("map-pin", "Intervention à domicile", "Lyon, Rhône (69) et Ain (01) — on vient à vous."),
        ],
        "process_kicker": "Notre méthode",
        "process_title": "La réparation d'airbag en 4 étapes",
        "process_intro": "Aucun élément pyrotechnique n'est déposé à l'aveugle&nbsp;: le calculateur SRS est diagnostiqué d'abord, et chaque étape est validée avec vous avant de passer à la suivante.",
        "process": [
            ("Diagnostic SRS", "scan-line", "Lecture des codes défaut airbag / SRS (B0xxx), vérification des prétensionneurs, du contacteur rotatif et des connecteurs&nbsp;: la cause réelle est identifiée avant toute dépose."),
            ("Mise en sécurité", "shield-check", "Batterie débranchée et délai de vidage respecté avant toute intervention sur le circuit pyrotechnique, conformément aux consignes constructeur."),
            ("Remplacement ciblé", "wrench", "Dépose du contacteur rotatif, du capteur ou du prétensionneur défaillant, remplacement compatible, repose et contrôle des connecteurs."),
            ("Effacement &amp; contrôle", "activity", "Effacement des codes défaut, vérification du voyant airbag au contacteur puis contrôle final&nbsp;: le témoin SRS reste éteint."),
        ],
        "cta": {
            "kicker": "Voyant airbag allumé&nbsp;? Appelez maintenant",
            "title": "Un doute sur votre sécurité passive&nbsp;? Un appel suffit pour cadrer l'intervention.",
            "text": "Décrivez les symptômes (voyant airbag, contacteur de volant, code défaut affiché)&nbsp;: nous vous donnons une première orientation et un créneau d'intervention — <strong class=\"font-semibold text-zinc-200\">devis gratuit avant toute dépose</strong>.",
            "points": ["Devis gratuit", "Circuit pyrotechnique sécurisé", "Rapidité d'intervention", "À domicile Lyon &amp; 69"],
        },
    },
    {
        "file": "service-ecu-clonage.html",
        "slug": "service-ecu-clonage",
        "active": "ecu",
        "parent_label": None,
        "parent_url": None,
        "hub_url": "service-ecu-clonage.html",
        "hub_label": "Programmation calculateurs",
        "breadcrumb": "Clonage ECU — Lyon",
        "badge": "clonage ECU Lyon — calculateur ECU/BSI 69",
        "icon": "cpu",
        "h1": "Clonage ECU &amp; programmation calculateurs ECU/BSI à Lyon",
        "hero": "<strong class=\"font-semibold text-zinc-200\">Clonage ECU Lyon</strong>, calculateur HS, ECU noyé ou véhicule ne démarre plus&nbsp;? Copie intégrale du firmware sur un calculateur neuf ou d'occasion avec outils <strong class=\"font-semibold text-zinc-200\">FoxFlash</strong> — codage VIN et synchronisation immobiliseur sur Lyon et le Rhône <strong class=\"font-semibold text-zinc-200\">(69)</strong>.",
        "title": "Clonage ECU Lyon — Programmation ECU/BSI | Mecanoo",
        "description": "Clonage ECU/BSI à Lyon : copie du firmware, codage VIN, synchronisation immo. Calculateur HS ou noyé — Rhône (69) et Ain (01), outils FoxFlash.",
        "keywords": "clonage ECU Lyon, programmation calculateur ECU BSI Lyon, copie calculateur Lyon, ECU cloning 69, reprogrammation calculateur Rhône",
        "og_title": "Clonage ECU &amp; programmation ECU/BSI Lyon | Mecanoo",
        "og_description": "Copie calculateur moteur, clonage ECU/BSI et codage VIN sur Lyon et le Rhône (69).",
        "service_name": "Clonage ECU Lyon",
        "problem_title": "Quand faut-il cloner un calculateur ?",
        "problem_intro": "ECU endommagé par l'eau, surtension, panne électronique ou remplacement nécessaire sans reprogrammation concession — le clonage évite le codage onéreux en concession.",
        "problems": [
            ("Calculateur moteur HS", "ECU noyé, court-circuit, composants grillés — véhicule ne démarre plus.", "cpu"),
            ("Remplacement ECU d'occasion", "Calculateur d'occasion non codé à votre véhicule — immobilisation ou défauts persistants.", "refresh-cw"),
            ("Perte données origine", "Effacement accidentel, mise à jour ratée, ECU vierge après panne.", "hard-drive"),
            ("Devis concession élevé", "Codage + main-d'œuvre concession souvent très coûteux et délais longs.", "euro"),
        ],
        "solution_title": "Clonage ECU avec FoxFlash",
        "solution_intro": "Lecture du calculateur d'origine, copie complète du firmware (Flash + EEPROM) sur ECU de remplacement, synchronisation immo et codage VIN si nécessaire.",
        "solution_points": [
            "Lecture complète ECU d'origine (Flash, EEPROM, OTP)",
            "Transfert sur calculateur neuf ou d'occasion compatible",
            "Codage VIN, immo, kilométrage selon besoin",
            "Peugeot, Citroën, Renault, VW, BMW, Mercedes… Lyon, 69 et Ain 01",
        ],
        "faq_intro": "« clonage ECU Lyon », « programmation calculateur ECU BSI Lyon », « ECU cloning 69 »",
        "faqs": [
            ("Qu'est-ce que le clonage ECU et dans quels cas l'utiliser à Lyon ?", "Copie intégrale du firmware d'un calculateur HS vers un ECU de remplacement. Indispensable si l'ECU d'origine est irréparable ou lors d'un remplacement par un calculateur d'occasion."),
            ("Peut-on cloner un calculateur Peugeot ou Citroën sans aller en concession ?", "Oui, avec outils FoxFlash sur Lyon, le Rhône (69) et l'Ain (01) — lecture, copie et codage sur place selon modèle."),
            ("Combien de temps dure un clonage ECU chez Mecanoo ?", "Selon marque et accès calculateur : généralement quelques heures. Devis après marque, modèle et motorisation."),
        ],
        "wa_text": "Bonjour%2C%20clonage%20ECU%20Lyon",
        "img_alt": "Clonage ECU Lyon — programmation calculateur ECU/BSI Rhône 69",
        "related_links": [
            ("service-cle-voiture.html", "Clé de voiture — duplication &amp; programmation"),
            ("service-suppression-options.html", "Suppression d'options — codage BSI / ECU"),
            ("services/programmation-electronique-ecu/", "Programmation électronique ECU — clonage &amp; réparation"),
        ],
    },
    {
        "file": "service-immo-off.html",
        "slug": "service-immo-off",
        "active": "ecu",
        "parent_label": "Calculateurs ECU/BSI",
        "parent_url": "service-ecu-clonage.html",
        "hub_url": "service-ecu-clonage.html",
        "hub_label": "Programmation calculateurs",
        "breadcrumb": "Immo Off — Lyon",
        "badge": "immo off Lyon — antidémarrage ECU/BSI 69",
        "icon": "lock",
        "h1": "Immo Off &amp; suppression antidémarrage à Lyon",
        "hero": "<strong class=\"font-semibold text-zinc-200\">Immo off Lyon</strong>, problème antidémarrage, ECU ou BSI verrouillé&nbsp;? Suppression immobiliseur par reprogrammation avec <strong class=\"font-semibold text-zinc-200\">FoxFlash</strong> — dépannage électronique sur Lyon et le Rhône <strong class=\"font-semibold text-zinc-200\">(69)</strong>.",
        "title": "Immo Off Lyon — Suppression antidémarrage | Mecanoo",
        "description": "Immo off à Lyon : suppression antidémarrage et reprogrammation immobiliseur ECU/BSI. Véhicule ne démarre plus — Rhône (69) et Ain (01).",
        "keywords": "immo off Lyon, suppression antidémarrage Lyon, reprogrammation immo 69, dépannage immobiliseur ECU BSI Rhône",
        "og_title": "Immo Off Lyon | Mecanoo",
        "og_description": "Suppression antidémarrage et immo off ECU/BSI sur Lyon et le 69.",
        "service_name": "Immo Off Lyon",
        "problem_title": "Les problèmes d'antidémarrage (immo)",
        "problem_intro": "Véhicule qui ne démarre plus, clé non reconnue, ECU/BSI remplacé sans codage ou panne circuit immobiliseur — le diagnostic valise identifie le calculateur fautif.",
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
            ("Mon véhicule ne démarre plus à cause de l'immo : que faire à Lyon ?", "Diagnostic valise d'abord. Si immo HS ou ECU remplacé, immo off par reprogrammation est souvent la solution la plus rapide."),
            ("L'immo off est-il définitif ?", "Oui : suppression gravée dans le calculateur — le véhicule démarre sans vérification immobiliseur."),
            ("Faites-vous l'immo off sur Peugeot et Citroën dans le 69 ?", "Oui : PSA (ECU + BSI), Renault, VAG et autres — sur Lyon et métropole."),
        ],
        "wa_text": "Bonjour%2C%20immo%20off%20Lyon",
        "img_alt": "Immo off Lyon — suppression antidémarrage ECU/BSI Rhône 69",
    },
    {
        "file": "service-stage1.html",
        "slug": "service-stage1",
        "active": "reprog",
        "parent_label": "Reprogrammation moteur",
        "parent_url": "service-reprogrammation.html",
        "hub_url": "service-reprogrammation.html",
        "hub_label": "Reprogrammation moteur",
        "breadcrumb": "Reprogrammation Stage 1 — Lyon",
        "badge": "stage 1 Lyon — reprog moteur 69",
        "icon": "zap",
        "h1": "Reprogrammation Stage 1 &amp; gain de puissance à Lyon",
        "hero": "<strong class=\"font-semibold text-zinc-200\">Reprogrammation stage 1 Lyon</strong>, reprog moteur ou gain de puissance/couple&nbsp;? Cartographie optimisée avec outils <strong class=\"font-semibold text-zinc-200\">FoxFlash</strong> — diesel et essence sur Lyon et le Rhône <strong class=\"font-semibold text-zinc-200\">(69)</strong>.",
        "title": "Stage 1 Lyon — Reprogrammation moteur | Mecanoo",
        "description": "Stage 1 à Lyon : reprogrammation moteur sur mesure, +20 à +40 ch, +40 à +80 Nm. Cartographie FoxFlash — Rhône (69) et Ain (01).",
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
        "solution_title": "Stage 1 FoxFlash — puissance &amp; couple optimisés",
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
        "active": "reprog",
        "parent_label": "Reprogrammation moteur",
        "parent_url": "service-reprogrammation.html",
        "hub_url": "service-reprogrammation.html",
        "hub_label": "Reprogrammation moteur",
        "breadcrumb": "Conversion Éthanol E85 — Lyon",
        "badge": "flexfuel E85 Lyon — conversion éthanol 69",
        "icon": "fuel",
        "h1": "Reprogrammation Flexfuel E85 &amp; conversion Éthanol à Lyon",
        "hero": "<strong class=\"font-semibold text-zinc-200\">Reprogrammation E85 Lyon</strong>, conversion flexfuel ou passage à l'éthanol&nbsp;? Cartographie Flex Fuel avec <strong class=\"font-semibold text-zinc-200\">FoxFlash</strong> — roulez SP95/E85 indifféremment, économies à la pompe sur Lyon et le Rhône <strong class=\"font-semibold text-zinc-200\">(69)</strong>.",
        "title": "Conversion E85 Lyon — Flexfuel sans boîtier | Mecanoo",
        "description": "Conversion éthanol E85 à Lyon : cartographie Flex Fuel intégrée au calculateur, sans boîtier. Roulez E85 et SP95 — Rhône (69), Ain (01).",
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
        "file": "service-fap.html",
        "slug": "service-fap",
        "active": "antipollution",
        "parent_label": "Solutions anti-pollution",
        "parent_url": "service-antipollution.html",
        "hub_url": "service-antipollution.html",
        "hub_label": "Solutions anti-pollution",
        "breadcrumb": "Suppression FAP — Lyon",
        "badge": "suppression FAP Lyon — FAP 69",
        "icon": "filter",
        "h1": "Suppression FAP &amp; solution filtre à particules à Lyon",
        "hero": "<strong class=\"font-semibold text-zinc-200\">Suppression FAP Lyon</strong>, filtre à particules saturé ou régénération impossible&nbsp;? Reprogrammation logicielle définitive du FAP / DPF avec <strong class=\"font-semibold text-zinc-200\">FoxFlash</strong> — évitez le remplacement à 1 500 €+ en concession sur Lyon et le Rhône <strong class=\"font-semibold text-zinc-200\">(69)</strong>.",
        "title": "Suppression FAP Lyon — Filtre à particules | Mecanoo",
        "description": "Suppression FAP à Lyon : filtre à particules saturé, régénérations ratées, voyant allumé. Reprogrammation définitive — Rhône (69), Ain (01).",
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
            ("Mon voyant FAP est allumé sur Lyon : que faire ?", "Diagnostic valise d'abord. Si FAP colmaté ou HS, reprogrammation définitive souvent plus économique que remplacement."),
            ("La suppression FAP est-elle définitive ?", "Oui : modification gravée dans le calculateur via FoxFlash — pas un simple effacement temporaire."),
            ("Intervenez-vous sur diesel Peugeot et Citroën pour le FAP dans le 69 ?", "Oui : BlueHDi, HDi, et autres motorisations diesel courantes sur Lyon et métropole."),
        ],
        "wa_text": "Bonjour%2C%20suppression%20FAP%20Lyon",
        "img_alt": "Suppression FAP Lyon — filtre à particules diesel Rhône 69",
    },
    {
        "file": "service-egr.html",
        "slug": "service-egr",
        "active": "antipollution",
        "parent_label": "Solutions anti-pollution",
        "parent_url": "service-antipollution.html",
        "hub_url": "service-antipollution.html",
        "hub_label": "Solutions anti-pollution",
        "breadcrumb": "Suppression EGR — Lyon",
        "badge": "suppression EGR Lyon — vanne EGR 69",
        "icon": "wind",
        "h1": "Suppression EGR &amp; vanne EGR bloquée à Lyon",
        "hero": "<strong class=\"font-semibold text-zinc-200\">Suppression EGR Lyon</strong>, vanne EGR bloquée ou encrassée&nbsp;? Reprogrammation logicielle définitive + option démontage vanne — solution durable avec <strong class=\"font-semibold text-zinc-200\">FoxFlash</strong> sur Lyon et le Rhône <strong class=\"font-semibold text-zinc-200\">(69)</strong>.",
        "title": "Suppression EGR Lyon — Vanne EGR bloquée | Mecanoo",
        "description": "Suppression EGR à Lyon : vanne EGR bloquée, encrassement, codes défaut. Reprogrammation logicielle définitive — Rhône (69) et Ain (01).",
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
        "file": "service-adblue.html",
        "slug": "service-adblue",
        "active": "antipollution",
        "parent_label": "Solutions anti-pollution",
        "parent_url": "service-antipollution.html",
        "hub_url": "service-antipollution.html",
        "hub_label": "Solutions anti-pollution",
        "breadcrumb": "AdBlue / SCR — Lyon",
        "badge": "problème AdBlue Lyon — Rhône 69",
        "icon": "alert-triangle",
        "h1": "Dépannage &amp; solution électronique AdBlue / SCR à Lyon",
        "hero": "<strong class=\"font-semibold text-zinc-200\">Problème AdBlue Lyon</strong>, <strong class=\"font-semibold text-zinc-200\">défaut antipollution Peugeot Citroën</strong> ou voyant SCR récurrent&nbsp;? Reprogrammation logicielle définitive avec outils <strong class=\"font-semibold text-zinc-200\">FoxFlash</strong> — alternative aux devis exorbitants en concession sur Lyon et le <strong class=\"font-semibold text-zinc-200\">69</strong>.",
        "title": "Dépannage AdBlue Lyon — Défaut SCR | Mecanoo",
        "description": "Problème AdBlue à Lyon : défaut SCR, voyant antipollution, pompe et injecteur. Suppression logicielle AdBlue — Rhône (69) et Ain (01).",
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
        "file": "service-cle-voiture.html",
        "slug": "service-cle-voiture",
        "active": "ecu",
        "parent_label": None,
        "parent_url": None,
        "hub_url": "service-ecu-clonage.html",
        "hub_label": "Calculateurs ECU/BSI &amp; immobiliseur",
        "breadcrumb": "Clé de voiture — Lyon",
        "badge": "clé de voiture Lyon — duplication &amp; programmation 69 / Ain 01",
        "icon": "key-round",
        "h1": "Clé de voiture — duplication &amp; programmation à Lyon",
        "hero": "<strong class=\"font-semibold text-zinc-200\">Clé de voiture Lyon</strong>&nbsp;: clé perdue, boîtier cassé ou clé non détectée — <strong class=\"font-semibold text-zinc-200\">duplication</strong>, programmation d'une clé de rechange et appairage avec l'<strong class=\"font-semibold text-zinc-200\">immobiliseur</strong> à domicile sur Lyon, Rhône <strong class=\"font-semibold text-zinc-200\">(69)</strong> et Ain <strong class=\"font-semibold text-zinc-200\">(01)</strong>.",
        "title": "Clé de voiture Lyon — Duplication &amp; programmation | Mecanoo",
        "description": "Clé de voiture perdue ou cassée à Lyon ? Duplication et programmation de clé de rechange, décodage transpondeur — Rhône (69) et Ain (01).",
        "keywords": "clé de voiture Lyon, duplication clé auto 69, programmer clé rechange Lyon, clé pliante cassée, transpondeur immobiliseur Ain 01",
        "og_title": "Clé de voiture Lyon — Duplication & programmation | Mecanoo",
        "og_description": "Clé perdue ou cassée à Lyon ? Duplication et programmation de clé de rechange, décodage transpondeur — Rhône (69) et Ain (01).",
        "service_name": "Clé de voiture Lyon",
        "service_type": "Duplication, programmation & codage de clé automobile — décodage transpondeur et immobiliseur",
        "step3": "Programmation de la clé, appairage avec l'immobiliseur et test de démarrage avant restitution.",
        "problem_title": "Clé de voiture en panne — les cas fréquents",
        "problem_intro": "Perte, casse du boîtier ou clé non reconnue par le véhicule&nbsp;: la majorité des interventions clé se résouvent sans concession, à condition de lire le transpondeur avant de remplacer quoi que ce soit.",
        "problems": [
            ("Clé perdue ou unique", "Plus aucune clé en état de marche — situation bloquante, même à distance.", "key-round"),
            ("Boîtier cassé / gâchette usée", "Télécommande fissurée ou gâchette fatiguée : la clé fonctionne mal mécaniquement.", "tool"),
            ("Clé non détectée", "Le véhicule ne démarre plus — erreur d'immobiliseur ou transpondeur non lu.", "alert-triangle"),
            ("Aucune clé de rechange", "Une seule clé fournie d'origine : en programmer une seconde avant l'urgence.", "copy"),
        ],
        "solution_title": "Duplication &amp; programmation de clé automobile",
        "solution_intro": "Lecture du transpondeur, réparation ou remplacement du boîtier, appairage avec le calculateur d'immobiliseur et test complet — la clé démarre le véhicule avant notre départ.",
        "solution_points": [
            "Duplication de clé simple, clé pliante ou télécommande",
            "Programmation et appairage avec l'immobiliseur (transpondeur)",
            "Réparation de boîtier, gâchette et batterie sur clé existante",
            "Intervention à domicile Lyon, Rhône (69) et Ain (01)",
        ],
        "faq_intro": "« duplication clé voiture Lyon », « programmer clé de rechange 69 », « clé non détectée Lyon »",
        "faqs": [
            ("Combien coûte une clé de voiture supplémentaire à Lyon ?", "Une clé de rechange simple reste abordable ; une clé pliante multimarque avec codage est plus onéreuse — devis après marque et modèle. Duplier avant la casse revient toujours moins cher qu'une urgence sans aucune clé."),
            ("Peut-on programmer une clé si toutes les clés sont perdues ?", "Dans la plupart des cas, oui : le transpondeur est lu ou reprogrammé puis appairé avec l'immobiliseur. Selon la marque et le niveau de sécurité, une réinitialisation peut être nécessaire — diagnostic préalable sur Lyon et le 69."),
            ("Le véhicule ne détecte plus ma clé : que faire ?", "Essayez une seconde clé, contrôlez la pile puis le boîtier. Si le démarrage reste impossible, le défaut vient de la clé ou du capteur de lecture — dépannage à domicile sur Lyon, Rhône (69) et Ain (01)."),
        ],
        "wa_text": "Bonjour%2C%20programmation%20cl%C3%A9%20voiture%20Lyon",
        "img_alt": "Duplication et programmation de clé de voiture à Lyon — immobiliseur Rhône 69",
        "related_links": [
            ("service-ecu-clonage.html", "Clonage ECU/BSI &amp; codage VIN"),
            ("service-immo-off.html", "Suppression d'immobiliseur"),
            ("services/reproduction-cles-auto/", "Reproduction de clés &amp; télécommandes"),
            ("services/perte-totale-cles-lyon/", "Perte totale de clés — création sur place"),
        ],
        # --- Habillage UI spécifique à la page clé (sections optionnelles) ---
        "cards_modern": True,
        "sticky_cta": True,
        "reassurance": [
            ("key-round", "Toutes marques", "Clé simple, pliante ou télécommande — essence, diesel, hybride."),
            ("timer", "Intervention rapide", "Diagnostic ciblé le jour même si disponible, réponse sous 24 h."),
            ("file-text", "Devis gratuit", "Tarif annoncé avant toute programmation ou commande de clé."),
            ("map-pin", "Intervention à domicile", "Lyon, Rhône (69) et Ain (01) — on vient à vous."),
        ],
        "process_kicker": "Notre méthode",
        "process_title": "Intervenir sur une clé de voiture en 4 étapes",
        "process_intro": "Aucune programmation à l'aveugle&nbsp;: la clé d'origine est lue d'abord, et chaque étape est validée avec vous avant de passer à la suivante.",
        "process": [
            ("Lecture &amp; diagnostic", "scan-line", "Identification du véhicule et lecture du transpondeur&nbsp;: type de clé, niveau de sécurité et état de l'immobiliseur sont connus avant toute commande."),
            ("Préparation de la clé", "key-round", "Clé de rechange ou boîtier neuf compatible, copie du tracé mécanique si nécessaire, gâchette et batterie contrôlées."),
            ("Programmation", "cpu", "Appairage de la clé avec le calculateur d'immobiliseur&nbsp;: transpondeur accepté, télécommande mémorisée, verrouillage à distance fonctionnel."),
            ("Test &amp; livraison", "activity", "Démarrage, fermeture centralisée et essai complet avec vous — la clé est remise fonctionnelle, sauf mauvaise surprise."),
        ],
        "cta": {
            "kicker": "Clé perdue ou cassée&nbsp;? Appelez maintenant",
            "title": "Une clé bloquante ne s'arrange pas seule — un appel suffit pour cadrer l'intervention.",
            "text": "Indiquez la marque, le modèle et l'année&nbsp;: nous vous confirmons si la clé peut être programmée à distance de l'atelier et fixons un créneau — <strong class=\"font-semibold text-zinc-200\">devis gratuit avant toute intervention</strong>.",
            "points": ["Devis gratuit", "Clé testée avant départ", "Rapidité d'intervention", "À domicile Lyon &amp; 69"],
        },
    },
    {
        "file": "service-suppression-options.html",
        "slug": "service-suppression-options",
        "active": "ecu",
        "parent_label": None,
        "parent_url": None,
        "hub_url": "service-ecu-clonage.html",
        "hub_label": "Calculateurs ECU/BSI",
        "breadcrumb": "Suppression d'options — Lyon",
        "badge": "suppression d'options Lyon — codage BSI / ECU 69 / Ain 01",
        "icon": "sliders-horizontal",
        "h1": "Suppression d'options à Lyon — limiteur, start/stop &amp; feux",
        "hero": "<strong class=\"font-semibold text-zinc-200\">Suppression d'options Lyon</strong>&nbsp;: <strong class=\"font-semibold text-zinc-200\">limiteur de vitesse</strong>, start/stop, feux de jour ou menu bloqué — codage de la <strong class=\"font-semibold text-zinc-200\">BSI et de l'ECU</strong> avec sauvegarde de la configuration d'origine, à domicile sur Lyon, Rhône <strong class=\"font-semibold text-zinc-200\">(69)</strong> et Ain <strong class=\"font-semibold text-zinc-200\">(01)</strong>.",
        "title": "Suppression options — limiteur &amp; start/stop Lyon | Mecanoo",
        "description": "Suppression d'options automobile à Lyon : limiteur de vitesse, start/stop, feux de jour, codage BSI et ECU — intervention à domicile, Rhône (69) et Ain (01).",
        "keywords": "suppression options Lyon, désactivation limiteur vitesse 69, désactiver start stop Lyon, codage BSI ECU Ain 01, menu compteur caché",
        "og_title": "Suppression options — limiteur & start/stop Lyon | Mecanoo",
        "og_description": "Suppression d'options automobile à Lyon : limiteur, start/stop, feux de jour, codage BSI et ECU — Rhône (69) et Ain (01).",
        "service_name": "Suppression d'options Lyon",
        "service_type": "Codage et désactivation d'options automobile — limiteur, start/stop, feux, menu BSI / ECU",
        "step3": "Vérification des options codées, sauvegarde de la configuration puis restitution du véhicule testé.",
        "problem_title": "Quelles options désactiver ? Les plus demandées",
        "problem_intro": "Chaque constructeur verrouille une partie de la configuration du véhicule&nbsp;: ces options se règlent dans la BSI ou l'ECU, pas par un bouton. La lecture de la configuration d'origine précède toute modification.",
        "problems": [
            ("Limiteur de vitesse bridant", "Vitesse plafonnée à 180 ou 200 km/h — paramètre à désactiver dans le calculateur.", "gauge"),
            ("Start/stop toujours actif", "Coupages fréquents en ville — fonction désactivable selon le véhicule.", "power"),
            ("Menu &amp; feux verrouillés", "Options désactivées par le constructeur : feux de jour, menu caché, langues.", "sliders-horizontal"),
            ("Avertisseurs intrusifs", "Alerte de vitesse, chime d'avertissement ou bip à reconfigurer ou supprimer.", "monitor"),
        ],
        "solution_title": "Codage &amp; désactivation d'options au calculateur",
        "solution_intro": "Connexion à la BSI ou à l'ECU, lecture de la configuration d'origine, modification des paramètres souhaités puis sauvegarde&nbsp;: chaque option codée est testée avant restitution du véhicule.",
        "solution_points": [
            "Sauvegarde de la configuration d'origine avant modification",
            "Limiteur, start/stop, feux de jour, menu et langues recodés",
            "Outils de codage multimarque — BSI, ECU, compteur",
            "Intervention à domicile Lyon, Rhône (69) et Ain (01)",
        ],
        "faq_intro": "« suppression d'options Lyon », « désactiver limiteur vitesse 69 », « désactiver start stop Lyon »",
        "faqs": [
            ("Quelles options peut-on désactiver à Lyon ?", "Selon la marque et le calculateur : limiteur de vitesse, start/stop, feux de jour, alerte de vitesse, menu ou langue du compteur, éclairage d'ambiance. La liste réelle est confirmée après lecture de la configuration du véhicule."),
            ("La suppression d'options est-elle définitive ?", "Elle est enregistrée dans la configuration du calculateur et survit aux coupures de batterie. La configuration d'origine étant sauvegardée lors de l'intervention, une remise à l'état d'origine reste possible."),
            ("Combien coûte un codage d'options à Lyon ?", "Tarif selon le nombre d'options et le véhicule — devis après marque et modèle. Intervention à domicile sur Lyon, le Rhône (69) et l'Ain (01)."),
        ],
        "wa_text": "Bonjour%2C%20suppression%20options%20automobile%20Lyon",
        "img_alt": "Suppression d'options automobile à Lyon — codage BSI et ECU Rhône 69",
        "related_links": [
            ("service-ecu-clonage.html", "Calculateurs ECU/BSI &amp; codage VIN"),
            ("service-reprogrammation.html", "Reprog moteur — Stage 1 &amp; E85"),
        ],
        # --- Habillage UI spécifique à la page options (sections optionnelles) ---
        "cards_modern": True,
        "sticky_cta": True,
        "reassurance": [
            ("shield-check", "Configuration sauvegardée", "L'état d'origine est conservé — retour possible si besoin."),
            ("timer", "Intervention rapide", "Codage le jour même si disponible, réponse sous 24 h."),
            ("file-text", "Devis gratuit", "Tarif annoncé avant toute modification de configuration."),
            ("map-pin", "Intervention à domicile", "Lyon, Rhône (69) et Ain (01) — on vient à vous."),
        ],
        "process_kicker": "Notre méthode",
        "process_title": "Coder ou désactiver une option en 4 étapes",
        "process_intro": "Le calculateur n'est jamais modifié à l'aveugle&nbsp;: la configuration d'origine est lue et sauvegardée d'abord, puis chaque option est validée avec vous.",
        "process": [
            ("Lecture de la configuration", "scan-line", "Connexion à la BSI ou à l'ECU et lecture des paramètres d'origine&nbsp;: les options réellement codées sur votre véhicule sont listées avec vous."),
            ("Sauvegarde", "shield-check", "Export de la configuration d'origine avant toute modification — la base d'un retour à l'état initial si vous le souhaitez."),
            ("Codage des options", "sliders-horizontal", "Désactivation ou reparamétrage des options choisies : limiteur, start/stop, feux de jour, menu, alertes — une par une."),
            ("Vérification", "activity", "Contrôle de chaque option au volant puis essai complet&nbsp;: rien n'est laissé en erreur et les voyants restent éteints."),
        ],
        "cta": {
            "kicker": "Une option vous gêne&nbsp;? Appelez maintenant",
            "title": "Dites-nous quelle option bloquée — nous confirmons sa désactivation en quelques minutes.",
            "text": "Marque, modèle, année et option concernée (limiteur, start/stop, feux, menu)&nbsp;: nous vérifions la faisabilité puis fixons un créneau — <strong class=\"font-semibold text-zinc-200\">devis gratuit avant toute intervention</strong>.",
            "points": ["Devis gratuit", "Configuration sauvegardée", "Rapidité d'intervention", "À domicile Lyon &amp; 69"],
        },
    },
]

# ---------------------------------------------------------------------------
# Pilier « Services Clés Auto & Électronique » — routes /services/<slug>/
#
# Pages générées par le MÊME moteur build_page(), mais servies dans un
# sous-dossier : `prefix = "/"` (liens internes racine) et `route` (URL
# publique sans .html, compatible GitHub Pages via <dossier>/index.html).
# `legal = False` : la mention « hors voie publique » porte sur la reprog
# moteur / l'antipollution, sans objet sur ces prestations.
# ---------------------------------------------------------------------------

KEY_SERVICES = [
    {
        # --- /services/reproduction-cles-auto/ -----------------------------
        "file": "services/reproduction-cles-auto/index.html",
        "route": "services/reproduction-cles-auto/",
        "slug": "reproduction-cles-auto",
        "prefix": "/",
        "active": "keys",
        "legal": False,
        "pillar_blocks": True,
        "parent_label": "Services clés auto",
        "parent_url": "services/",
        "hub_url": "services/",
        "hub_label": "Services clés auto",
        "breadcrumb": "Reproduction de clés auto — Lyon",
        "badge": "reproduction clés auto Lyon — doubles &amp; télécommandes 69 / Ain 01",
        "icon": "key",
        "h1": "Reproduction de clés auto — doubles, télécommandes &amp; réfection de cartes à Lyon",
        "hero": "<strong class=\"font-semibold text-zinc-200\">Reproduction de clés auto Lyon</strong>&nbsp;: double de clé, télécommande usée ou <strong class=\"font-semibold text-zinc-200\">carte à réparer</strong> — décodage du tracé, copie du transpondeur et programmation à domicile sur Lyon, Rhône <strong class=\"font-semibold text-zinc-200\">(69)</strong> et Ain <strong class=\"font-semibold text-zinc-200\">(01)</strong>.",
        "title": "Double clé &amp; carte auto — reproduction Lyon | Mecanoo",
        "description": "Double de clé voiture à Lyon et reproduction de carte auto à Villeurbanne : réfection, télécommande, programmation à domicile — devis gratuit, Rhône (69).",
        "keywords": "reproduction clé voiture Lyon, double clé auto 69, réfection carte clé Lyon, réparer télécommande voiture, dupliquer clé pliante Ain 01",
        "og_title": "Double clé & carte auto — reproduction Lyon | Mecanoo",
        "og_description": "Double de clé voiture à Lyon et reproduction de carte auto à Villeurbanne : réfection, télécommande, programmation à domicile — devis gratuit.",
        "service_name": "Reproduction de clés auto Lyon",
        "service_type": "Reproduction de clés automobiles, doubles, télécommandes & réfection de cartes / boîtiers",
        "step3": "Programmation de la copie, appairage avec l'immobiliseur et test de démarrage.",
        "problem_title": "Clé abîmée ou simple exemplaire — les cas fréquents",
        "problem_intro": "Boîtier fatigué, télécommande qui ne répond plus ou absence de double de sécurité&nbsp;: la plupart des clés se réparent ou se dupliquent sans concession, à condition de lire le transpondeur avant de commander une pièce.",
        "problems": [
            ("Une seule clé", "Aucun double de secours : une casse ou une perte et le véhicule est immobilisé.", "copy"),
            ("Carte / boîtier usé", "Gâchette fatiguée, coque fissurée, touches décollées — la clé fonctionne mal.", "tool"),
            ("Télécommande muette", "Boutons mous, portée réduite ou code radio à reprogrammer.", "radio"),
            ("Clé pliante chère en concession", "Pièce d'origine et codage à plusieurs centaines d'euros, délais longs.", "euro"),
        ],
        "solution_title": "Double, réfection de carte &amp; programmation de clé",
        "solution_intro": "Lecture du transpondeur, recopie du tracé mécanique, reconditionnement du boîtier puis appairage avec l'immobiliseur&nbsp;: la copie est testée avant notre départ, pas seulement à la remise.",
        "solution_points": [
            "Double de clé simple, clé pliante ou télécommande multimarque",
            "Réfection de carte : coque, gâchette, touches et batterie",
            "Décodage du tracé mécanique et lecture / copie du transpondeur",
            "Intervention à domicile Lyon, Rhône (69) et Ain (01)",
        ],
        "faq_intro": "« reproduction clé voiture Lyon », « double clé auto 69 », « réfection carte clé Lyon »",
        "faqs": [
            ("Pouvez-vous réparer ma clé au lieu d'en acheter une nouvelle ?", "Souvent oui : gâchette, coque, touches, batterie ou câblage se remplacent pièce par pièce sur de nombreuses marques. Si l'électronique est morte, une clé de rechange compatible est programmée — le point est fait avant toute commande."),
            ("Dupliquez-vous les clés pliantes et les clés cartes ?", "Oui : clé pliante, clé cartes et télécommandes se dupliquent, avec décodage du tracé et copie du transpondeur. Devis après marque, modèle et année sur Lyon, Rhône (69) et Ain (01)."),
            ("Combien de temps prend une reproduction de clé à Lyon ?", "Généralement le jour même quand la clé de référence est présente, sinon sur rendez-vous après commande du boîtier compatible. La clé est appairée puis testée au démarrage avant restitution."),
        ],
        "wa_text": "Bonjour%2C%20reproduction%20de%20cl%C3%A9s%20auto%20Lyon",
        "img_alt": "Reproduction de clés auto à Lyon — doubles, télécommandes et réfection de cartes Rhône 69",
        "related_links": [
            ("service-cle-voiture.html", "Clé de voiture — programmation &amp; immobiliseur"),
            ("services/perte-totale-cles-lyon/", "Perte totale de clés — création sur place"),
            ("services/ouverture-vehicule-sans-cle/", "Ouverture de véhicule sans clé"),
        ],
        "cards_modern": True,
        "sticky_cta": True,
        "reassurance": [
            ("key-round", "Toutes les clés", "Simple, pliante, cartes ou télécommande — multimarque."),
            ("timer", "Intervention rapide", "Créneau le jour même si disponible, réponse sous 24 h."),
            ("file-text", "Devis gratuit", "Tarif annoncé avant toute commande ou programmation."),
            ("map-pin", "Intervention à domicile", "Lyon, Rhône (69) et Ain (01) — on vient à vous."),
        ],
        "process_kicker": "Notre méthode",
        "process_title": "Reproduire une clé en 4 étapes",
        "process_intro": "La clé d'origine est lue avant toute commande&nbsp;: pas de boîtier acheté à l'aveugle, et chaque étape est validée avec vous.",
        "process": [
            ("Lecture &amp; diagnostic", "scan-line", "Identification du véhicule et lecture du transpondeur&nbsp;: type de clé, niveau de sécurité et état de l'immobiliseur sont connus avant de commander quoi que ce soit."),
            ("Décodage &amp; préparation", "key", "Copie du tracé mécanique de la lame, mise en forme de la copie, contrôle du boîtier, de la gâchette et de la batterie."),
            ("Programmation", "cpu", "Appairage de la copie avec l'immobiliseur&nbsp;: transpondeur accepté, télécommande mémorisée, verrouillage à distance fonctionnel."),
            ("Test &amp; livraison", "activity", "Démarrage, fermeture centralisée et essai complet avec vous — la clé est remise fonctionnelle."),
        ],
        "cta": {
            "kicker": "Clé abîmée ou sans double&nbsp;? Appelez maintenant",
            "title": "Un double se prépare avant la panne — un appel suffit pour cadrer l'intervention.",
            "text": "Indiquez la marque, le modèle et l'année&nbsp;: nous confirmons le type de clé et fixons un créneau — <strong class=\"font-semibold text-zinc-200\">devis express à Lyon avant toute intervention</strong>.",
            "points": ["Devis express à Lyon", "Clé testée avant départ", "Rapidité d'intervention", "À domicile Lyon &amp; 69"],
        },
    },
    {
        # --- /services/perte-totale-cles-lyon/ -----------------------------
        "file": "services/perte-totale-cles-lyon/index.html",
        "route": "services/perte-totale-cles-lyon/",
        "slug": "perte-totale-cles-lyon",
        "prefix": "/",
        "active": "keys",
        "legal": False,
        "pillar_blocks": True,
        "parent_label": "Services clés auto",
        "parent_url": "services/",
        "hub_url": "services/",
        "hub_label": "Services clés auto",
        "breadcrumb": "Perte totale de clés — Lyon",
        "badge": "perte totale de clés Lyon — création de clé sur place 69 / Ain 01",
        "icon": "key-round",
        "h1": "Perte totale de clés — création de clé sur place à Lyon",
        "hero": "<strong class=\"font-semibold text-zinc-200\">Toutes vos clés sont perdues</strong>&nbsp;? Nous créons une clé neuve <strong class=\"font-semibold text-zinc-200\">sur place</strong>, même sans aucun exemplaire restant&nbsp;: lecture ou reprogrammation de l'immobiliseur, décodage mécanique et appairage à domicile sur Lyon, Rhône <strong class=\"font-semibold text-zinc-200\">(69)</strong> et Ain <strong class=\"font-semibold text-zinc-200\">(01)</strong>.",
        "title": "Perte totale clé Lyon — refaire clé sans double | Mecanoo",
        "description": "Perte totale de clé de voiture à Lyon : refaire une clé sans aucun double, reprogrammation de l'immobiliseur sur place — devis gratuit, Rhône (69).",
        "keywords": "perte totale clé voiture Lyon, créer clé sans exemplaire 69, clé perdue toutes Lyon, programme clé perdue immobiliseur Ain 01",
        "og_title": "Perte totale clé Lyon — refaire clé sans double | Mecanoo",
        "og_description": "Perte totale de clé de voiture à Lyon : refaire une clé sans aucun double, reprogrammation de l'immobiliseur sur place — devis gratuit.",
        "service_name": "Création de clé sur place — perte totale Lyon",
        "service_type": "Création de clé automobile quand toutes les clés sont perdues — reprogrammation immobiliseur & décodage mécanique",
        "step3": "Appairage de la clé créée avec l'immobiliseur et test complet de démarrage et de verrouillage.",
        "problem_title": "Quand plus aucune clé n'existe",
        "problem_intro": "Perte des deux clés, clé unique égarée ou volée&nbsp;: le véhicule ne redémarre pas et la concession n'est pas la seule issue. La faisabilité se vérifie par marque, modèle et niveau de sécurité avant tout déplacement.",
        "problems": [
            ("Aucun exemplaire restant", "Plus rien à programmer « à partir de » : la clé doit être créée, pas dupliquée.", "key-round"),
            ("Véhicule immobilisé", "Voiture bloquée sur la voie, au parking ou devant chez vous.", "lock"),
            ("Clé unique d'origine", "Beaucoup de véhicules sortent avec une seule clé — aucun secours.", "copy"),
            ("Devis concession élevé", "Recodage et clé d'origine très chers, avec délais d'attente.", "euro"),
        ],
        "solution_title": "Création de clé sur place, sans exemplaire",
        "solution_intro": "Connexion au calculateur d'immobiliseur pour lire ou reprogrammer les autorisations, décodage du tracé mécanique sur place puis appairage&nbsp;: la clé créée démarre le véhicule avant notre départ.",
        "solution_points": [
            "Création d'une clé neuve quand plus aucune clé n'existe",
            "Lecture ou reprogrammation du calculateur d'immobiliseur",
            "Décodage du tracé mécanique sur place — pas d'aller-retour concession",
            "Intervention à domicile Lyon, Rhône (69) et Ain (01)",
        ],
        "faq_intro": "« perte totale clé voiture Lyon », « créer clé sans exemplaire 69 », « toutes les clés perdues Lyon »",
        "faqs": [
            ("Peut-on créer une clé quand toutes les clés sont perdues ?", "Dans la plupart des cas oui : les autorisations sont lues ou reprogrammées dans l'immobiliseur, la clé est décodée puis appairée. Certaines marques et certains niveaux de sécurité imposent une procédure particulière — diagnostic préalable sur Lyon et le 69."),
            ("Faut-il aller en concession pour une clé perdue ?", "Pas nécessairement : l'intervention se fait à domicile sur Lyon, le Rhône (69) et l'Ain (01), avec devis avant de commencer. La concession reste une option si le constructeur verrouille fortement la procédure — nous vous le disons clairement."),
            ("Combien de temps pour recréer une clé à Lyon ?", "Selon marque et sécurité : souvent à la journée une fois le véhicule identifié, parfois après commande d'un boîtier compatible. Un créneau vous est confirmé au téléphone ou par WhatsApp."),
        ],
        "wa_text": "Bonjour%2C%20perte%20totale%20de%20cl%C3%A9s%20Lyon",
        "img_alt": "Création de clé sur place à Lyon — perte totale de clés, immobiliseur Rhône 69",
        "related_links": [
            ("service-cle-voiture.html", "Clé de voiture — duplication &amp; programmation"),
            ("services/reproduction-cles-auto/", "Reproduction de clés &amp; télécommandes"),
            ("services/ouverture-vehicule-sans-cle/", "Ouverture de véhicule sans clé"),
        ],
        "cards_modern": True,
        "sticky_cta": True,
        "reassurance": [
            ("key-round", "Même sans aucune clé", "Création sur place quand plus rien n'existe."),
            ("timer", "Réponse rapide", "Orientation téléphonique immédiate, créneau le jour même si disponible."),
            ("file-text", "Devis gratuit", "Tarif confirmé avant toute programmation ou commande."),
            ("map-pin", "Intervention à domicile", "Lyon, Rhône (69) et Ain (01) — on vient à vous."),
        ],
        "process_kicker": "Notre méthode",
        "process_title": "Recréer une clé perdue en 4 étapes",
        "process_intro": "Aucun codage à l'aveugle&nbsp;: l'immobiliseur est d'abord interrogé, puis chaque étape est validée avec vous avant de passer à la suivante.",
        "process": [
            ("Diagnostic immobiliseur", "scan-line", "Lecture du calculateur et du système antidémarrage&nbsp;: nous déterminons si la clé est créable sur place et quelle procédure de sécurité s'applique à votre marque."),
            ("Préparation de la clé", "key-round", "Clé neuve compatible, mise en forme du tracé mécanique sur place, contrôle de la gâchette et de la batterie."),
            ("Programmation &amp; appairage", "cpu", "Autorisation de démarrage enregistrée dans l'immobiliseur, télécommande mémorisée, verrouillage à distance opérationnel."),
            ("Test complet", "activity", "Démarrage, verrouillage, déverrouillage et essai avec vous — la clé est remise fonctionnelle, avec ses consignes d'utilisation."),
        ],
        "cta": {
            "kicker": "Plus aucune clé&nbsp;? Appelez maintenant",
            "title": "Sans aucune clé, rien ne s'arrange tout seul — un appel suffit pour débloquer la situation.",
            "text": "Marque, modèle, année et motorisation&nbsp;: nous confirmons la faisabilité et fixons un créneau d'intervention — <strong class=\"font-semibold text-zinc-200\">devis express à Lyon, gratuit et sans engagement</strong>.",
            "points": ["Devis express à Lyon", "Création même sans exemplaire", "Réponse rapide", "À domicile Lyon &amp; 69"],
        },
    },
    {
        # --- /services/ouverture-vehicule-sans-cle/ ------------------------
        "file": "services/ouverture-vehicule-sans-cle/index.html",
        "route": "services/ouverture-vehicule-sans-cle/",
        "slug": "ouverture-vehicule-sans-cle",
        "prefix": "/",
        "active": "keys",
        "legal": False,
        "pillar_blocks": True,
        "parent_label": "Services clés auto",
        "parent_url": "services/",
        "hub_url": "services/",
        "hub_label": "Services clés auto",
        "breadcrumb": "Ouverture de véhicule sans clé — Lyon",
        "badge": "ouverture de véhicule Lyon — dépannage d'urgence non destructif 69 / Ain 01",
        "icon": "unlock",
        "h1": "Ouverture de véhicule sans clé — dépannage d'urgence à Lyon",
        "hero": "<strong class=\"font-semibold text-zinc-200\">Clé fermée à l'intérieur</strong> ou télécommande bloquée&nbsp;? Ouverture <strong class=\"font-semibold text-zinc-200\">non destructive</strong> du véhicule&nbsp;: la carrosserie, le joint et la porte restent intacts — dépannage sur Lyon, Rhône <strong class=\"font-semibold text-zinc-200\">(69)</strong> et Ain <strong class=\"font-semibold text-zinc-200\">(01)</strong>.",
        "title": "Ouverture voiture bloquée Lyon — sans dégât, 69 | Mecanoo",
        "description": "Porte de voiture bloquée avec clé à l'intérieur à Lyon ? Ouverture sans dégât, non destructive, en urgence — dépannage à domicile, Rhône (69).",
        "keywords": "ouverture voiture sans clé Lyon, dépannage auto urgence 69, clé fermée à l'intérieur Lyon, ouverture non destructive voiture Ain 01",
        "og_title": "Ouverture voiture bloquée Lyon — sans dégât, 69 | Mecanoo",
        "og_description": "Porte de voiture bloquée avec clé à l'intérieur à Lyon ? Ouverture sans dégât, non destructive, en urgence — dépannage à domicile.",
        "service_name": "Ouverture de véhicule sans clé Lyon",
        "service_type": "Ouverture non destructive de véhicule, dépannage d'urgence sans clé — intervention à domicile",
        "step3": "Contrôle du verrouillage, test de la fermeture et remise en service du véhicule.",
        "problem_title": "Véhicule fermé — les situations d'urgence",
        "problem_intro": "Clé inaccessible à l'intérieur, pile de télécommande morte ou portière verrouillée sans recours&nbsp;: une ouverture propre évite la casse, la dépose de cylindre et la réparation qui suit.",
        "problems": [
            ("Clé fermée à l'intérieur", "Clé sur le siège ou dans le coffre, porte verrouillée — situation la plus fréquente.", "lock"),
            ("Télécommande hors batterie", "Pile morte ou code radio perdu : plus aucune façon d'ouvrir.", "battery-warning"),
            ("Objets ou passagers bloqués", "Bagages, animal ou enfant à l'intérieur — urgence à traiter vite.", "siren"),
            ("Ouverture par la force", "Porte forcée ou cylindre percé : réparation carrosserie et serrure à plusieurs centaines d'euros.", "shield-alert"),
        ],
        "solution_title": "Ouverture non destructive, sans dégât",
        "solution_intro": "Outils d'ouverture dédiés et méthode adaptée au modèle du véhicule&nbsp;: la porte s'ouvre sans forcer, puis le verrouillage et la fermeture sont contrôlés avec vous avant notre départ.",
        "solution_points": [
            "Ouverture non destructive — carrosserie, joint et porte préservés",
            "Méthode adaptée au modèle : ni percement ni déformation",
            "Contrôle du verrouillage et essai de fermeture après intervention",
            "Intervention à domicile Lyon, Rhône (69) et Ain (01)",
        ],
        "faq_intro": "« ouverture voiture sans clé Lyon », « dépannage auto urgence 69 », « clé fermée à l'intérieur Lyon »",
        "faqs": [
            ("L'ouverture d'une voiture abîme-t-elle la porte ?", "Non, quand elle est faite avec les bons outils : l'ouverture non destructive ne force ni le joint, ni la carrosserie, ni la serrure. C'est précisément ce qui la distingue d'une effraction improvisée."),
            ("Intervenez-vous en urgence à Lyon et dans le 69 ?", "Oui — Lyon, la métropole, le Rhône (69) et l'Ain (01). Appelez ou écrivez sur WhatsApp : le créneau est confirmé immédiatement et le dépannage est planifié au plus tôt selon la disponibilité du jour."),
            ("Que faire si ma télécommande de clé ne répond plus ?", "Contrôlez d'abord la pile et essayez la seconde clé. Si le verrouillage reste impossible, l'ouverture du véhicule puis la réparation de la télécommande (ou une clé de rechange) se font sur place — Lyon, Rhône (69) et Ain (01)."),
        ],
        "wa_text": "Bonjour%2C%20ouverture%20de%20v%C3%A9hicule%20sans%20cl%C3%A9%20Lyon",
        "img_alt": "Ouverture de véhicule sans clé à Lyon — dépannage d'urgence non destructif Rhône 69",
        "related_links": [
            ("services/perte-totale-cles-lyon/", "Perte totale de clés — création sur place"),
            ("services/reproduction-cles-auto/", "Reproduction de clés &amp; télécommandes"),
            ("service-cle-voiture.html", "Clé de voiture — programmation &amp; immobiliseur"),
        ],
        "cards_modern": True,
        "sticky_cta": True,
        "reassurance": [
            ("unlock", "Ouverture non destructive", "Carrosserie, joint et porte intacts."),
            ("siren", "Dépannage d'urgence", "Réponse immédiate, créneau le jour même si disponible."),
            ("shield-check", "Aucun percement", "Ni dépose de cylindre, ni déformation — contrôle final."),
            ("map-pin", "Intervention à domicile", "Lyon, Rhône (69) et Ain (01) — on vient à vous."),
        ],
        "process_kicker": "Notre méthode",
        "process_title": "Ouvrir un véhicule en 4 étapes",
        "process_intro": "Aucune porte n'est forcée&nbsp;: la méthode est choisie selon le modèle, puis le verrouillage est recontrôlé avec vous avant notre départ.",
        "process": [
            ("Diagnostic du verrou", "scan-line", "Identification du véhicule et du type de fermeture (centralisée, à distance, antivol) — la méthode d'ouverture dépend du modèle."),
            ("Choix de la méthode", "settings", "Outils d'ouverture dédiés sélectionnés selon la portière et la serrure : aucune intervention au hasard sur la carrosserie."),
            ("Ouverture non destructive", "unlock", "Ouverture de la porte sans forcer, sans percement ni déformation — le joint et la peinture restent intacts."),
            ("Contrôle &amp; remise en service", "activity", "Test du verrouillage, fermeture et réouverture avec vous, vérification de la centrale — puis, si besoin, réparation de la télécommande sur place."),
        ],
        "cta": {
            "kicker": "Véhicule fermé&nbsp;? Appelez maintenant",
            "title": "Une clé bloquante ne s'ouvre pas seule — un appel débloque la situation en quelques minutes.",
            "text": "Précisez le modèle et l'endroit où se trouve le véhicule&nbsp;: nous confirmons l'intervention et le créneau — <strong class=\"font-semibold text-zinc-200\">dépannage d'urgence avec devis express à Lyon</strong>.",
            "points": ["Devis express à Lyon", "Ouverture non destructive", "Réponse immédiate", "Lyon, 69 &amp; Ain 01"],
        },
    },
    {
        # --- /services/programmation-electronique-ecu/ ----------------------
        "file": "services/programmation-electronique-ecu/index.html",
        "route": "services/programmation-electronique-ecu/",
        "slug": "programmation-electronique-ecu",
        "prefix": "/",
        "active": "keys",
        "legal": False,
        "pillar_blocks": True,
        "parent_label": "Services clés auto",
        "parent_url": "services/",
        "hub_url": "services/",
        "hub_label": "Services clés auto",
        "breadcrumb": "Programmation électronique ECU — Lyon",
        "badge": "programmation électronique ECU Lyon — clonage &amp; réparation 69 / Ain 01",
        "icon": "circuit-board",
        "h1": "Programmation électronique ECU — clonage, réinitialisation &amp; réparation sur table à Lyon",
        "hero": "<strong class=\"font-semibold text-zinc-200\">Programmation électronique Lyon</strong>&nbsp;: clonage de calculateurs, <strong class=\"font-semibold text-zinc-200\">réinitialisation de boîtiers</strong> (BSI, compteur, module immo) et <strong class=\"font-semibold text-zinc-200\">réparation électronique sur table</strong> — lecture / écriture des firmware et codage à Lyon, Rhône <strong class=\"font-semibold text-zinc-200\">(69)</strong> et Ain <strong class=\"font-semibold text-zinc-200\">(01)</strong>.",
        "title": "Clonage calculateur Lyon — électronique auto 69 | Mecanoo",
        "description": "Clonage de calculateur moteur à Lyon et réparation électronique auto dans le Rhône : clonage ECU, codage, réparation sur table — devis gratuit.",
        "keywords": "programmation électronique ECU Lyon, clonage calculateur 69, réinitialisation boîtier BSI Lyon, réparation calculateur sur table Ain 01",
        "og_title": "Clonage calculateur Lyon — électronique auto 69 | Mecanoo",
        "og_description": "Clonage de calculateur moteur à Lyon et réparation électronique auto dans le Rhône : clonage ECU, codage, réparation sur table — devis gratuit.",
        "service_name": "Programmation électronique ECU Lyon",
        "service_type": "Programmation électronique automobile — clonage de calculateurs, réinitialisation de boîtiers & réparation sur table",
        "step3": "Écriture, codage puis contrôle du calculateur sur le véhicule et essai avant restitution.",
        "problem_title": "Calculateur en panne ou boîtier à reprogrammer",
        "problem_intro": "ECU noyé, BSI remplacé sans codage, compteur verrouillé ou composant grillé&nbsp;: la panne électronique se traite au calculateur, après lecture et sauvegarde des données d'origine.",
        "problems": [
            ("Calculateur moteur HS", "ECU noyé, court-circuit, composants grillés — le véhicule ne démarre plus.", "cpu"),
            ("Boîtier à réinitialiser", "BSI, compteur ou module remplacé et non synchronisé avec le véhicule.", "refresh-cw"),
            ("Données d'origine perdues", "Effacement accidentel, mise à jour interrompue, calculateur vierge.", "hard-drive"),
            ("Devis concession", "Remplacement complet et codage à plusieurs milliers d'euros, délais longs.", "euro"),
        ],
        "solution_title": "Clonage, réinitialisation &amp; réparation sur table",
        "solution_intro": "Lecture et sauvegarde du firmware (Flash + EEPROM), copie sur un calculateur compatible, réinitialisation des boîtiers codés puis, si la panne est matérielle, reprise des composants à l'établi.",
        "solution_points": [
            "Clonage de calculateurs : copie Flash + EEPROM sur ECU compatible",
            "Réinitialisation et codage de BSI, compteur et module immobiliseur",
            "Réparation électronique sur table : composants, connectique, alimentation",
            "Peugeot, Citroën, Renault, VAG, BMW… — Lyon, 69 et Ain 01",
        ],
        "faq_intro": "« programmation électronique ECU Lyon », « clonage calculateur 69 », « réparation calculateur sur table Lyon »",
        "faqs": [
            ("Quelle différence entre clonage et réinitialisation d'un calculateur ?", "Le clonage copie intégralement les données d'un calculateur d'origine vers un autre (remplacement). La réinitialisation remet un boîtier codé — BSI, compteur — à un état permettant de le recoder au véhicule. Selon la panne, l'une ou l'autre est nécessaire."),
            ("Réparez-vous les calculateurs sur table ?", "Oui : quand la panne est matérielle (composant grillé, alimentation, connectique), la carte est reprise à l'établi après diagnostic. Si le calculateur est irréparable, le clonage vers un élément compatible reste la solution."),
            ("Combien de temps pour programmer un calculateur à Lyon ?", "Lecture et écriture : souvent à la journée selon l'accès et la marque. Réparation sur table : délai annoncé après inspection du module — devis avant toute intervention sur Lyon, le 69 et l'Ain (01)."),
        ],
        "wa_text": "Bonjour%2C%20programmation%20%C3%A9lectronique%20ECU%20Lyon",
        "img_alt": "Programmation électronique ECU à Lyon — clonage de calculateurs et réparation sur table Rhône 69",
        "related_links": [
            ("service-ecu-clonage.html", "Clonage ECU/BSI &amp; codage VIN"),
            ("service-immo-off.html", "Immo off — antidémarrage ECU/BSI"),
            ("services/reproduction-cles-auto/", "Reproduction de clés &amp; télécommandes"),
        ],
        "cards_modern": True,
        "sticky_cta": True,
        "reassurance": [
            ("cpu", "Clonage &amp; réinitialisation", "ECU, BSI, compteur et module immobiliseur."),
            ("wrench", "Réparation sur table", "Composants et connectique repris à l'atelier."),
            ("file-text", "Devis gratuit", "Tarif annoncé avant toute lecture ou écriture."),
            ("map-pin", "Intervention à domicile", "Lyon, Rhône (69) et Ain (01) — on vient à vous."),
        ],
        "process_kicker": "Notre méthode",
        "process_title": "Programmer un calculateur en 4 étapes",
        "process_intro": "Aucun calculateur n'est écrit sans lecture préalable&nbsp;: la sauvegarde des données d'origine précède toujours la modification.",
        "process": [
            ("Diagnostic &amp; identification", "scan-line", "Connexion au véhicule et au module concerné&nbsp;: le type de calculateur, l'origine de la panne et la faisabilité sont établis avant toute écriture."),
            ("Lecture &amp; sauvegarde", "shield-check", "Extraction complète du firmware (Flash, EEPROM) et sauvegarde des données d'origine — la base d'un retour en arrière."),
            ("Programmation ou réparation", "cpu", "Copie vers le calculateur compatible, réinitialisation du boîtier codé, ou reprise des composants sur table si la panne est matérielle."),
            ("Codage &amp; essai", "activity", "Codage VIN et synchronisation immobiliseur si nécessaire, puis contrôle sur véhicule et essai — le module est restitué en état de marche."),
        ],
        "cta": {
            "kicker": "Calculateur en panne&nbsp;? Appelez maintenant",
            "title": "Un calculateur se diagnostique avant de s'écrire — un appel suffit pour cadrer la réparation.",
            "text": "Marque, modèle et symptôme (ne démarre plus, boîtier remplacé, voyant)&nbsp;: nous donnons une première orientation et fixons un créneau — <strong class=\"font-semibold text-zinc-200\">devis express à Lyon avant toute écriture</strong>.",
            "points": ["Devis express à Lyon", "Sauvegarde d'origine systématique", "Réponse rapide", "Lyon, 69 &amp; Ain 01"],
        },
    },
]

# Pages de service à générer (pilier historique + pilier « clés auto »).
ALL_SERVICES = SERVICES + KEY_SERVICES

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

BASE_CLASS = "transition hover:text-racing"
ACTIVE_CLASS = "font-semibold text-racing"
MOBILE_ACTIVE_CLASS = "font-semibold text-racing"
MOBILE_BASE_CLASS = "text-zinc-300 hover:text-racing"


def automotive_business_node():
    """Entité schema.org LocalBusiness/AutomotiveBusiness — identique sur toutes les pages (@id stable)."""
    return {
        "@type": ["LocalBusiness", "AutomotiveBusiness", "AutoRepair"],
        "@id": f"{SITE}/#localbusiness",
        "name": "Mecanoo Lyon",
        "alternateName": "Mecanoo",
        "image": [f"{SITE}/images/seo-reparation-voiture-lyon_1.jpg"],
        "url": f"{SITE}/",
        "telephone": "+33603439954",
        "priceRange": "€€",
        "description": (
            "Mecanoo Lyon — spécialiste serrurerie automobile & électronique à Lyon, Rhône (69) et Ain (01) : "
            "double et reproduction de clés, création de clé sur place en cas de perte totale, ouverture de véhicule "
            "non destructive, clonage et programmation de calculateurs ECU/BSI — intervention à domicile, devis gratuit."
        ),
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Interventions à domicile",
            "addressLocality": "Lyon",
            "addressRegion": "Auvergne-Rhône-Alpes",
            "postalCode": "69000",
            "addressCountry": "FR",
        },
        "geo": {"@type": "GeoCoordinates", "latitude": 45.764, "longitude": 4.8357},
        "hasMap": "https://www.google.com/maps/search/?api=1&query=Mecanoo+Lyon+diagnostic+%C3%A9lectronique+automobile",
        "openingHoursSpecification": [
            {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                "opens": "08:00",
                "closes": "19:00",
            }
        ],
        "contactPoint": [
            {
                "@type": "ContactPoint",
                "telephone": "+33603439954",
                "contactType": "customer service",
                "areaServed": ["FR-69", "FR-01"],
                "availableLanguage": ["French"],
            }
        ],
        "areaServed": [
            {"@type": "AdministrativeArea", "name": "Rhône"},
            {"@type": "AdministrativeArea", "name": "Ain"},
            {"@type": "City", "name": "Lyon"},
            {"@type": "City", "name": "Villeurbanne"},
            {"@type": "City", "name": "Vénissieux"},
            {"@type": "City", "name": "Bron"},
            {"@type": "City", "name": "Saint-Priest"},
            {"@type": "City", "name": "Meyzieu"},
            {"@type": "City", "name": "Décines-Charpieu"},
            {"@type": "City", "name": "Caluire-et-Cuire"},
            {"@type": "City", "name": "Oullins"},
            {"@type": "City", "name": "Bourg-en-Bresse"},
            {"@type": "City", "name": "Ambérieu-en-Bugey"},
            {"@type": "City", "name": "Nantua"},
            {"@type": "City", "name": "Gex"},
            {"@type": "City", "name": "Miribel"},
            {"@type": "City", "name": "Belley"},
        ],
    }


def offer_node(url):
    """Offer 'devis gratuit' — aucun prix public (tarif communiqué après diagnostic).

    Pas de champ `price` ni `priceCurrency` : inventer un prix exposerait une donnée
    fausse dans les résultats Google (politique structured data spam).
    """
    return {
        "@type": "Offer",
        "name": "Devis gratuit avant intervention",
        "description": "Diagnostic et devis gratuits — tarif de la réparation communiqué après diagnostic, aucune pièce déposée sans accord.",
        "url": url,
        "availability": "https://schema.org/InStock",
        "seller": {"@id": f"{SITE}/#localbusiness"},
        "areaServed": [
            {"@type": "AdministrativeArea", "name": "Rhône"},
            {"@type": "AdministrativeArea", "name": "Ain"},
        ],
    }


def schema_json(s):
    import json
    route = s.get("route", s["file"])  # URL publique : "services/<slug>/" pour le pilier clés
    faqs = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in s["faqs"]]
    breadcrumbs = [
        {"@type": "ListItem", "position": 1, "name": "Accueil", "item": f"{SITE}/"},
    ]
    pos = 2
    if s.get("parent_label") and s.get("parent_url"):
        breadcrumbs.append({"@type": "ListItem", "position": pos, "name": s["parent_label"], "item": f"{SITE}/{s['parent_url']}"})
        pos += 1
    breadcrumbs.append({"@type": "ListItem", "position": pos, "name": s["service_name"], "item": f"{SITE}/{route}"})
    graph = [
        automotive_business_node(),
        {"@type": "BreadcrumbList", "itemListElement": breadcrumbs},
        {"@type": "Service", "@id": f"{SITE}/{route}#service",
         "serviceType": s.get("service_type", s["service_name"]),
         "name": s["service_name"], "description": s["description"],
         "provider": {"@id": f"{SITE}/#localbusiness"},
         "areaServed": [
             {"@type": "AdministrativeArea", "name": "Rhône"},
             {"@type": "AdministrativeArea", "name": "Ain"},
             {"@type": "City", "name": "Lyon"},
             {"@type": "City", "name": "Villeurbanne"},
             {"@type": "City", "name": "Vénissieux"},
             {"@type": "City", "name": "Bron"},
             {"@type": "City", "name": "Saint-Priest"},
             {"@type": "City", "name": "Caluire-et-Cuire"},
             {"@type": "City", "name": "Oullins"},
         ],
         "offers": offer_node(f"{SITE}/{route}"),
         "url": f"{SITE}/{route}"},
        {"@type": "FAQPage", "mainEntity": faqs},
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)


def problem_cards(s):
    """Cartes 'causes' — variante moderne (spec `cards_modern`) ou standard."""
    modern = bool(s.get("cards_modern"))
    cards = []
    for title, desc, icon in s["problems"]:
        if modern:
            cards.append(f"""          <li class="group relative flex h-full flex-col overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-br from-white/[0.07] via-white/[0.03] to-white/[0.01] p-6 transition duration-300 hover:-translate-y-1 hover:border-racing/45 hover:shadow-xl hover:shadow-racing/10">
            <span class="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-racing/60 to-transparent opacity-0 transition group-hover:opacity-100" aria-hidden="true"></span>
            <div class="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-racing/15 text-racing ring-1 ring-racing/30 transition group-hover:bg-racing group-hover:text-ink" aria-hidden="true"><i data-lucide="{icon}" class="h-6 w-6"></i></div>
            <h3 class="text-lg font-bold text-white">{title}</h3>
            <p class="mt-2 text-sm leading-relaxed text-zinc-400">{desc}</p>
          </li>""")
        else:
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


# ---------------------------------------------------------------------------
# Sections optionnelles (habillage spécifique — ex. page bloc ABS)
# ---------------------------------------------------------------------------

def reassurance_block(s):
    """Bandeau de réassurance (garantie, rapidité, devis, domicile) — spec `reassurance`."""
    items = s.get("reassurance") or []
    if not items:
        return ""
    rows = []
    for icon, title, desc in items:
        rows.append(f"""          <li class="group flex items-start gap-3 rounded-2xl border border-white/10 bg-white/[0.03] p-4 transition duration-300 hover:-translate-y-0.5 hover:border-racing/40 hover:bg-racing/[0.07] sm:items-center">
            <span class="inline-flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-racing/15 text-racing ring-1 ring-racing/30 transition group-hover:bg-racing group-hover:text-ink" aria-hidden="true"><i data-lucide="{icon}" class="h-5 w-5"></i></span>
            <span class="min-w-0">
              <span class="block font-semibold leading-tight text-white">{title}</span>
              <span class="mt-1 block text-sm leading-snug text-zinc-400">{desc}</span>
            </span>
          </li>""")
    return f"""    <section class="bg-ink py-6 sm:py-8" aria-label="Nos engagements">
      <div class="mx-auto max-w-6xl px-4 sm:px-6">
        <ul class="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
{chr(10).join(rows)}
        </ul>
      </div>
    </section>
"""


# ---------------------------------------------------------------------------
# Composants transverses du pilier « clés auto & électronique »
# Aucun nom d'outil ni de marque d'équipement : uniquement des garanties et
# des compétences formulées en langage generic (SEO + conformité éditoriale).
# Reutilisés par les 4 pages clés (spec `pillar_blocks`) et par le hub.
# ---------------------------------------------------------------------------

# Garanties & compétences — le « comment on travaille », technique et rassurant.
KEY_GUARANTEES = [
    ("cpu", "Équipement électronique de précision",
     "Lecture et programmation des calculateurs sur un matériel de diagnostic haute fidélité."),
    ("scan-line", "Taillage laser informatisé",
     "Reproduction du tracé de la clé au laser, calquée sur la géométrie d'origine."),
    ("stethoscope", "Diagnostic constructeur",
     "Protocoles de diagnostic propres à chaque constructeur, avant toute intervention."),
    ("feather", "Intervention sans dégât",
     "Ouverture et manipulation préservant la carrosserie, la serrure et l'électronique."),
]

# Pourquoi nous choisir — le « pourquoi nous », engagements de service (assurance).
WHY_CHOOSE = [
    ("timer", "Intervention rapide — Lyon &amp; agglomération",
     "Créneau le jour même quand c'est possible, sur Lyon et sa périphérie."),
    ("file-text", "Devis gratuit et transparent",
     "Tarif annoncé et accepté avant toute intervention, sans surprise."),
    ("badge-check", "Travail garanti",
     "Chaque clé et chaque calculateur sont testés avant notre départ."),
    ("crosshair", "Matériel de taillage haute précision",
     "Taillage laser contrôlé pour une copie fidèle du tracé d'origine."),
]

# Problèmes résolus — chaque « symptôme » client renvoie vers la page qui le traite.
KEY_PROBLEMS_RESOLVED = [
    ("key-round", "«&nbsp;J'ai perdu ma seule clé&nbsp;»",
     "Plus aucun exemplaire en main&nbsp;: nous recréons une clé sur place et reprogrammons l'immobiliseur.",
     "/services/perte-totale-cles-lyon/", "Perte totale de clés"),
    ("copy", "«&nbsp;Je veux un double, vite&nbsp;»",
     "Double de clé ou télécommande taillé et programmé dans la foulée, quand la copie de référence est présente.",
     "/services/reproduction-cles-auto/", "Reproduction de clés"),
    ("lock", "«&nbsp;Mes clés sont bloquées à l'intérieur&nbsp;»",
     "Portes verrouillées avec les clés dedans&nbsp;: ouverture non destructive sur place.",
     "/services/ouverture-vehicule-sans-cle/", "Ouverture de véhicule"),
    ("cpu", "«&nbsp;Mon calculateur moteur est en panne&nbsp;»",
     "Diagnostic, remplacement ou clonage de calculateur pour repartir avec un boîtier fonctionnel.",
     "/services/programmation-electronique-ecu/", "Programmation électronique"),
]


def guarantees_block():
    """Section « Garanties & compétences » — grille technique (bg-ink)."""
    items = []
    for icon, title, desc in KEY_GUARANTEES:
        items.append(f"""          <li class="group relative flex h-full flex-col overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-br from-white/[0.06] via-white/[0.02] to-transparent p-6 transition duration-300 hover:-translate-y-1 hover:border-racing/45 hover:shadow-xl hover:shadow-racing/10">
            <span class="pointer-events-none absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-racing/60 to-transparent opacity-0 transition group-hover:opacity-100" aria-hidden="true"></span>
            <span class="mb-5 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-racing/15 text-racing ring-1 ring-racing/30 transition group-hover:scale-110 group-hover:bg-racing group-hover:text-ink" aria-hidden="true"><i data-lucide="{icon}" class="h-6 w-6"></i></span>
            <h3 class="text-lg font-bold text-white">{title}</h3>
            <p class="mt-2 text-sm leading-relaxed text-zinc-400">{desc}</p>
          </li>""")
    return f"""    <section id="garanties" class="border-b border-white/5 bg-ink py-14 sm:py-20" aria-labelledby="garanties-heading">
      <div class="mx-auto max-w-6xl px-4 sm:px-6">
        <p class="inline-flex items-center gap-2 rounded-full border border-racing/30 bg-racing/10 px-3 py-1 text-xs font-semibold uppercase tracking-wider text-racing"><i data-lucide="shield-check" class="h-3.5 w-3.5"></i>&nbsp;Garanties &amp; compétences</p>
        <h2 id="garanties-heading" class="mt-4 text-2xl font-bold tracking-tight text-white sm:text-3xl">Précision, méthode et contrôle — à chaque intervention</h2>
        <p class="mt-4 max-w-3xl text-zinc-400">Nos compétences reposent sur un équipement électronique de précision, un taillage laser informatisé et un diagnostic adapté à chaque constructeur — sans dégât sur votre véhicule.</p>
        <ul class="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
{chr(10).join(items)}
        </ul>
      </div>
    </section>
"""


def why_choose_block():
    """Section « Pourquoi nous choisir » — engagements de service centrés (assurance)."""
    items = []
    for icon, title, desc in WHY_CHOOSE:
        items.append(f"""          <li class="group flex flex-col items-center text-center">
            <span class="mb-4 inline-flex h-14 w-14 items-center justify-center rounded-2xl bg-racing/15 text-racing ring-1 ring-racing/30 transition duration-300 group-hover:scale-110 group-hover:bg-racing group-hover:text-ink" aria-hidden="true"><i data-lucide="{icon}" class="h-7 w-7"></i></span>
            <h3 class="text-base font-bold text-white">{title}</h3>
            <p class="mt-2 max-w-[16rem] text-sm leading-relaxed text-zinc-400">{desc}</p>
          </li>""")
    return f"""    <section id="pourquoi-nous-choisir" class="relative overflow-hidden border-b border-white/5 bg-gradient-to-b from-zinc-950 to-ink py-16 sm:py-24" aria-labelledby="pourquoi-heading">
      <div class="absolute left-1/2 top-0 h-64 w-[46rem] -translate-x-1/2 rounded-full bg-racing/10 blur-3xl" aria-hidden="true"></div>
      <div class="relative mx-auto max-w-6xl px-4 sm:px-6">
        <p class="inline-flex items-center gap-2 rounded-full border border-racing/30 bg-racing/10 px-3 py-1 text-xs font-semibold uppercase tracking-wider text-racing"><i data-lucide="badge-check" class="h-3.5 w-3.5"></i>&nbsp;Pourquoi nous choisir</p>
        <h2 id="pourquoi-heading" class="mt-4 text-2xl font-bold tracking-tight text-white sm:text-3xl">Des engagements clairs, pas des promesses</h2>
        <p class="mt-4 max-w-3xl text-zinc-400">Rapidité, transparence du devis, garantie du travail et précision du matériel — voici sur quoi vous pouvez compter, à Lyon et en agglomération.</p>
        <ul class="mt-12 grid gap-10 sm:grid-cols-2 lg:grid-cols-4">
{chr(10).join(items)}
        </ul>
      </div>
    </section>
"""


def problems_resolved_block():
    """Section « Problèmes résolus » — chaque symptôme client est un lien vers
    la prestation qui le traite (liens root-relative, valables accueil + hub)."""
    items = []
    for icon, quote, desc, href, label in KEY_PROBLEMS_RESOLVED:
        items.append(f"""          <li>
            <a href="{href}" class="group relative flex h-full flex-col overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-br from-white/[0.06] via-white/[0.02] to-transparent p-6 transition duration-300 hover:-translate-y-1 hover:border-racing/45 hover:shadow-xl hover:shadow-racing/10 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-racing/70">
              <span class="pointer-events-none absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-racing/60 to-transparent opacity-0 transition group-hover:opacity-100" aria-hidden="true"></span>
              <span class="mb-4 inline-flex h-11 w-11 items-center justify-center rounded-xl bg-racing/15 text-racing ring-1 ring-racing/30 transition group-hover:scale-110 group-hover:bg-racing group-hover:text-ink" aria-hidden="true"><i data-lucide="{icon}" class="h-5 w-5"></i></span>
              <p class="text-base font-semibold italic text-zinc-200">{quote}</p>
              <p class="mt-2 text-sm leading-relaxed text-zinc-400">{desc}</p>
              <span class="mt-auto inline-flex items-center gap-1 pt-4 text-sm font-semibold text-racing">{label}<i data-lucide="arrow-right" class="h-4 w-4 transition group-hover:translate-x-0.5" aria-hidden="true"></i></span>
            </a>
          </li>""")
    return f"""    <section id="problemes-resolus" class="border-b border-white/5 bg-zinc-950 py-14 sm:py-20" aria-labelledby="problemes-heading">
      <div class="mx-auto max-w-6xl px-4 sm:px-6">
        <p class="inline-flex items-center gap-2 rounded-full border border-racing/30 bg-racing/10 px-3 py-1 text-xs font-semibold uppercase tracking-wider text-racing"><i data-lucide="life-buoy" class="h-3.5 w-3.5"></i>&nbsp;Problèmes résolus</p>
        <h2 id="problemes-heading" class="mt-4 text-2xl font-bold tracking-tight text-white sm:text-3xl">Vous reconnaissez-vous&nbsp;? Nous avons la solution.</h2>
        <p class="mt-4 max-w-3xl text-zinc-400">Quatre situations fréquentes — chacune renvoie vers la prestation qui la traite, avec devis avant intervention.</p>
        <ul class="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
{chr(10).join(items)}
        </ul>
      </div>
    </section>
"""


def solution_section(s):
    """Bloc solution — carte 'Déroulement' masquée quand une section processus existe (spec `process`)."""
    P = s.get("prefix", "")
    has_process = bool(s.get("process"))
    grid = '      <div class="mx-auto grid max-w-6xl gap-10 px-4 sm:gap-14 sm:px-6 lg:grid-cols-2 lg:items-start">'
    single = '      <div class="mx-auto max-w-6xl px-4 sm:px-6">'

    deroulement = "" if has_process else """        <div class="rounded-2xl border border-racing/20 bg-racing/5 p-6">
          <h3 class="flex items-center gap-2 font-semibold text-white"><i data-lucide="wrench" class="h-5 w-5 text-racing"></i>Déroulement</h3>
          <ol class="mt-4 space-y-3 text-sm text-zinc-400">
            <li class="flex gap-3"><span class="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-racing/20 text-xs font-bold text-racing">1</span><span>Diagnostic valise OBD — marque, modèle, motorisation, codes défaut.</span></li>
            <li class="flex gap-3"><span class="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-racing/20 text-xs font-bold text-racing">2</span><span>Devis transparent avant intervention.</span></li>
            <li class="flex gap-3"><span class="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-racing/20 text-xs font-bold text-racing">3</span><span>""" + s.get("step3", "Reprogrammation / clonage FoxFlash — modification définitive.") + """</span></li>
            <li class="flex gap-3"><span class="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-racing/20 text-xs font-bold text-racing">4</span><span>Contrôle et essai — véhicule opérationnel.</span></li>
          </ol>
        </div>
"""
    open_col = '<div class="max-w-3xl">' if has_process else "<div>"

    return f"""    <section class="border-b border-white/5 bg-ink py-14 sm:py-20">
{single if has_process else grid}
        {open_col}
          <h2 class="text-2xl font-bold tracking-tight text-white sm:text-3xl">{s['solution_title']}</h2>
          <p class="mt-4 text-zinc-400">{s['solution_intro']}</p>
          <ul class="mt-6 space-y-4 text-zinc-300">
{solution_points(s['solution_points'])}
          </ul>
          <div class="mt-8 flex flex-wrap gap-4">
            <a href="https://wa.me/33603439954?text={s['wa_text']}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-2 rounded-xl border border-[#25D366]/40 bg-[#25D366]/10 px-6 py-3 font-semibold text-emerald-300 transition hover:bg-[#25D366]/18"><i data-lucide="message-circle" class="h-5 w-5"></i>WhatsApp</a>
            <a href="{P}{s['hub_url']}" class="inline-flex items-center gap-2 rounded-xl border border-zinc-600 bg-white/5 px-6 py-3 font-semibold text-zinc-200 transition hover:bg-white/10">{s['hub_label']}<i data-lucide="arrow-right" class="h-5 w-5"></i></a>
          </div>
        </div>
{deroulement}      </div>
    </section>
"""


def process_block(s):
    """Section processus en 4 étapes avec icônes (spec `process`)."""
    steps = s.get("process") or []
    if not steps:
        return ""
    cards = []
    for i, (title, icon, desc) in enumerate(steps, start=1):
        cards.append(f"""          <li class="group relative flex h-full flex-col overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-b from-white/[0.07] via-white/[0.03] to-white/[0.01] p-6 transition duration-300 hover:-translate-y-1.5 hover:border-racing/45 hover:shadow-xl hover:shadow-racing/10">
            <span class="pointer-events-none absolute right-4 top-3 select-none text-5xl font-extrabold leading-none text-white/[0.07] transition group-hover:text-racing/30" aria-hidden="true">0{i}</span>
            <span class="mb-5 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-racing/15 text-racing ring-1 ring-racing/30 transition group-hover:scale-110 group-hover:bg-racing group-hover:text-ink" aria-hidden="true"><i data-lucide="{icon}" class="h-6 w-6"></i></span>
            <h3 class="pr-8 text-lg font-bold text-white">{title}</h3>
            <p class="mt-2 text-sm leading-relaxed text-zinc-400">{desc}</p>
          </li>""")
    return f"""    <section id="process" class="border-b border-white/5 bg-zinc-950 py-14 sm:py-20" aria-labelledby="process-heading">
      <div class="mx-auto max-w-6xl px-4 sm:px-6">
        <p class="inline-flex items-center gap-2 rounded-full border border-racing/30 bg-racing/10 px-3 py-1 text-xs font-semibold uppercase tracking-wider text-racing"><i data-lucide="list-checks" class="h-3.5 w-3.5"></i>&nbsp;{s['process_kicker']}</p>
        <h2 id="process-heading" class="mt-4 text-2xl font-bold tracking-tight text-white sm:text-3xl">{s['process_title']}</h2>
        <p class="mt-4 max-w-3xl text-zinc-400">{s['process_intro']}</p>
        <ol class="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
{chr(10).join(cards)}
        </ol>
        <p class="mt-8 flex flex-wrap items-center gap-x-6 gap-y-3 text-sm text-zinc-400"><i data-lucide="info" class="h-4 w-4 shrink-0 text-racing" aria-hidden="true"></i>Chaque étape fait l'objet d'un point avec vous&nbsp;: rien n'est déposé ni remplacé sans votre accord.</p>
      </div>
    </section>
"""


def sticky_cta(s):
    """Barre d'appel fixe en bas sur mobile (spec `sticky_cta`)."""
    if not s.get("sticky_cta"):
        return ""
    return f"""    <div class="fixed inset-x-0 bottom-0 z-[55] border-t border-white/10 bg-ink/95 px-3 py-3 backdrop-blur-md md:hidden" role="region" aria-label="Contact rapide">
      <div class="mx-auto flex max-w-6xl gap-3">
        <a href="tel:+33603439954" class="flex flex-1 items-center justify-center gap-2 rounded-xl bg-racing-strong px-4 py-3 text-sm font-bold text-white shadow-lg shadow-racing/30 transition active:scale-95"><i data-lucide="phone" class="h-4 w-4" aria-hidden="true"></i>Appeler</a>
        <a href="https://wa.me/33603439954?text={s['wa_text']}" target="_blank" rel="noopener noreferrer" class="flex flex-1 items-center justify-center gap-2 rounded-xl border border-[#25D366]/40 bg-[#25D366]/15 px-4 py-3 text-sm font-bold text-emerald-300 transition active:scale-95"><i data-lucide="message-circle" class="h-4 w-4" aria-hidden="true"></i>WhatsApp</a>
      </div>
    </div>
"""


def final_cta(s):
    """Bloc final de conversion — variante percutante (spec `cta`) ou standard."""
    P = s.get("prefix", "")
    cta = s.get("cta")
    if not cta:
        return f"""    <section class="py-14 sm:py-20">
      <div class="mx-auto max-w-3xl px-4 text-center sm:px-6">
        <p class="text-lg font-medium text-white">Besoin d'un devis — {s['service_name']} ?</p>
        <p class="mt-3 text-zinc-400">Marque, modèle, année, motorisation — réponse sous 24 h en général sur Lyon, Rhône (69) et Ain (01).</p>
        <div class="mt-8 flex flex-col items-center justify-center gap-4 sm:flex-row">
          <a href="tel:+33603439954" class="inline-flex items-center gap-2 rounded-xl bg-racing-strong px-8 py-3.5 font-semibold text-white transition hover:bg-racing-strong/90"><i data-lucide="phone" class="h-5 w-5"></i>06&nbsp;03&nbsp;43&nbsp;99&nbsp;54</a>
          <a href="https://wa.me/33603439954?text={s['wa_text']}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-2 rounded-xl border border-[#25D366]/40 bg-[#25D366]/10 px-8 py-3.5 font-semibold text-emerald-300 transition hover:bg-[#25D366]/18"><i data-lucide="message-circle" class="h-5 w-5"></i>WhatsApp</a>
          <a href="{P}index.html#contact" class="inline-flex items-center gap-2 rounded-xl border border-zinc-600 bg-white/5 px-8 py-3.5 font-semibold text-zinc-200 transition hover:bg-white/10">Formulaire contact<i data-lucide="arrow-right" class="h-5 w-5"></i></a>
        </div>
      </div>
    </section>"""

    points = "\n".join(
        f'          <li class="inline-flex items-center gap-2"><i data-lucide="circle-check" class="h-4 w-4 shrink-0 text-racing" aria-hidden="true"></i>{p}</li>'
        for p in cta["points"]
    )
    return f"""    <section class="relative overflow-hidden border-t border-white/5 py-16 sm:py-24" aria-labelledby="cta-heading">
      <div class="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-racing/70 to-transparent" aria-hidden="true"></div>
      <div class="absolute left-1/2 top-0 h-64 w-[46rem] -translate-x-1/2 rounded-full bg-racing/20 blur-3xl" aria-hidden="true"></div>
      <div class="relative mx-auto max-w-3xl px-4 text-center sm:px-6">
        <p class="inline-flex items-center gap-2 rounded-full border border-racing/30 bg-racing/10 px-4 py-1.5 text-xs font-semibold uppercase tracking-wider text-racing"><i data-lucide="siren" class="h-3.5 w-3.5" aria-hidden="true"></i>&nbsp;{cta['kicker']}</p>
        <h2 id="cta-heading" class="mt-5 text-3xl font-extrabold leading-tight tracking-tight text-white sm:text-4xl">{cta['title']}</h2>
        <p class="mx-auto mt-4 max-w-2xl text-lg text-zinc-400">{cta['text']}</p>
        <div class="mt-8 flex flex-col items-stretch justify-center gap-3 sm:flex-row sm:items-center">
          <a href="tel:+33603439954" class="group inline-flex items-center justify-center gap-3 rounded-2xl bg-racing-strong px-7 py-4 text-base font-bold text-white shadow-2xl shadow-racing/40 transition duration-200 hover:scale-[1.03] hover:bg-racing active:scale-95 sm:text-lg">
            <span class="relative flex h-3 w-3" aria-hidden="true"><span class="absolute inline-flex h-full w-full animate-ping rounded-full bg-white opacity-75"></span><span class="relative inline-flex h-3 w-3 rounded-full bg-white"></span></span>
            Appeler le 06&nbsp;03&nbsp;43&nbsp;99&nbsp;54
          </a>
          <a href="https://wa.me/33603439954?text={s['wa_text']}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center justify-center gap-2 rounded-2xl border border-[#25D366]/45 bg-[#25D366]/15 px-7 py-4 text-base font-bold text-emerald-300 transition duration-200 hover:scale-[1.03] hover:bg-[#25D366]/25 active:scale-95 sm:text-lg"><i data-lucide="message-circle" class="h-5 w-5" aria-hidden="true"></i>WhatsApp</a>
        </div>
        <a href="{P}index.html#contact" class="mt-5 inline-flex items-center gap-1.5 text-sm font-semibold text-zinc-300 underline-offset-4 transition hover:text-racing hover:underline">Préférez-vous le formulaire de contact ?<i data-lucide="arrow-right" class="h-4 w-4" aria-hidden="true"></i></a>
        <ul class="mt-8 flex flex-wrap items-center justify-center gap-x-6 gap-y-3 text-sm font-medium text-zinc-300">
{points}
        </ul>
      </div>
    </section>"""


def render_footer(wa_text, fab_pos="bottom-5", prefix=""):
    """Rend le FOOTER commun — `prefix` préfixe les liens internes ("" / "/")."""
    return FOOTER.format(wa_text=wa_text, fab_pos=fab_pos, prefix=prefix)


def footer_html(s):
    """FOOTER — position du bouton WhatsApp surélevée si une barre d'appel fixe est présente."""
    fab_pos = "bottom-20" if s.get("sticky_cta") else "bottom-5"
    return render_footer(s["wa_text"], fab_pos, s.get("prefix", ""))


def related_block(s):
    """Maillage interne optionnel : liens vers les pages associées (spec 'related_links')."""
    P = s.get("prefix", "")
    links = s.get("related_links") or []
    if not links:
        return ""
    items = "\n".join(
        f'          <li><a href="{P}{href}" class="inline-flex items-center gap-1.5 rounded-xl border border-white/10 bg-white/[0.03] px-4 py-2.5 text-sm font-semibold text-zinc-200 transition hover:border-racing/40 hover:text-racing">{label}<i data-lucide="arrow-right" class="h-4 w-4" aria-hidden="true"></i></a></li>'
        for href, label in links
    )
    return f"""    <section class="border-b border-white/5 bg-zinc-950 py-10 sm:py-12" aria-label="Pages associées">
      <div class="mx-auto max-w-6xl px-4 sm:px-6">
        <h2 class="text-xl font-bold tracking-tight text-white sm:text-2xl">Pages associées — {s['service_name']}</h2>
        <ul class="mt-5 flex flex-wrap gap-3">
{items}
        </ul>
      </div>
    </section>
"""


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
    # `prefix` : préfixe des ressources internes ("" racine, "/" sous-dossier).
    meta = {"prefix": "", **meta}
    h = HEAD
    for k, v in meta.items():
        h = h.replace("{" + k + "}", v)
    return h


def breadcrumb_html(s, prefix=""):
    if s.get("parent_label") and s.get("parent_url"):
        return f"""           <li aria-hidden="true">/</li>
           <li><a href="{prefix}{s['parent_url']}" class="text-zinc-400 transition hover:text-racing">{s['parent_label']}</a></li>"""
    return ""


def legal_block(s):
    """Mention légale hors piste — pertinente uniquement pour ce qui touche à la
    reprogrammation moteur / aux suppressions antipollution (spec `legal`).
    Le "\n" de tête préserve la mise en page historique (ligne vide avant)."""
    return "\n" + LEGAL if s.get("legal", True) else ""


def build_page(s):
    P = s.get("prefix", "")  # "" à la racine, "/" depuis services/…
    canonical = f"{SITE}/{s.get('route', s['file'])}"
    nav = render_nav(s["active"], prefix=P)

    head = render_head({
        "prefix": P,
        "description": s["description"], "keywords": s["keywords"], "title": s["title"],
        "canonical": canonical, "og_title": s["og_title"], "og_description": s["og_description"],
        "schema": schema_json(s),
    })

    # Composants transverses du pilier clés/électronique — activés par le flag
    # `pillar_blocks` pour ne pas altérer les 14 pages historiques.
    pillar_html = ""
    if s.get("pillar_blocks"):
        pillar_html = f"""
{guarantees_block()}
{why_choose_block()}
"""

    body = f"""{head}
{nav}
  <main>
    <nav class="border-b border-white/5 bg-zinc-950/80 px-4 py-3 text-sm text-zinc-500 sm:px-6" aria-label="Fil d'Ariane">
      <div class="mx-auto max-w-6xl">
        <ol class="flex flex-wrap items-center gap-2">
          <li><a href="{P}index.html" class="text-zinc-400 transition hover:text-racing">Accueil</a></li>
{breadcrumb_html(s, P)}
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
            <a href="tel:+33603439954" class="inline-flex items-center gap-2 rounded-xl bg-racing-strong px-6 py-3 font-semibold text-white shadow-xl shadow-racing/30 transition hover:bg-racing-strong/90"><i data-lucide="phone" class="h-5 w-5"></i>06&nbsp;03&nbsp;43&nbsp;99&nbsp;54</a>
            <a href="https://wa.me/33603439954?text={s['wa_text']}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-2 rounded-xl border border-[#25D366]/40 bg-[#25D366]/10 px-6 py-3 font-semibold text-emerald-300 transition hover:bg-[#25D366]/18"><i data-lucide="message-circle" class="h-5 w-5"></i>WhatsApp</a>
            <a href="{P}index.html#contact" class="inline-flex items-center gap-2 rounded-xl border border-zinc-600 bg-white/5 px-6 py-3 font-semibold text-zinc-200 transition hover:bg-white/10">{s.get('hero_cta_label', 'Demander un devis')}<i data-lucide="arrow-right" class="h-5 w-5"></i></a>
          </div>
        </div>
        <div class="mt-10 lg:col-span-2 lg:mt-0">
          <figure class="overflow-hidden rounded-2xl border border-white/10">
            <div class="aspect-[4/5] max-h-[520px] bg-zinc-900/80 sm:aspect-video sm:max-h-none">
              <img src="{P}images/seo-reparation-voiture-lyon_1.jpg" alt="{s['img_alt']}" width="1264" height="848" loading="eager" decoding="async" class="size-full object-cover object-center" />
            </div>
          </figure>
        </div>
      </div>
    </section>
{reassurance_block(s)}
    <section class="border-y border-white/5 bg-zinc-950 py-14 sm:py-20">
      <div class="mx-auto max-w-6xl px-4 sm:px-6">
        <h2 class="text-2xl font-bold tracking-tight text-white sm:text-3xl">{s['problem_title']}</h2>
        <p class="mt-4 max-w-3xl text-zinc-400">{s['problem_intro']}</p>
        <ul class="mt-10 grid gap-6 sm:grid-cols-2">
{problem_cards(s)}
        </ul>
      </div>
    </section>

{solution_section(s)}{process_block(s)}
{pillar_html}{related_block(s)}{faq_block(s)}{legal_block(s)}
{final_cta(s)}
  </main>
{sticky_cta(s)}{footer_html(s)}
"""
    return body


# ---------------------------------------------------------------------------
# Pages piliers (hubs)
# ---------------------------------------------------------------------------

HUB_CARDS = """          <article class="group flex flex-col rounded-2xl border border-white/10 bg-gradient-to-br from-zinc-900/80 to-transparent p-6 transition hover:-translate-y-1 hover:border-racing/40 hover:shadow-xl hover:shadow-racing/10">
            <div class="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-racing/15 text-racing ring-1 ring-racing/30"><i data-lucide="{icon}" class="h-6 w-6"></i></div>
            <h3 class="text-lg font-bold text-white">{title}</h3>
            <p class="mt-2 text-sm text-zinc-400">{desc}</p>
            <div class="mt-auto pt-6"><a href="{href}" class="inline-flex items-center gap-1 text-sm font-semibold text-racing hover:underline">En savoir plus<i data-lucide="arrow-right" class="h-4 w-4"></i></a></div>
          </article>"""


def hub_breadcrumb(name, prefix=""):
    return f"""<ol class="flex flex-wrap items-center gap-2">
          <li><a href="{prefix}index.html" class="text-zinc-400 transition hover:text-racing">Accueil</a></li><li aria-hidden="true">/</li>
          <li class="text-zinc-300">{name}</li>
        </ol>"""


def build_reprogrammation_hub():
    """service-reprogrammation.html — Reprogrammation moteur : Stage 1 & E85."""
    cards = []
    hub_items = [
        ("service-stage1.html", "zap", "Stage 1 — puissance &amp; couple", "Reprog moteur sur mesure : gains typiques +20 à +40 ch, meilleure réponse, essence et diesel."),
        ("service-flexfuel.html", "fuel", "Conversion Éthanol E85 (Flexfuel)", "Cartographie Flex Fuel intégrée au calculateur — E85 / SP95 indifféremment, sans boîtier."),
    ]
    for href, icon, title, desc in hub_items:
        cards.append(HUB_CARDS.format(icon=icon, title=title, desc=desc, href=href))

    other = []
    other_items = [
        ("service-ecu-clonage.html", "cpu", "Clonage ECU &amp; programmation ECU/BSI", "Copie firmware, codage VIN, immo off — calculateurs."),
        ("service-antipollution.html", "filter", "Anti-pollution — FAP, EGR, AdBlue", "Suppressions logicielles définitives FoxFlash."),
        ("service-diagnostic.html", "scan-line", "Diagnostic électronique &amp; valise OBD", "Lecture codes défaut moteur, boîte, ABS, airbag."),
    ]
    for href, icon, title, desc in other_items:
        other.append(HUB_CARDS.format(icon=icon, title=title, desc=desc, href=href))

    import json
    faqs = [
        ("Quelle est la différence entre Stage 1 et conversion E85 ?", "Le Stage 1 optimise la cartographie pour plus de puissance et de couple ; la conversion E85 (flexfuel) adapte la cartographie pour rouler à l'éthanol E85 ou à l'essence indifféremment, sans boîtier additif."),
        ("La reprogrammation moteur est-elle disponible sur Lyon et l'Ain ?", "Oui : Mecanoo intervient sur Lyon, la métropole, le Rhône (69) et l'Ain (01) avec outils FoxFlash — devis après marque, modèle et motorisation."),
    ]
    faq_entities = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]
    schema = json.dumps({"@context": "https://schema.org", "@graph": [
        automotive_business_node(),
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Accueil", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Reprogrammation moteur Lyon", "item": f"{SITE}/service-reprogrammation.html"},
        ]},
        {"@type": "Service", "@id": f"{SITE}/service-reprogrammation.html#service",
         "serviceType": "Reprogrammation moteur Stage 1 & conversion Éthanol E85 Lyon",
         "name": "Reprogrammation moteur Stage 1 & Éthanol E85 Lyon",
         "description": "Reprogrammation moteur Lyon : Stage 1 gain de puissance/couple et conversion éthanol E85 flexfuel par FoxFlash — sans boîtier.",
         "provider": {"@id": f"{SITE}/#localbusiness"},
         "areaServed": [{"@type": "AdministrativeArea", "name": "Rhône"}, {"@type": "AdministrativeArea", "name": "Ain"}, {"@type": "City", "name": "Lyon"}],
         "offers": offer_node(f"{SITE}/service-reprogrammation.html"),
         "url": f"{SITE}/service-reprogrammation.html"},
        {"@type": "FAQPage", "mainEntity": faq_entities},
    ]}, ensure_ascii=False)

    faq_items = "\n".join(
        f"""          <div class="rounded-2xl border border-white/10 bg-white/[0.02] p-6">
            <dt class="font-semibold text-white">{q}</dt>
            <dd class="mt-2 text-zinc-400">{a}</dd>
          </div>""" for q, a in faqs
    )

    head = render_head({
        "description": "Reprogrammation moteur à Lyon : Stage 1 puissance/couple et conversion éthanol E85 sans boîtier, outils FoxFlash — Rhône (69) et Ain (01).",
        "keywords": "reprogrammation moteur Lyon, stage 1 Lyon, conversion E85 Lyon, flexfuel Lyon, reprog ECU 69, reprog moteur Rhône",
        "title": "Reprogrammation Moteur Lyon — Stage 1 &amp; E85 | Mecanoo",
        "canonical": f"{SITE}/service-reprogrammation.html",
        "og_title": "Reprogrammation moteur Lyon — Stage 1 & E85 | Mecanoo",
        "og_description": "Stage 1 puissance/couple et conversion éthanol E85 flexfuel par FoxFlash — Lyon, Rhône (69) et Ain (01).",
        "schema": schema,
    })
    nav = render_nav("reprog")

    return f"""{head}
{nav}
  <main>
    <nav class="border-b border-white/5 bg-zinc-950/80 px-4 py-3 text-sm text-zinc-500 sm:px-6" aria-label="Fil d'Ariane">
      <div class="mx-auto max-w-6xl">
        {hub_breadcrumb('Reprogrammation moteur — Stage 1 &amp; E85')}
      </div>
    </nav>
    <section class="relative overflow-hidden bg-gradient-to-b from-zinc-950 to-ink pb-16 pt-12 sm:pb-24 sm:pt-16 noise-bg">
      <div class="absolute inset-x-0 top-0 h-96 bg-gradient-to-b from-racing/15 to-transparent blur-3xl" aria-hidden="true"></div>
      <div class="relative mx-auto max-w-6xl px-4 sm:px-6 lg:grid lg:grid-cols-5 lg:items-center lg:gap-12">
        <div class="lg:col-span-3">
          <p class="mb-4 inline-flex items-center gap-2 rounded-full border border-racing/30 bg-racing/10 px-3 py-1 text-xs font-semibold uppercase tracking-wider text-racing"><i data-lucide="zap" class="h-3.5 w-3.5"></i>&nbsp;reprogrammation moteur Lyon — Stage 1 &amp; E85</p>
          <h1 class="mb-6 text-4xl font-extrabold leading-tight tracking-tight text-white sm:text-5xl">Reprogrammation moteur — Stage 1 &amp; conversion Éthanol E85 à Lyon</h1>
          <p class="text-lg text-zinc-400"><strong class="font-semibold text-zinc-200">Reprogrammation moteur Lyon</strong>&nbsp;: <strong class="font-semibold text-zinc-200">Stage 1</strong> (gain de puissance et couple) et <strong class="font-semibold text-zinc-200">conversion Éthanol E85</strong> (flexfuel) intégrée au calculateur — sans boîtier, outils <strong class="font-semibold text-zinc-200">FoxFlash</strong>, intervention sur Lyon, Rhône <strong class="font-semibold text-zinc-200">(69)</strong> et Ain <strong class="font-semibold text-zinc-200">(01)</strong>.</p>
          <div class="mt-8 flex flex-wrap gap-4">
            <a href="tel:+33603439954" class="inline-flex items-center gap-2 rounded-xl bg-racing-strong px-6 py-3 font-semibold text-white shadow-xl shadow-racing/30 transition hover:bg-racing-strong/90"><i data-lucide="phone" class="h-5 w-5"></i>06&nbsp;03&nbsp;43&nbsp;99&nbsp;54</a>
            <a href="https://wa.me/33603439954?text=Bonjour%2C%20reprog%20moteur%20Lyon%20(stage%201%20%2F%20E85)" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-2 rounded-xl border border-[#25D366]/40 bg-[#25D366]/10 px-6 py-3 font-semibold text-emerald-300 transition hover:bg-[#25D366]/18"><i data-lucide="message-circle" class="h-5 w-5"></i>WhatsApp</a>
            <a href="index.html#contact" class="inline-flex items-center gap-2 rounded-xl border border-zinc-600 bg-white/5 px-6 py-3 font-semibold text-zinc-200 transition hover:bg-white/10">Devis reprog moteur<i data-lucide="arrow-right" class="h-5 w-5"></i></a>
          </div>
        </div>
        <div class="mt-10 lg:col-span-2 lg:mt-0">
          <figure class="overflow-hidden rounded-2xl border border-white/10">
            <div class="aspect-[4/5] max-h-[520px] bg-zinc-900/80 sm:aspect-video sm:max-h-none">
              <img src="images/seo-reparation-voiture-lyon_1.jpg" alt="Reprogrammation moteur Stage 1 et conversion éthanol E85 à Lyon — Mecanoo" width="1264" height="848" loading="eager" decoding="async" class="size-full object-cover object-center" />
            </div>
          </figure>
        </div>
      </div>
    </section>
    <section class="border-y border-white/5 bg-zinc-950 py-14 sm:py-20">
      <div class="mx-auto max-w-6xl px-4 sm:px-6">
        <h2 class="text-2xl font-bold tracking-tight text-white sm:text-3xl">Nos reprogrammations moteur</h2>
        <p class="mt-4 max-w-2xl text-zinc-400">Deux spécialités, un seul rendez-vous — cartographies sur mesure FoxFlash, devis après diagnostic valise.</p>
        <div class="mt-10 grid gap-6 sm:grid-cols-2">
{chr(10).join(cards)}
        </div>
      </div>
    </section>
    <section class="border-b border-white/5 bg-ink py-14 sm:py-20">
      <div class="mx-auto max-w-6xl px-4 sm:px-6">
        <h2 class="text-2xl font-bold tracking-tight text-white sm:text-3xl">Autres domaines d'intervention — électronique &amp; diagnostic</h2>
        <p class="mt-4 max-w-2xl text-zinc-400">Mecanoo Lyon couvre aussi le clonage calculateurs, l'anti-pollution et le diagnostic valise OBD sur Lyon, Rhône (69) et Ain (01).</p>
        <div class="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
{chr(10).join(other)}
        </div>
      </div>
    </section>
    <section id="faq" class="border-b border-white/5 bg-ink py-20 sm:py-24" aria-labelledby="reprog-faq-heading">
      <div class="mx-auto max-w-3xl px-4 sm:px-6">
        <h2 id="reprog-faq-heading" class="text-3xl font-bold tracking-tight text-white sm:text-4xl">Questions fréquentes — reprogrammation moteur Lyon</h2>
        <p class="mt-4 text-lg text-zinc-400">Recherche Google : « reprogrammation moteur Lyon », « stage 1 Lyon », « conversion E85 Lyon ».</p>
        <dl class="mt-10 space-y-6">
{faq_items}
        </dl>
      </div>
    </section>
{LEGAL}
    <section class="py-14 sm:py-20">
      <div class="mx-auto max-w-3xl px-4 text-center sm:px-6">
        <p class="text-lg font-medium text-white">Un devis Stage 1 ou E85 ?</p>
        <p class="mt-3 text-zinc-400">Marque, modèle, année, motorisation — réponse sous 24 h en général sur Lyon, Rhône (69) et Ain (01).</p>
        <div class="mt-8 flex flex-col items-center justify-center gap-4 sm:flex-row">
          <a href="tel:+33603439954" class="inline-flex items-center gap-2 rounded-xl bg-racing-strong px-8 py-3.5 font-semibold text-white transition hover:bg-racing-strong/90"><i data-lucide="phone" class="h-5 w-5"></i>06&nbsp;03&nbsp;43&nbsp;99&nbsp;54</a>
          <a href="https://wa.me/33603439954?text=Bonjour%2C%20reprog%20moteur%20Lyon%20(stage%201%20%2F%20E85)" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-2 rounded-xl border border-[#25D366]/40 bg-[#25D366]/10 px-8 py-3.5 font-semibold text-emerald-300 transition hover:bg-[#25D366]/18"><i data-lucide="message-circle" class="h-5 w-5"></i>WhatsApp</a>
          <a href="index.html#contact" class="inline-flex items-center gap-2 rounded-xl border border-zinc-600 bg-white/5 px-8 py-3.5 font-semibold text-zinc-200 transition hover:bg-white/10">Formulaire contact<i data-lucide="arrow-right" class="h-5 w-5"></i></a>
        </div>
      </div>
    </section>
  </main>
{render_footer("Bonjour%2C%20reprog%20moteur%20Lyon%20(stage%201%20%2F%20E85)")}
"""


def build_antipollution_hub():
    """service-antipollution.html — Solutions anti-pollution : FAP, EGR, AdBlue."""
    cards = []
    hub_items = [
        ("service-fap.html", "filter", "Suppression FAP", "Filtre à particules saturé, régénération impossible — reprogrammation DPF définitive."),
        ("service-egr.html", "wind", "Suppression EGR", "Vanne EGR bloquée ou encrassée — désactivation logicielle + option démontage."),
        ("service-adblue.html", "alert-triangle", "Dépannage AdBlue / SCR", "Défaut antipollution, compteur bloqué, injecteur urée — suppression définitive."),
    ]
    for href, icon, title, desc in hub_items:
        cards.append(HUB_CARDS.format(icon=icon, title=title, desc=desc, href=href))

    other = []
    other_items = [
        ("service-ecu-clonage.html", "cpu", "Clonage ECU &amp; programmation ECU/BSI", "Copie firmware, codage VIN, immo off — calculateurs."),
        ("service-reprogrammation.html", "zap", "Reprog moteur — Stage 1 &amp; E85", "Gain puissance/couple et conversion éthanol flexfuel."),
        ("service-diagnostic.html", "scan-line", "Diagnostic électronique &amp; valise OBD", "Lecture codes défaut moteur, boîte, ABS, airbag."),
    ]
    for href, icon, title, desc in other_items:
        other.append(HUB_CARDS.format(icon=icon, title=title, desc=desc, href=href))

    import json
    faqs = [
        ("La suppression FAP / EGR / AdBlue est-elle définitive ?", "Oui : la modification est gravée dans le calculateur via FoxFlash — ce n'est pas un simple effacement temporaire de voyants."),
        ("Quel est le prix d'une suppression anti-pollution à Lyon ?", "Selon le système (FAP, EGR ou AdBlue) et le véhicule — devis après diagnostic valise. Toujours bien plus économique que le remplacement en concession (souvent 1 200 à 4 000 €)."),
        ("Intervenez-vous sur Lyon, le Rhône et l'Ain ?", "Oui : Lyon et métropole, Rhône (69) et Ain (01) — Bourg-en-Bresse, Ambérieu-en-Bugey, Nantua, Gex et environs."),
    ]
    faq_entities = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]
    schema = json.dumps({"@context": "https://schema.org", "@graph": [
        automotive_business_node(),
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Accueil", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Solutions anti-pollution Lyon", "item": f"{SITE}/service-antipollution.html"},
        ]},
        {"@type": "Service", "@id": f"{SITE}/service-antipollution.html#service",
         "serviceType": "Suppression FAP, EGR & AdBlue — solutions anti-pollution Lyon",
         "name": "Solutions anti-pollution FAP, EGR & AdBlue Lyon",
         "description": "Solutions anti-pollution Lyon : suppression définitive FAP, EGR et AdBlue par reprogrammation FoxFlash — fin des voyants et des régénérations.",
         "provider": {"@id": f"{SITE}/#localbusiness"},
         "areaServed": [{"@type": "AdministrativeArea", "name": "Rhône"}, {"@type": "AdministrativeArea", "name": "Ain"}, {"@type": "City", "name": "Lyon"}],
         "offers": offer_node(f"{SITE}/service-antipollution.html"),
         "url": f"{SITE}/service-antipollution.html"},
        {"@type": "FAQPage", "mainEntity": faq_entities},
    ]}, ensure_ascii=False)

    faq_items = "\n".join(
        f"""          <div class="rounded-2xl border border-white/10 bg-white/[0.02] p-6">
            <dt class="font-semibold text-white">{q}</dt>
            <dd class="mt-2 text-zinc-400">{a}</dd>
          </div>""" for q, a in faqs
    )

    head = render_head({
        "description": "Solutions anti-pollution à Lyon : suppression définitive FAP, EGR et AdBlue par reprogrammation FoxFlash — fin des voyants. Rhône (69), Ain (01).",
        "keywords": "suppression FAP EGR AdBlue Lyon, anti-pollution Lyon, FAP DPF 69, vanne EGR Lyon, problème AdBlue Rhône",
        "title": "Anti-Pollution Lyon — FAP, EGR &amp; AdBlue | Mecanoo",
        "canonical": f"{SITE}/service-antipollution.html",
        "og_title": "Solutions anti-pollution Lyon — FAP, EGR, AdBlue | Mecanoo",
        "og_description": "Suppression définitive FAP, EGR et AdBlue par reprogrammation FoxFlash — Lyon, Rhône (69) et Ain (01).",
        "schema": schema,
    })
    nav = render_nav("antipollution")

    return f"""{head}
{nav}
  <main>
    <nav class="border-b border-white/5 bg-zinc-950/80 px-4 py-3 text-sm text-zinc-500 sm:px-6" aria-label="Fil d'Ariane">
      <div class="mx-auto max-w-6xl">
        {hub_breadcrumb('Solutions anti-pollution — FAP, EGR, AdBlue')}
      </div>
    </nav>
    <section class="relative overflow-hidden bg-gradient-to-b from-zinc-950 to-ink pb-16 pt-12 sm:pb-24 sm:pt-16 noise-bg">
      <div class="absolute inset-x-0 top-0 h-96 bg-gradient-to-b from-racing/15 to-transparent blur-3xl" aria-hidden="true"></div>
      <div class="relative mx-auto max-w-6xl px-4 sm:px-6 lg:grid lg:grid-cols-5 lg:items-center lg:gap-12">
        <div class="lg:col-span-3">
          <p class="mb-4 inline-flex items-center gap-2 rounded-full border border-racing/30 bg-racing/10 px-3 py-1 text-xs font-semibold uppercase tracking-wider text-racing"><i data-lucide="filter" class="h-3.5 w-3.5"></i>&nbsp;solutions anti-pollution Lyon — FAP · EGR · AdBlue</p>
          <h1 class="mb-6 text-4xl font-extrabold leading-tight tracking-tight text-white sm:text-5xl">Solutions anti-pollution — FAP, EGR &amp; AdBlue à Lyon</h1>
          <p class="text-lg text-zinc-400"><strong class="font-semibold text-zinc-200">Solutions anti-pollution Lyon</strong>&nbsp;: <strong class="font-semibold text-zinc-200">suppression définitive FAP, EGR et AdBlue</strong> par reprogrammation logicielle <strong class="font-semibold text-zinc-200">FoxFlash</strong> — fin des voyants, des régénérations et des frais de concession sur Lyon, Rhône <strong class="font-semibold text-zinc-200">(69)</strong> et Ain <strong class="font-semibold text-zinc-200">(01)</strong>.</p>
          <div class="mt-8 flex flex-wrap gap-4">
            <a href="tel:+33603439954" class="inline-flex items-center gap-2 rounded-xl bg-racing-strong px-6 py-3 font-semibold text-white shadow-xl shadow-racing/30 transition hover:bg-racing-strong/90"><i data-lucide="phone" class="h-5 w-5"></i>06&nbsp;03&nbsp;43&nbsp;99&nbsp;54</a>
            <a href="https://wa.me/33603439954?text=Bonjour%2C%20suppression%20FAP%2FEGR%2FAdBlue%20Lyon" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-2 rounded-xl border border-[#25D366]/40 bg-[#25D366]/10 px-6 py-3 font-semibold text-emerald-300 transition hover:bg-[#25D366]/18"><i data-lucide="message-circle" class="h-5 w-5"></i>WhatsApp</a>
            <a href="index.html#contact" class="inline-flex items-center gap-2 rounded-xl border border-zinc-600 bg-white/5 px-6 py-3 font-semibold text-zinc-200 transition hover:bg-white/10">Devis anti-pollution<i data-lucide="arrow-right" class="h-5 w-5"></i></a>
          </div>
        </div>
        <div class="mt-10 lg:col-span-2 lg:mt-0">
          <figure class="overflow-hidden rounded-2xl border border-white/10">
            <div class="aspect-[4/5] max-h-[520px] bg-zinc-900/80 sm:aspect-video sm:max-h-none">
              <img src="images/seo-reparation-voiture-lyon_1.jpg" alt="Suppression FAP, EGR et AdBlue par reprogrammation à Lyon — Mecanoo" width="1264" height="848" loading="eager" decoding="async" class="size-full object-cover object-center" />
            </div>
          </figure>
        </div>
      </div>
    </section>
    <section class="border-y border-white/5 bg-zinc-950 py-14 sm:py-20">
      <div class="mx-auto max-w-6xl px-4 sm:px-6">
        <h2 class="text-2xl font-bold tracking-tight text-white sm:text-3xl">Nos solutions anti-pollution</h2>
        <p class="mt-4 max-w-2xl text-zinc-400">Chaque système dispose d'une page dédiée optimisée SEO — cliquez pour en savoir plus.</p>
        <div class="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
{chr(10).join(cards)}
        </div>
      </div>
    </section>
    <section class="border-b border-white/5 bg-ink py-14 sm:py-20">
      <div class="mx-auto max-w-6xl px-4 sm:px-6">
        <h2 class="text-2xl font-bold tracking-tight text-white sm:text-3xl">Autres domaines d'intervention — électronique &amp; diagnostic</h2>
        <p class="mt-4 max-w-2xl text-zinc-400">Mecanoo Lyon couvre aussi le clonage calculateurs, la reprogrammation moteur et le diagnostic valise OBD sur Lyon, Rhône (69) et Ain (01).</p>
        <div class="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
{chr(10).join(other)}
        </div>
      </div>
    </section>
    <section id="faq" class="border-b border-white/5 bg-ink py-20 sm:py-24" aria-labelledby="antipollution-faq-heading">
      <div class="mx-auto max-w-3xl px-4 sm:px-6">
        <h2 id="antipollution-faq-heading" class="text-3xl font-bold tracking-tight text-white sm:text-4xl">Questions fréquentes — anti-pollution Lyon</h2>
        <p class="mt-4 text-lg text-zinc-400">Recherche Google : « suppression FAP Lyon », « vanne EGR bloquée 69 », « problème AdBlue Lyon ».</p>
        <dl class="mt-10 space-y-6">
{faq_items}
        </dl>
      </div>
    </section>
{LEGAL}
    <section class="py-14 sm:py-20">
      <div class="mx-auto max-w-3xl px-4 text-center sm:px-6">
        <p class="text-lg font-medium text-white">Un devis suppression FAP, EGR ou AdBlue ?</p>
        <p class="mt-3 text-zinc-400">Marque, modèle, année, motorisation, symptômes — réponse sous 24 h en général sur Lyon, Rhône (69) et Ain (01).</p>
        <div class="mt-8 flex flex-col items-center justify-center gap-4 sm:flex-row">
          <a href="tel:+33603439954" class="inline-flex items-center gap-2 rounded-xl bg-racing-strong px-8 py-3.5 font-semibold text-white transition hover:bg-racing-strong/90"><i data-lucide="phone" class="h-5 w-5"></i>06&nbsp;03&nbsp;43&nbsp;99&nbsp;54</a>
          <a href="https://wa.me/33603439954?text=Bonjour%2C%20suppression%20FAP%2FEGR%2FAdBlue%20Lyon" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-2 rounded-xl border border-[#25D366]/40 bg-[#25D366]/10 px-8 py-3.5 font-semibold text-emerald-300 transition hover:bg-[#25D366]/18"><i data-lucide="message-circle" class="h-5 w-5"></i>WhatsApp</a>
          <a href="index.html#contact" class="inline-flex items-center gap-2 rounded-xl border border-zinc-600 bg-white/5 px-8 py-3.5 font-semibold text-zinc-200 transition hover:bg-white/10">Formulaire contact<i data-lucide="arrow-right" class="h-5 w-5"></i></a>
        </div>
      </div>
    </section>
  </main>
{render_footer("Bonjour%2C%20suppression%20FAP%2FEGR%2FAdBlue%20Lyon")}
"""


def build_services_hub():
    """services/index.html — Services clés auto & électronique (hub du pilier).

    Servie depuis un sous-dossier : tous les liens internes sont root-relative
    (P = "/"), comme pour les pages du pilier.
    """
    P = "/"

    hub_items = [
        ("/services/reproduction-cles-auto/", "key", "Reproduction de clés &amp; télécommandes", "Doubles de clés, télécommandes, réfection de cartes et boîtiers — décodage, transpondeur et programmation à domicile."),
        ("/services/perte-totale-cles-lyon/", "key-round", "Perte totale de clés", "Création de clé sur place quand plus aucun exemplaire n'existe — immobiliseur reprogrammé, véhicule redémarrable."),
        ("/services/ouverture-vehicule-sans-cle/", "unlock", "Ouverture de véhicule sans clé", "Dépannage d'urgence, ouverture non destructive — carrosserie, joint et serrure préservés."),
        ("/services/programmation-electronique-ecu/", "circuit-board", "Programmation électronique ECU", "Clonage de calculateurs, réinitialisation de boîtiers (BSI, compteur) et réparation électronique sur table."),
    ]
    cards = [HUB_CARDS.format(icon=icon, title=title, desc=desc, href=href) for href, icon, title, desc in hub_items]

    other_items = [
        ("/service-diagnostic.html", "scan-line", "Diagnostic électronique &amp; valise OBD", "Lecture codes défaut moteur, boîte, ABS, airbag."),
        ("/service-ecu-clonage.html", "cpu", "Clonage ECU &amp; programmation ECU/BSI", "Copie firmware, codage VIN, synchronisation immo."),
        ("/service-cle-voiture.html", "key-round", "Clé de voiture — programmation", "Clé de rechange, appairage avec l'immobiliseur."),
    ]
    other = [HUB_CARDS.format(icon=icon, title=title, desc=desc, href=href) for href, icon, title, desc in other_items]

    import json
    faqs = [
        ("Quels services pour les clés de voiture proposez-vous à Lyon ?", "Quatre prestations complémentaires : reproduction de clés et de télécommandes (doubles, réfection de cartes), création de clé sur place en cas de perte totale, ouverture de véhicule sans clé non destructive, et programmation électronique ECU (clonage, réinitialisation de boîtiers, réparation sur table)."),
        ("Pouvez-vous intervenir quand toutes les clés sont perdues ?", "Oui : lecture ou reprogrammation de l'immobiliseur, décodage mécanique et création d'une clé neuve sur place — Lyon, Rhône (69) et Ain (01), devis avant intervention."),
        ("L'ouverture de véhicule sans clé abîme-t-elle la voiture ?", "Non : l'ouverture non destructive préserve la carrosserie, le joint et la serrure, sans percement ni déformation. Le verrouillage est recontrôlé avec vous avant le départ."),
        ("Clonage ECU et programmation électronique, c'est la même chose ?", "Le clonage copie les données d'un calculateur vers un autre ; la réinitialisation remet un boîtier codé à un état recodable ; la réparation sur table traite la panne matérielle. La bonne approche est choisie après diagnostic."),
    ]
    faq_entities = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]
    schema = json.dumps({"@context": "https://schema.org", "@graph": [
        automotive_business_node(),
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Accueil", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Services clés auto & électronique", "item": f"{SITE}/services/"},
        ]},
        {"@type": ["WebPage", "CollectionPage"], "@id": f"{SITE}/services/#webpage",
         "url": f"{SITE}/services/", "name": "Services clés auto & électronique — Mecanoo Lyon",
         "inLanguage": "fr-FR", "isPartOf": {"@id": f"{SITE}/#website"},
         "description": "Reproduction de clés, perte totale de clés, ouverture de véhicule sans clé et programmation électronique ECU à Lyon, Rhône (69) et Ain (01)."},
        {"@type": "FAQPage", "mainEntity": faq_entities},
    ]}, ensure_ascii=False)

    faq_items = "\n".join(
        f"""          <div class="rounded-2xl border border-white/10 bg-white/[0.02] p-6">
            <dt class="font-semibold text-white">{q}</dt>
            <dd class="mt-2 text-zinc-400">{a}</dd>
          </div>""" for q, a in faqs
    )

    wa = "https://wa.me/33603439954?text=Bonjour%2C%20services%20cl%C3%A9s%20auto%20Lyon"

    head = render_head({
        "prefix": P,
        "description": "Services clés auto à Lyon : reproduction de clés et télécommandes, création de clé sur place (perte totale), ouverture de véhicule non destructive, programmation électronique ECU — Rhône (69) et Ain (01).",
        "keywords": "services clés auto Lyon, reproduction clé voiture 69, perte totale clé Lyon, ouverture véhicule sans clé, programmation ECU Rhône",
        "title": "Services clés auto &amp; électronique Lyon — clés, ouverture, ECU | Mecanoo",
        "canonical": f"{SITE}/services/",
        "og_title": "Services clés auto & électronique — Lyon | Mecanoo",
        "og_description": "Reproduction de clés, perte totale, ouverture de véhicule et programmation ECU à Lyon, Rhône (69) et Ain (01).",
        "schema": schema,
    })
    nav = render_nav("keys", prefix=P)

    return f"""{head}
{nav}
  <main>
    <nav class="border-b border-white/5 bg-zinc-950/80 px-4 py-3 text-sm text-zinc-500 sm:px-6" aria-label="Fil d'Ariane">
      <div class="mx-auto max-w-6xl">
        {hub_breadcrumb('Services clés auto &amp; électronique', P)}
      </div>
    </nav>
    <section class="relative overflow-hidden bg-gradient-to-b from-zinc-950 to-ink pb-16 pt-12 sm:pb-24 sm:pt-16 noise-bg">
      <div class="absolute inset-x-0 top-0 h-96 bg-gradient-to-b from-racing/15 to-transparent blur-3xl" aria-hidden="true"></div>
      <div class="relative mx-auto max-w-6xl px-4 sm:px-6 lg:grid lg:grid-cols-5 lg:items-center lg:gap-12">
        <div class="lg:col-span-3">
          <p class="mb-4 inline-flex items-center gap-2 rounded-full border border-racing/30 bg-racing/10 px-3 py-1 text-xs font-semibold uppercase tracking-wider text-racing"><i data-lucide="key-round" class="h-3.5 w-3.5"></i>&nbsp;services clés auto &amp; électronique — Lyon 69 / Ain 01</p>
          <h1 class="mb-6 text-4xl font-extrabold leading-tight tracking-tight text-white sm:text-5xl">Services clés auto &amp; électronique à Lyon</h1>
          <p class="text-lg text-zinc-400">Quatre prestations urgentes, un seul interlocuteur&nbsp;: <strong class="font-semibold text-zinc-200">reproduction de clés et télécommandes</strong>, <strong class="font-semibold text-zinc-200">création de clé sur place</strong> en cas de perte totale, <strong class="font-semibold text-zinc-200">ouverture de véhicule non destructive</strong> et <strong class="font-semibold text-zinc-200">programmation électronique ECU</strong> — intervention à domicile sur Lyon, Rhône <strong class="font-semibold text-zinc-200">(69)</strong> et Ain <strong class="font-semibold text-zinc-200">(01)</strong>.</p>
          <div class="mt-8 flex flex-wrap gap-4">
            <a href="tel:+33603439954" class="inline-flex items-center gap-2 rounded-xl bg-racing-strong px-6 py-3 font-semibold text-white shadow-xl shadow-racing/30 transition hover:bg-racing-strong/90"><i data-lucide="phone" class="h-5 w-5"></i>06&nbsp;03&nbsp;43&nbsp;99&nbsp;54</a>
            <a href="{wa}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-2 rounded-xl border border-[#25D366]/40 bg-[#25D366]/10 px-6 py-3 font-semibold text-emerald-300 transition hover:bg-[#25D366]/18"><i data-lucide="message-circle" class="h-5 w-5"></i>WhatsApp</a>
            <a href="{P}index.html#contact" class="inline-flex items-center gap-2 rounded-xl border border-zinc-600 bg-white/5 px-6 py-3 font-semibold text-zinc-200 transition hover:bg-white/10">Devis express à Lyon<i data-lucide="arrow-right" class="h-5 w-5"></i></a>
          </div>
        </div>
        <div class="mt-10 lg:col-span-2 lg:mt-0">
          <figure class="overflow-hidden rounded-2xl border border-white/10">
            <div class="aspect-[4/5] max-h-[520px] bg-zinc-900/80 sm:aspect-video sm:max-h-none">
              <img src="{P}images/seo-reparation-voiture-lyon_1.jpg" alt="Services clés auto et électronique à Lyon — reproduction de clés, ouverture de véhicule, programmation ECU Rhône 69" width="1264" height="848" loading="eager" decoding="async" class="size-full object-cover object-center" />
            </div>
          </figure>
        </div>
      </div>
    </section>
    <section class="border-y border-white/5 bg-zinc-950 py-14 sm:py-20">
      <div class="mx-auto max-w-6xl px-4 sm:px-6">
        <h2 class="text-2xl font-bold tracking-tight text-white sm:text-3xl">Nos 4 services clés auto</h2>
        <p class="mt-4 max-w-2xl text-zinc-400">Chaque prestation dispose de sa page dédiée — cliquez pour le détail, les prix se confirment après marque et modèle.</p>
        <div class="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
{chr(10).join(cards)}
        </div>
      </div>
    </section>
{problems_resolved_block()}
{guarantees_block()}
{why_choose_block()}
    <section class="border-b border-white/5 bg-ink py-14 sm:py-20">
      <div class="mx-auto max-w-6xl px-4 sm:px-6">
        <h2 class="text-2xl font-bold tracking-tight text-white sm:text-3xl">Autres domaines d'intervention — électronique &amp; diagnostic</h2>
        <p class="mt-4 max-w-2xl text-zinc-400">Mecanoo Lyon couvre aussi le diagnostic valise OBD, le clonage de calculateurs et la programmation de clé de voiture sur Lyon, Rhône (69) et Ain (01).</p>
        <div class="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
{chr(10).join(other)}
        </div>
      </div>
    </section>
    <section id="faq" class="border-b border-white/5 bg-ink py-20 sm:py-24" aria-labelledby="keys-faq-heading">
      <div class="mx-auto max-w-3xl px-4 sm:px-6">
        <h2 id="keys-faq-heading" class="text-3xl font-bold tracking-tight text-white sm:text-4xl">Questions fréquentes — services clés auto Lyon</h2>
        <p class="mt-4 text-lg text-zinc-400">Recherche Google : « reproduction clé voiture Lyon », « perte totale de clés 69 », « ouverture voiture sans clé Lyon ».</p>
        <dl class="mt-10 space-y-6">
{faq_items}
        </dl>
      </div>
    </section>
    <section class="py-14 sm:py-20">
      <div class="mx-auto max-w-3xl px-4 text-center sm:px-6">
        <p class="text-lg font-medium text-white">Une clé bloquante, un calculateur en panne&nbsp;?</p>
        <p class="mt-3 text-zinc-400">Marque, modèle, année et symptôme — réponse rapide sur Lyon, Rhône (69) et Ain (01).</p>
        <div class="mt-8 flex flex-col items-center justify-center gap-4 sm:flex-row">
          <a href="tel:+33603439954" class="inline-flex items-center justify-center gap-2 rounded-xl bg-racing-strong px-8 py-3.5 font-semibold text-white transition hover:bg-racing-strong/90"><i data-lucide="phone" class="h-5 w-5"></i>06&nbsp;03&nbsp;43&nbsp;99&nbsp;54</a>
          <a href="{wa}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center justify-center gap-2 rounded-xl border border-[#25D366]/40 bg-[#25D366]/10 px-8 py-3.5 font-semibold text-emerald-300 transition hover:bg-[#25D366]/18"><i data-lucide="message-circle" class="h-5 w-5"></i>WhatsApp</a>
          <a href="{P}index.html#contact" class="inline-flex items-center justify-center gap-2 rounded-xl border border-zinc-600 bg-white/5 px-8 py-3.5 font-semibold text-zinc-200 transition hover:bg-white/10">Devis express à Lyon<i data-lucide="arrow-right" class="h-5 w-5"></i></a>
        </div>
      </div>
    </section>
  </main>
{render_footer("Bonjour%2C%20services%20cl%C3%A9s%20auto%20Lyon", "bottom-5", P)}
"""


def build_actualites():
    """actualites.html — hub éditorial « Actualités & guides » (page non-service).

    Contenu réel uniquement : chaque carte pointe vers une page existante.
    Pas d'article daté inventé — la page se construit par ajout de guides.
    """
    import json

    guides = [
        ("service-cle-voiture.html", "key-round", "Clé de voiture perdue ou cassée", "Duplication, clé de rechange et appairage avec l'immobiliseur — Lyon 69 / Ain 01."),
        ("service-airbag.html", "shield-check", "Voyant airbag allumé", "Contacteur rotatif, connecteur sous siège, prétensionneur — diagnostic SRS."),
        ("service-abs.html", "shield-alert", "Voyant ABS allumé", "Capteur de roue ou bloc hydraulique : lire les codes C0xxx avant de remplacer."),
        ("service-diagnostic.html", "scan-line", "Lire les codes défaut sans se tromper", "Ce que la valise OBD révèle — et pourquoi ne rien effacer à l'aveugle."),
        ("service-suppression-options.html", "sliders-horizontal", "Limiteur &amp; start/stop : ce qui se code", "Options désactivables dans la BSI / ECU, configuration d'origine sauvegardée."),
        ("service-fap.html", "filter", "FAP saturé : les vraies options", "Régénérations bloquées, factures qui s'accumulent — ce que dit le diagnostic."),
    ]
    guides_html = "\n".join(
        HUB_CARDS.format(icon=icon, title=title, desc=desc, href=href)
        for href, icon, title, desc in guides
    )

    news = [
        ("service-airbag.html", "Réparation airbag (SRS) — nouvelle prestation"),
        ("service-cle-voiture.html", "Duplication &amp; programmation de clé de voiture"),
        ("service-suppression-options.html", "Suppression d'options — codage BSI / ECU"),
        ("service-abs.html", "Bloc ABS — capteurs de roue, pompe hydraulique"),
    ]
    news_html = "\n".join(
        f'          <li><a href="{href}" class="inline-flex items-center gap-1.5 rounded-xl border border-white/10 bg-white/[0.03] px-4 py-2.5 text-sm font-semibold text-zinc-200 transition hover:border-racing/40 hover:text-racing">{label}<i data-lucide="arrow-right" class="h-4 w-4" aria-hidden="true"></i></a></li>'
        for href, label in news
    )

    schema = json.dumps({"@context": "https://schema.org", "@graph": [
        automotive_business_node(),
        {"@type": "WebSite", "@id": f"{SITE}/#website", "url": f"{SITE}/",
         "name": "Mecanoo Lyon", "inLanguage": "fr-FR",
         "publisher": {"@id": f"{SITE}/#localbusiness"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Accueil", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Actualités & guides", "item": f"{SITE}/actualites.html"},
        ]},
        {"@type": ["WebPage", "CollectionPage"], "@id": f"{SITE}/actualites.html#webpage",
         "url": f"{SITE}/actualites.html", "name": "Actualités & guides — Mecanoo Lyon",
         "inLanguage": "fr-FR", "isPartOf": {"@id": f"{SITE}/#website"},
         "description": "Guides, conseils et nouveautés de Mecanoo Lyon : clé de voiture, voyant airbag, bloc ABS, suppression FAP et codage d'options — Rhône (69) et Ain (01)."},
    ]}, ensure_ascii=False)

    head = render_head({
        "description": "Guides, conseils et nouveautés de Mecanoo Lyon : clé de voiture, voyant airbag, bloc ABS, suppression FAP et codage d'options — Rhône (69) et Ain (01).",
        "keywords": "actualités auto Lyon, guides diagnostic automobile, conseils entretien 69, électronique automobile Ain 01",
        "title": "Actualités &amp; guides auto Lyon | Mecanoo",
        "canonical": f"{SITE}/actualites.html",
        "og_title": "Actualités & guides auto Lyon | Mecanoo",
        "og_description": "Guides, conseils et nouveautés de Mecanoo Lyon — clé de voiture, airbag, ABS, FAP, codage options. Rhône (69) et Ain (01).",
        "schema": schema,
    })
    nav = render_nav(None)

    return f"""{head}
{nav}
  <main>
    <nav class="border-b border-white/5 bg-zinc-950/80 px-4 py-3 text-sm text-zinc-500 sm:px-6" aria-label="Fil d'Ariane">
      <div class="mx-auto max-w-6xl">
        <ol class="flex flex-wrap items-center gap-2">
          <li><a href="index.html" class="text-zinc-400 transition hover:text-racing">Accueil</a></li>
          <li aria-hidden="true">/</li>
          <li class="text-zinc-300">Actualités &amp; guides</li>
        </ol>
      </div>
    </nav>

    <section class="relative overflow-hidden bg-gradient-to-b from-zinc-950 to-ink pb-16 pt-12 sm:pb-24 sm:pt-16 noise-bg">
      <div class="absolute inset-x-0 top-0 h-96 bg-gradient-to-b from-racing/15 to-transparent blur-3xl" aria-hidden="true"></div>
      <div class="relative mx-auto max-w-6xl px-4 sm:px-6">
        <p class="mb-4 inline-flex items-center gap-2 rounded-full border border-racing/30 bg-racing/10 px-3 py-1 text-xs font-semibold uppercase tracking-wider text-racing"><i data-lucide="newspaper" class="h-3.5 w-3.5"></i>&nbsp;guides &amp; nouveautés</p>
        <h1 class="mb-6 max-w-3xl text-4xl font-extrabold leading-tight tracking-tight text-white sm:text-5xl">Actualités &amp; guides — électronique automobile à Lyon</h1>
        <p class="max-w-3xl text-lg text-zinc-400">Conseils de diagnostic, explications de pannes et nouveautés de nos prestations&nbsp;: de quoi comprendre le problème avant d'ouvrir le capot — <strong class="font-semibold text-zinc-200">Mecanoo</strong> intervient à domicile sur Lyon, Rhône <strong class="font-semibold text-zinc-200">(69)</strong> et Ain <strong class="font-semibold text-zinc-200">(01)</strong>.</p>
        <div class="mt-8 flex flex-wrap gap-4">
          <a href="tel:+33603439954" class="inline-flex items-center gap-2 rounded-xl bg-racing-strong px-6 py-3 font-semibold text-white shadow-xl shadow-racing/30 transition hover:bg-racing-strong/90"><i data-lucide="phone" class="h-5 w-5"></i>06&nbsp;03&nbsp;43&nbsp;99&nbsp;54</a>
          <a href="index.html#services" class="inline-flex items-center gap-2 rounded-xl border border-zinc-600 bg-white/5 px-6 py-3 font-semibold text-zinc-200 transition hover:bg-white/10">Toutes nos prestations<i data-lucide="arrow-right" class="h-5 w-5"></i></a>
        </div>
      </div>
    </section>

    <section class="border-y border-white/5 bg-zinc-950 py-14 sm:py-20">
      <div class="mx-auto max-w-6xl px-4 sm:px-6">
        <h2 class="text-2xl font-bold tracking-tight text-white sm:text-3xl">Nos guides pratiques</h2>
        <p class="mt-4 max-w-2xl text-zinc-400">Un guide par symptôme ou par prestation — rédigé à partir de nos interventions réelles sur Lyon et le 69.</p>
        <div class="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
{guides_html}
        </div>
      </div>
    </section>

    <section class="border-b border-white/5 bg-ink py-14 sm:py-20">
      <div class="mx-auto max-w-6xl px-4 sm:px-6">
        <h2 class="text-2xl font-bold tracking-tight text-white sm:text-3xl">Nouveautés du site</h2>
        <p class="mt-4 max-w-2xl text-zinc-400">Les dernières prestations ajoutées à notre catalogue — chacune dispose de sa page dédiée.</p>
        <ul class="mt-8 flex flex-wrap gap-3">
{news_html}
        </ul>
      </div>
    </section>
{LEGAL}
    <section class="py-14 sm:py-20">
      <div class="mx-auto max-w-3xl px-4 text-center sm:px-6">
        <p class="text-lg font-medium text-white">Une question sur votre véhicule ?</p>
        <p class="mt-3 text-zinc-400">Marque, modèle, année, symptôme — réponse sous 24 h en général sur Lyon, Rhône (69) et Ain (01).</p>
        <div class="mt-8 flex flex-col items-center justify-center gap-4 sm:flex-row">
          <a href="tel:+33603439954" class="inline-flex items-center justify-center gap-2 rounded-xl bg-racing-strong px-8 py-3.5 font-semibold text-white transition hover:bg-racing-strong/90"><i data-lucide="phone" class="h-5 w-5"></i>06&nbsp;03&nbsp;43&nbsp;99&nbsp;54</a>
          <a href="https://wa.me/33603439954?text=Bonjour%2C%20%C3%A9lectronique%20automobile%20Lyon" target="_blank" rel="noopener noreferrer" class="inline-flex items-center justify-center gap-2 rounded-xl border border-[#25D366]/40 bg-[#25D366]/10 px-8 py-3.5 font-semibold text-emerald-300 transition hover:bg-[#25D366]/18"><i data-lucide="message-circle" class="h-5 w-5"></i>WhatsApp</a>
          <a href="index.html#contact" class="inline-flex items-center justify-center gap-2 rounded-xl border border-zinc-600 bg-white/5 px-8 py-3.5 font-semibold text-zinc-200 transition hover:bg-white/10">Formulaire contact<i data-lucide="arrow-right" class="h-5 w-5"></i></a>
        </div>
      </div>
    </section>
  </main>
{render_footer("Bonjour%2C%20%C3%A9lectronique%20automobile%20Lyon")}
"""


if __name__ == "__main__":
    for svc in ALL_SERVICES:
        out = BASE / svc["file"]
        out.parent.mkdir(parents=True, exist_ok=True)  # services/<slug>/
        out.write_text(build_page(svc), encoding="utf-8")
        print(f"Generated {out.relative_to(BASE)}")
    hub = BASE / "service-reprogrammation.html"
    hub.write_text(build_reprogrammation_hub(), encoding="utf-8")
    print(f"Generated {hub.name}")
    anti = BASE / "service-antipollution.html"
    anti.write_text(build_antipollution_hub(), encoding="utf-8")
    print(f"Generated {anti.name}")
    keys_hub = BASE / "services" / "index.html"
    keys_hub.parent.mkdir(parents=True, exist_ok=True)
    keys_hub.write_text(build_services_hub(), encoding="utf-8")
    print(f"Generated {keys_hub.relative_to(BASE)}")
    act = BASE / "actualites.html"
    act.write_text(build_actualites(), encoding="utf-8")
    print(f"Generated {act.name}")
    sync_nav_pages()
