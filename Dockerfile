# Image de base légère et sécurisée
FROM nginx:alpine

# Définition des métadonnées
LABEL maintainer="Mecanoo Lyon" \
      description="Serveur web Nginx pour le site statique Mecanoo Lyon"

# Remplacement de la configuration Nginx par défaut
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copie des fichiers statiques du site
COPY . /usr/share/nginx/html

# Exposition du port HTTP interne
EXPOSE 80

# Healthcheck de conformité du service
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

# Démarrage de Nginx au premier plan
CMD ["nginx", "-g", "daemon off;"]
