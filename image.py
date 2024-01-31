from PIL import Image
from io import BytesIO
import psycopg2

# Connectez-vous à la base de données
connection = psycopg2.connect(
    host="127.0.0.1",
    database="ftf_2022",
    user="postgres",
    password="root"
)

cursor = connection.cursor()

# Exécutez votre requête SQL pour récupérer les données de la colonne photo_bdata
cursor.execute("SELECT photo_bdata FROM sss_competition_db.ct_team_intervenant_photos where ct_team_intervenant_photo_id=759882;")  # Remplacez ... par votre condition WHERE

# Récupérez les données binaires
photo_data_binary = cursor.fetchone()[0]

# Fermez la connexion
cursor.close()
connection.close()

# Maintenant, vous avez les données binaires. Vous pouvez les utiliser comme bon vous semble.
image = Image.open(BytesIO(photo_data_binary))

# Affichez l'image
image.show()