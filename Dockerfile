FROM alpine:latest

RUN apk add --no-cache python3 py3-pip build-base libffi-dev musl-dev linux-headers python3-dev

# Créer un environnement virtuel
RUN python3 -m venv /venv

WORKDIR /app
COPY . /app

RUN /venv/bin/pip install --no-cache-dir -r requirements.txt

# Copier le script entrypoint.sh dans le conteneur
COPY entrypoint.sh /app/entrypoint.sh

# Vérifier les permissions du fichier entrypoint.sh
RUN ls -l /app

# Rendre le script d'entrée exécutable
RUN chmod +x /app/entrypoint.sh

# Définir l'environnement virtuel pour les commandes suivantes
ENV PATH="/venv/bin:$PATH"

# Définir le script entrypoint.sh comme point d'entrée
ENTRYPOINT ["sh", "/app/entrypoint.sh"]
