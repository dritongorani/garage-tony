# Mecanoo Lyon — mecanolyon.fr

Site **100 % statique** (HTML / CSS / JS) pour *Mecanoo Lyon*, électronique automobile
et diagnostic à Lyon : diagnostic valise OBD, clonage ECU/BSI, reprogrammation Stage 1
& Éthanol E85, solutions anti-pollution (FAP / EGR / AdBlue), réparation de bloc ABS,
réparation airbag, duplication de clé, suppression d'options et hub de guides.

> **Pas de backend.** Aucun Node.js, Express, Python à l'exécution, ni base de données.
> Le site est composé de fichiers statiques servis tels quels.

---

## Stack

| | |
|---|---|
| Front | HTML statique, CSS, JavaScript (vanilla) |
| Hébergement | **GitHub Pages** |
| Domaine | `mecanolyon.fr` — déclaré par le fichier `CNAME` |
| Générateur | `generate-services.py` — Python 3, **stdlib seule**, aucune dépendance |
| Conteneur *(optionnel)* | `nginx:alpine` pour un aperçu local |

---

## Arborescence

```
mecanolyon/
├── index.html                    # Accueil
├── service-abs.html              # Réparation bloc ABS
├── service-airbag.html           # Réparation airbag (SRS / voyant airbag)
├── service-diagnostic.html       # Diagnostic électronique (pilier)
├── service-ecu-clonage.html      # Clonage / programmation ECU-BSI
├── service-reprogrammation.html  # Reprog Stage 1 & Éthanol E85 (hub)
├── service-stage1.html           # Reprog Stage 1
├── service-flexfuel.html         # Conversion éthanol E85
├── service-antipollution.html    # Anti-pollution FAP/EGR/AdBlue (hub)
├── service-fap.html              # Suppression FAP/DPF
├── service-egr.html              # Suppression vanne EGR
├── service-adblue.html           # Dépannage / suppression AdBlue
├── service-immo-off.html         # Suppression d'immobiliseur
├── service-cle-voiture.html      # Duplication / programmation de clé
├── service-suppression-options.html  # Codage & désactivation d'options
├── actualites.html               # Guides & nouveautés (hub éditorial)
├── zone-intervention.html        # Zone d'intervention (Rhône / Ain)
├── thank-you.html                # Page de remerciement (noindex)
├── services/                     # Section « Clés & électronique » (URL propres)
│   ├── index.html                # Hub « Services clés auto & électronique »
│   ├── reproduction-cles-auto/index.html
│   ├── perte-totale-cles-lyon/index.html
│   ├── ouverture-vehicule-sans-cle/index.html
│   └── programmation-electronique-ecu/index.html
│
├── sitemap.xml                   # Sitemap (22 URL indexables)
├── robots.txt                    # + directive Sitemap
├── CNAME                         # Domaine personnalisé GitHub Pages
│
├── partials/                     # Composants partagés (markup unique)
│   └── navbar.html               # ⚠️ Source unique de la nav — éditez ICI
│
├── images/                       # Images référencées par les balises <img> / og:image
│   └── seo-reparation-voiture-lyon_1.jpg
├── assets/                       # Scripts et assets partagés
│   ├── canonical-host.js         # Redirige www → domaine canonique
│   └── nav.js                    # Dropdown « Nos services » + menu mobile
│
├── generate-services.py          # ⚠️ Source de vérité des pages service-*.html
│                                 #    + des pages services/ (hub + 4 clés auto)
│                                 #    + injecte partials/navbar.html (sync_nav_pages)
├── .agent/                       # Configuration des agents (ignorée par git)
│
├── Dockerfile / nginx.conf / docker-compose.yml   # Aperçu local optionnel
├── .dockerignore / .gitignore
└── README.md
```

> **Pourquoi les HTML sont-ils à la racine ?** GitHub Pages ne réécrit pas les chemins
> ni ne sert de sous-dossier type `public/`. `index.html`, `sitemap.xml`, `robots.txt`
> et `CNAME` doivent rester à la racine pour que le site soit servi correctement.

---

## Lancer en local

Aucune dépendance à installer — ouvrez simplement le site :

```bash
python3 -m http.server 8080
# → http://localhost:8080
```

