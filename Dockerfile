# Utilisez une image de base légère pour Python
FROM python:3.9-slim

# Définissez le répertoire de travail dans le conteneur
WORKDIR /app

# Copiez les fichiers nécessaires dans le conteneur
COPY requirements.txt /app/requirements.txt
COPY app.py /app/app.py
COPY static /app/static
COPY templates /app/templates

# Installez les dépendances Python
#RUN pip install --no-cache-dir -r /app/requirements.txt
RUN pip install --no-cache-dir Flask==2.1.3 -r /app/requirements.txt


# Exposez le port sur lequel l'application Flask écoute
EXPOSE 5000

# Démarrez l'application Flask
CMD ["python", "app.py"]
