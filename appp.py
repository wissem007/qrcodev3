from flask import Flask, render_template, request, redirect, url_for
import cv2
import os
import psycopg2
import numpy as np
import qrcode
from pyzbar.pyzbar import decode
from PIL import Image
from io import BytesIO

app = Flask(__name__)

if not os.path.exists('static'):
    os.makedirs('static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_qrcode', methods=['POST'])
def generate_qrcode():
    data = request.form.get('data')

    if data:
        img_path = generer_qrcode(data)
        return render_template('success.html', data=data, img_path=img_path)
    else:
        return render_template('error.html', message='Veuillez entrer des données valides.')

@app.route('/scan_qrcode_image', methods=['POST'])
def scan_qrcode_image():
    if 'file' not in request.files:
        return render_template('error.html', message='Aucun fichier téléchargé.')

    file = request.files['file']

    if file.filename == '':
        return render_template('error.html', message='Aucun fichier sélectionné.')

    if file:
        image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
        qr_data = lire_qrcode(image)

        if qr_data:
            return redirect(url_for('recuperer_details_licence', licence_num=qr_data))
        else:
            return render_template('error.html', message='Aucune donnée QR Code trouvée dans l\'image.')

def generer_qrcode(data):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img_path = os.path.join('static', 'qrcode.png')
    img.save(img_path)
    return img_path

def lire_qrcode(image):
    decoded_objects = decode(image)
    qr_data = None

    for obj in decoded_objects:
        qr_data = obj.data.decode('utf-8')

    return qr_data

def save_image(image_data):
    image_dir = 'static/images'
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    img_path = os.path.join('static', 'images', 'photo.jpg')

    # img_path = os.path.join(image_dir, 'photo.jpg')

    with open(img_path, 'wb') as img_file:
        img_file.write(image_data)

    return img_path

@app.route('/recuperer_details_licence/<licence_num>')
def recuperer_details_licence(licence_num):
    connection = psycopg2.connect(
        host="127.0.0.1",
        database="ftf_2022",
        user="postgres",
        password="root"
    )

    cursor = connection.cursor()

    sql_query = f"""
    SELECT 
        i.ct_intervenant_id,
        i.name,
        i.last_name,
        i.alias,
        i.cin_number,
        i.passport_num,
        i.date_of_birth,
        i.place_of_birth,
        t.ct_team_intervenant_id,
        t.ct_team_id,
        t.ct_season_id,
        p.photo_bdata
    FROM 
        sss_competition_db.ct_intervenants i
    LEFT JOIN 
        sss_competition_db.ct_team_intervenants t 
        ON i.ct_intervenant_id = t.ct_intervenant_id
    LEFT JOIN
        sss_competition_db.ct_team_intervenant_photos p
        ON t.ct_team_intervenant_photo_id  = p.ct_team_intervenant_photo_id 
    WHERE 
         i.licence_num = '{licence_num}'
    ORDER BY 
        t.ct_season_id DESC
    LIMIT 1;
    """

    cursor.execute(sql_query)
    details = cursor.fetchone()  # Utilisez fetchone() car vous n'avez besoin que d'une seule ligne

    cursor.close()
    connection.close()

    img_path = None
    if details and details[-1]:  # Vérifiez que details[-1] n'est pas None
        img_path = save_image(details[-1])  # La fonction save_image doit être définie

    return render_template('details.html', details=details, img_path=img_path)

if __name__ == '__main__':
    app.run(debug=True)