Ou via Docker Compose (nginx sur le port 8080) :

```bash
docker compose up --build
# → http://localhost:8080
```

### Régénérer les pages `service-*.html` et `services/`

Les pages de service et la section `services/` sont **générées**. Toute
modification manuelle dessus sera écrasée à la prochaine exécution : passez
toujours par `generate-services.py`.

```bash
python3 generate-services.py
```

- Modifiez les données / textes dans la table `SERVICES` (pages `service-*.html`),
  `KEY_SERVICES` (4 pages `services/<slug>/`) et `HUB` (hub `services/index.html`).
- Le script est **idempotent** : relancer ne change rien si les données n'ont pas bougé.
- **Routage** : les pages `services/<slug>/index.html` permettent des URL propres
  (`https://mecanolyon.fr/services/…`) compatibles GitHub Pages **et** nginx
  (`try_files $uri $uri/ $uri.html`). Les liens internes de ces pages sont
  préfixés via le token `prefix` (`""` à la racine, `"/"` sous `services/`).
- Après ajout d'une page, ajoutez-la aussi dans `sitemap.xml`.

---

## Composant de navigation (`partials/navbar.html`)

La nav existe **à un seul endroit** : `partials/navbar.html`. Elle est injectée à
la génération dans **toutes** les pages :

| Cible | Mécanisme |
|---|---|
| `service-*.html` (générées) | `render_nav(active)` dans `generate-services.py` |
| `index.html`, `zone-intervention.html` | `sync_nav_pages()` — remplace le bloc entre les marqueurs `<!-- nav:begin -->` … `<!-- nav:end -->` |

**Règles :**

- ✏️ Pour changer le menu (libellés, ordre, styles, état `hover`) : éditez
  **`partials/navbar.html`**, jamais une page.
- ⚠️ Ne pas éditer le markup *entre* `nav:begin` et `nav:end` : il est réécrit à
  chaque `python3 generate-services.py`.
- Le partial utilise des tokens `str.format` : **aucune accolade littérale**
  (`{` `}`) autorisée hors tokens (`{diag_class}`, `{abs_class}`, `{zone_class}`,
  `{mobile_*}`, `{home_href}`, `{services_href}`, `{faq_href}`, `{contact_href}`,
  `{prefix}`, `{keys_class}`, `{mobile_keys_class}`, `{keys_hub_href}`).
  `{prefix}` est `""` à la racine et `"/"` pour les pages sous `services/`.
  Un token manquant → le générateur s'arrête sur `KeyError`.
- Si les marqueurs `nav:begin` / `nav:end` sont supprimés d'une page, le
  générateur **sort en erreur** plutôt que de réécrire hors marqueurs.

**Structure actuelle du menu** (Mobile-First, `lg:` pour le desktop) :

- Liens de premier niveau : `Accueil` · `Nos services` ▾ · `Clés &amp; électronique` ▾ ·
  `Actualités` · `Contact`.
- Le déroulant « Nos services » liste **exactement 6 prestations** : Clé de
  voiture, Diagnostic auto, Réparation Airbag *(badge « Nouveau »)*,
  Suppression d'options, Suppression AdBlue, Clonage Calculateur Moteur —
  plus un lien de pied « Voir toutes les prestations » (`{services_href}`).
- Le déroulant **« Clés &amp; électronique »** (`#nav-keys`) liste **4 prestations**
  vers les URL propres de `services/` : Reproduction de clés auto, Perte totale
  de clés, Ouverture de véhicule *(badge « Urgence »)*, Programmation
  électronique ECU — plus un lien de pied « Les 4 services clés auto »
  (`{keys_hub_href}` → `services/`).
- Le comportement (survol/clic/`Échap`/clic extérieur, accordéon mobile,
  icône burger `menu` ⇄ `x`) est porté par **`assets/nav.js`**, chargé en fin
  de partial (`defer`). `nav.js` supporte **N déroulants / N accordéons** via
  les attributs `data-nav-dd*` / `data-nav-acc*` : ajouter un groupe de menu = ajouter
  un bloc doté de ces attributs, sans toucher au JS. Il n'y a **aucune CSS custom** : les états « fermé »
  sont des classes Tailwind statiques du partial, `nav.js` ne fait qu'écrire
  les styles inline qui déclenchent la transition. Aucune classe générée à la
  volée → compatible CDN Tailwind et zéro CLS (menu fermé = 0 px).
