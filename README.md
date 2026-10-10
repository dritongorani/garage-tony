# Mecanoo Lyon — mecanolyon.fr

Site **100 % statique** (HTML / CSS / JS) pour *Mecanoo Lyon*, électronique automobile
et diagnostic à Lyon : diagnostic valise OBD, clonage ECU/BSI, reprogrammation Stage 1
& Éthanol E85, solutions anti-pollution (FAP / EGR / AdBlue) et réparation de bloc ABS.

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
├── zone-intervention.html        # Zone d'intervention (Rhône / Ain)
├── thank-you.html                # Page de remerciement (noindex)
│
├── sitemap.xml                   # Sitemap (13 URL indexables)
├── robots.txt                    # + directive Sitemap
├── CNAME                         # Domaine personnalisé GitHub Pages
│
├── images/                       # Images référencées par les balises <img> / og:image
│   └── seo-reparation-voiture-lyon_1.jpg
├── assets/                       # Scripts et assets partagés
│   └── canonical-host.js         # Redirige www → domaine canonique
│
├── generate-services.py          # ⚠️ Source de vérité des pages service-*.html
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

### Régénérer les pages `service-*.html`

Les pages de service sont **générées**. Toute modification manuelle dessus sera
écrasée à la prochaine exécution : passez toujours par `generate-services.py`.

```bash
python3 generate-services.py
```

- Modifiez les données / textes dans la table `SERVICES` (début de fichier).
- Le script est **idempotent** : relancer ne change rien si les données n'ont pas bougé.
- Après ajout d'une page, ajoutez-la aussi dans `sitemap.xml`.

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
- [ ] **JSON-LD** — parsé sur les 14 pages (`@graph` : LocalBusiness, Breadcrumb, Service, FAQPage)
- [ ] **1 seul `<h1>`** par page
- [ ] **Méta** — title 30–60 car., description 120–160 car.
- [ ] **`sitemap.xml`** — XML valide, toutes les URL existent, couvre les pages indexables
- [ ] **`robots.txt`** — contient `Sitemap: https://mecanolyon.fr/sitemap.xml`
- [ ] **Assets** — `src` / `href` pointant vers `images/` et `assets/` existants

---

## Notes de structure

- **`images/` et `assets/` sont volontairement séparés.** Les URLs absolues
  `https://mecanolyon.fr/images/…` apparaissent dans les `og:image`, `twitter:image`
  et le schema `LocalBusiness` : déplacer ce fichier créerait des 404 SEO.
- **Maillage interne** — chaque page service déclare ses liens associés via
  `related_links` dans `generate-services.py` (helper `related_block`).
- **`.agent/`** est ignorée par git : configuration locale des agents, jamais déployée.
