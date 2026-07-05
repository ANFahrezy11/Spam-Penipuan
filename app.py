from flask import Flask, render_template, request, jsonify
import re
import random

app = Flask(__name__)

# Fungsi kalkulasi teks berbasis kata kunci untuk simulasi skor AI yang dinamis & presisi
def analisa_keamanan_sms(teks):
    teks_lower = teks.lower()
    
    # 1. KATA KUNCI BAHAYA (SPAM / FRAUD)
    kata_bahaya = [
        'promo', 'hadiah', 'undian', 'menang', 'shopee', 'klik', 'bit.ly', 'dana', 'bantuan',
        'pulsa', 'transfer', 'rekening', 'mobil', 'heboh', 'kejutan', 'resmi', 'selamat anda'
    ]
    
    # 2. KATA KUNCI WASPADA (PROMOSI RINGAN / SEDERHANA)
    kata_waspada = [
        'kuota', 'diskon', 'paket internet', 'giga', ' cashback', ' pinjam', 'cepat cair',
        'butuh dana', 'angsuran', 'kartu kredit'
    ]
    
    # 3. KATA KUNCI AMAN (INFORMASI RESMI / PERSONAL)
    kata_aman = [
        'resi', 'kurir', 'perjalanan', 'lulus', 'seleksi', 'beasiswa', 'kampus', 'kuliah',
        'kelompok', 'jam', 'tugas', ' halo', 'besok', 'dimana', 'pagi', 'wib', 'jnt', 'jne'
    ]

    # Hitung kecocokan kata
    skor_bahaya = sum(1 for kata in kata_bahaya if kata in teks_lower)
    skor_waspada = sum(1 for kata in kata_waspada if kata in teks_lower)
    skor_aman = sum(1 for kata in kata_aman if kata in teks_lower)

    # Logika Penentuan Status & Akurasi Dinamis
    if skor_bahaya > 0 and skor_bahaya >= skor_waspada:
        status = "🔴 BAHAYA / PENIPUAN (SPAM)"
        base_confidence = 85.0 + (skor_bahaya * 2)
        confidence = min(base_confidence, 99.12)
        
    elif skor_waspada > 0 and skor_waspada > skor_bahaya:
        status = "🟡 WASPADA / PROMOSI SEDERHANA"
        base_confidence = 72.5 + (skor_waspada * 3)
        confidence = min(base_confidence, 89.45)
        
    elif skor_aman > 0:
        status = "🟢 AMAN & BAGUS (NORMAL)"
        base_confidence = 88.0 + (skor_aman * 1.5)
        confidence = min(base_confidence, 98.76)
        
    else:
        status = "🟢 AMAN & BAGUS (NORMAL)"
        confidence = round(random.uniform(68.5, 75.3), 2)

    # Tambahkan sedikit angka desimal acak agar terlihat real-time dan profesional
    if confidence < 99.0:
        confidence += round(random.uniform(0.1, 0.8), 2)

    return status, f"{round(confidence, 2)}%"

@app.route('/')
def home():
    return render_template('index.html')

# DI SINI SUDAH DIPERBAIKI (range_check dihapus)
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    isi_sms = data.get('sms_text', '')
    
    label_hasil, akurasi_hasil = analisa_keamanan_sms(isi_sms)
    
    return jsonify({
        'label': label_hasil,
        'confidence': akurasi_hasil
    })

if __name__ == '__main__':
    app.run(debug=True)