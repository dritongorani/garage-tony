# 🚗 Garage GoAuto — Site Vitrine Mécanicien à Domicile

Site web statique pour **Garage GoAuto**, un service de mécanique mobile intervenant à domicile sur **Lyon (69)** et **Meximieux / Ain (01)**.

---

## 📋 Description

Site vitrine one-page présentant les prestations d'un mécanicien automobile à domicile. Il permet aux visiteurs de découvrir les services proposés, la zone d'intervention, et de prendre contact rapidement par téléphone, WhatsApp ou formulaire en ligne.

---

## ✨ Fonctionnalités

- **Section Hero** avec image de fond en parallaxe et appels à l'action
- **Présentation des prestations** : diagnostic OBD, entretien, freinage, distribution
- **Zone d'intervention** : villes couvertes dans le Rhône et l'Ain
- **Contact multi-canal** : appel direct, WhatsApp, formulaire en ligne
- **Carte Google Maps** intégrée
- **Design responsive** adapté mobile et desktop

---

## 🛠️ Stack technique

| Technologie | Usage |
|-------------|-------|
| HTML5 | Structure de la page |
| CSS3 | Mise en forme, animations, responsive |
| Google Maps Embed | Carte de localisation |

Aucune dépendance externe, aucun framework — HTML/CSS pur.

---

## 📁 Structure du projet

```
garage-goauto/
├── index.html              # Page principale
├── style.css               # Feuille de styles principale
├── formulaire.html         # Page formulaire de devis
├── formulaire.css          # Styles du formulaire
├── script.js               # Scripts JavaScript
├── sitemap.xml             # Sitemap pour le référencement SEO
├── CNAME                   # Nom de domaine personnalisé (GitHub Pages)
├── garage.jpg              # Image de fond hero
├── logo_go_auto_bg.png     # Logo fond transparent
├── logo_go_auto.png.png    # Logo variante
├── voiture_logo.png.png    # Icône voiture
```

---

## 🤖 Chatbot IA local

Le chatbot du site peut utiliser de vraies réponses IA via un backend local sécurisé.

1. Copiez `.env.example` en `.env`
2. Mettez votre clé dans `OPENAI_API_KEY`
3. Lancez l'API chat :

```bash
node chat-server.js
```

4. Gardez aussi le serveur statique du site actif :

```bash
python -m http.server 5500
```

Le front appelle `http://localhost:8787/api/chat`.

---

## 🚀 Déploiement

Le site est entièrement statique. Il peut être hébergé sur :

- **GitHub Pages** : activez Pages depuis les paramètres du dépôt (branche `main`, dossier `/root`)
- **Netlify / Vercel** : glissez-déposez le dossier ou connectez le repo
- Tout hébergement supportant des fichiers statiques

---

## 📞 Contact professionnel

**Garage GoAuto**
- 📱 Tél / WhatsApp : [06 03 43 99 54](tel:+33603439954)
- 📍 Meximieux (01) — Interventions Lyon & agglomération

---

## 📄 Licence

Projet privé — © 2025 Garage GoAuto. Tous droits réservés.
