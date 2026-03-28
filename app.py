from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
import pickle

app = Flask(__name__)

model = pickle.load(open('model.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))
df_clean = pickle.load(open('df_clean.pkl', 'rb'))
X_v6 = pickle.load(open('X_v6.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    sarki_adi = data.get('track_name', '')
    artist = data.get('artist', None)
    min_popularity = data.get('min_popularity', 60)

    if artist:
        sonuc = df_clean[
            (df_clean['track_name'].str.lower() == sarki_adi.lower()) &
            (df_clean['artists'].str.lower().str.contains(artist.lower()))
        ]
    else:
        sonuc = df_clean[df_clean['track_name'].str.lower() == sarki_adi.lower()]

    if len(sonuc) == 0:
        return jsonify({'error': f"'{sarki_adi}' bulunamadı!"}), 404

    idx = sonuc.index[0]
    sarki_genre = sonuc.iloc[0]['track_genre']

    distances, indices = model.kneighbors([X_v6[idx]], n_neighbors=300)

    oneriler = []
    seen = set()

    # Önce aynı genre'dan
    for ind in indices[0][1:]:
        s = df_clean.iloc[ind]
        key = f"{s['track_name']}_{s['artists']}"
        if s['track_genre'] == sarki_genre and s['popularity'] >= min_popularity and key not in seen and len(oneriler) < 10:
            seen.add(key)
            oneriler.append({
                'track_name': s['track_name'],
                'artists': s['artists'],
                'popularity': int(s['popularity'])
            })

    # Yeterli değilse genre dışından ekle
    if len(oneriler) < 5:
        for ind in indices[0][1:]:
            s = df_clean.iloc[ind]
            key = f"{s['track_name']}_{s['artists']}"
            if s['popularity'] >= min_popularity and key not in seen and len(oneriler) < 10:
                seen.add(key)
                oneriler.append({
                    'track_name': s['track_name'],
                    'artists': s['artists'],
                    'popularity': int(s['popularity'])
                })

    if not oneriler:
        return jsonify({'error': 'Yeterli popülerlikte öneri bulunamadı.'}), 404

    return jsonify({
        'query': sarki_adi,
        'recommendations': oneriler
    })

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'q parametresi gerekli'}), 400

    sonuclar = df_clean[df_clean['track_name'].str.lower().str.contains(query.lower())]
    sonuclar = sonuclar[['track_name', 'artists', 'popularity']].head(10)

    return jsonify(sonuclar.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)