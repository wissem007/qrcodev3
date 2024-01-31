from flask import Flask, render_template, request, redirect, url_for, send_file
import cv2
import os
import psycopg2
import numpy as np
import qrcode
from pyzbar.pyzbar import decode
from PIL import Image
from io import BytesIO

app = Flask(__name__)

# ... Votre code existant ...

@app.route('/get_image/<int:photo_id>')
def get_image(photo_id):
    connection = psycopg2.connect(
        host="127.0.0.1",
        database="ftf_2022",
        user="postgres",
        password="root"
    )

    cursor = connection.cursor()

    cursor.execute("SELECT photo_bdata FROM sss_competition_db.ct_team_intervenant_photos WHERE ct_team_intervenant_photo_id = %s;", (photo_id,))
    photo_data_binary = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return send_file(BytesIO(photo_data_binary), mimetype='image/jpeg')

# ... Le reste de votre code ...
