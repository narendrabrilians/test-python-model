from flask import Flask, request, jsonify
import tensorflow as tf
from PIL import Image
import numpy as np
import io
import os

# Inisialisasi Flask
app = Flask(__name__)

# Load model yang sudah disimpan
model = tf.keras.models.load_model('./model/dead_chicken_model.h5')

# Preprocessing fungsi untuk gambar
def preprocess_image(image, target_size=(224, 224)):
    """
    Mengubah ukuran gambar ke target_size dan menormalkan piksel.
    """
    image = image.resize(target_size)  # Resize gambar
    image = np.array(image) / 255.0   # Normalisasi piksel ke rentang [0, 1]
    image = np.expand_dims(image, axis=0)  # Tambahkan batch dimension
    return image

@app.route('/')
def hello_world():
    """
    Endpoint untuk mengembalikan 'Hello World' sebagai respons.
    """
    return "Hello World"

@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint untuk menerima gambar dan memberikan prediksi.
    """
    try:
        # Periksa apakah file dikirimkan
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400
        
        # Ambil file gambar dari request
        file = request.files['file']
        
        # Buka file gambar
        image = Image.open(io.BytesIO(file.read()))
        
        # Preprocessing gambar
        processed_image = preprocess_image(image)
        
        # Prediksi menggunakan model
        prediction = model.predict(processed_image)[0][0]
        
        # Tentukan hasil prediksi (dead chicken: boolean)
        dead_chicken = bool(prediction > 0.5)  # Konversi ke tipe Python bool
        
        # Mengembalikan hasil prediksi
        return jsonify({'dead_chicken': dead_chicken})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Jalankan server Flask
if __name__ == '__main__':
    # Gunakan port yang diberikan App Engine, atau default ke 8080 untuk pengembangan lokal
    port = int(os.environ.get("PORT", 8080)) 
    app.run(host='0.0.0.0', port=port)