- ⚠️ `nav.js` neutralise l'ancien listener inline qui basculait la classe
  `hidden` sur `#mobile-menu` (présent dans le `FOOTER` de
  `generate-services.py`, `index.html` et `zone-intervention.html`). Ce
  listener peut être supprimé sans risque : `assets/nav.js` est devenu la
  seule source d'état.

**Liens en attente de leur page** (à créer + à ajouter dans `sitemap.xml`) :
`actualites.html`, `service-cle-voiture.html`, `service-suppression-options.html`. Ils sont déjà en place dans le partial —
la checklist « aucun lien mort » ne sera verte qu'après leur création.

---

## Déploiement

Le site se déploie automatiquement sur GitHub Pages à chaque push sur `main`.

```bash
git add .
git commit -m "feat(seo): description du changement"
git push origin main
```

Le fichier `CNAME` contient `mecanolyon.fr` : c'est ce qui attache le domaine
personnalisé à la branche publiée.

---

## Checklist SEO avant chaque push

```bash
python3 generate-services.py          # 1. Régénérer (idempotent)
```

Vérifications à passer avant commit :

- [ ] **Liens internes** — aucun lien mort, ancres `#...` résolues
- [ ] **JSON-LD** — parsé sur les 22 pages qui en déclarent (`@graph` : LocalBusiness, Breadcrumb, Service/WebPage, FAQPage — `thank-you.html` est `noindex`)
- [ ] **1 seul `<h1>`** par page
- [ ] **Méta** — title 30–60 car., description 120–160 car.
- [ ] **`sitemap.xml`** — XML valide, toutes les URL existent, couvre les pages indexables
- [ ] **`robots.txt`** — contient `Sitemap: https://mecanolyon.fr/sitemap.xml`
- [ ] **Nav** — marqueurs `nav:begin` / `nav:end` intacts dans `index.html` et `zone-intervention.html`
- [ ] **Assets** — `src` / `href` pointant vers `images/` et `assets/` existants

---

## Notes de structure

- **`images/` et `assets/` sont volontairement séparés.** Les URLs absolues
  `https://mecanolyon.fr/images/…` apparaissent dans les `og:image`, `twitter:image`
  et le schema `LocalBusiness` : déplacer ce fichier créerait des 404 SEO.
- **Maillage interne** — chaque page service déclare ses liens associés via
  `related_links` dans `generate-services.py` (helper `related_block`).
- **Composants serrurerie / électronique (sans nom d'outil ni de marque).**
  Trois blocs Tailwind réutilisables sont définis dans `generate-services.py` —
  formulés uniquement en garanties et compétences génériques (conformité
  éditoriale) : `guarantees_block` (**Garanties & compétences** — équipement
  électronique de précision, taillage laser informatisé, diagnostic
  constructeur, intervention sans dégât), `why_choose_block` (**Pourquoi nous
  choisir** — intervention rapide Lyon & agglomération, devis gratuit,
  travail garanti, matériel de taillage haute précision) et
  `problems_resolved_block` (**Problèmes résolus** — « seule clé perdue »,
  « double rapide », « porte bloquée avec clés à l'intérieur », « calculateur
  en panne »).
  - *Bascule conditionnelle* : `garanties_block` + `why_choose_block` ne sont
    injectés dans `build_page` que si la spec porte `"pillar_blocks": True`
    (les 4 pages `services/<slug>/`) — les 14 pages historiques restent
    intactes. `problems_resolved_block` n'est pas dans `build_page` mais
    explicitement inséré dans `build_services_hub`.
  - *Accueil* : `index.html` (écrit à la main, hors générateur) affiche
    **Problèmes résolus** en `<section id="problemes-resolus">`, placé entre
    `#services-cles` et `#processus` ; ses cartes pointent en liens
    root-relative vers les 4 prestations. Ancre lisible par `#problemes-resolus`.
- **`.agent/`** est ignorée par git : configuration locale des agents, jamais déployée.
