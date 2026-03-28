# 🎵 Music Recommender

A music recommendation system built with Machine Learning (KNN) and Flask, trained on 81,000+ Spotify tracks.

## Demo

> Live demo coming soon — run locally with the instructions below.

## How It Works

1. Enter a song name (and optionally an artist)
2. The ML model finds songs with similar audio features
3. Results are filtered by genre and popularity

The model uses **K-Nearest Neighbors (KNN)** with cosine similarity across 9 audio features:
- Energy, Valence (mood), Danceability, Tempo
- Acousticness, Instrumentalness, Loudness
- Speechiness, Liveness

## Tech Stack

- **ML Model:** scikit-learn (KNN + cosine similarity)
- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript
- **Containerization:** Docker
- **Dataset:** [Spotify Tracks Dataset](https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset) (114K tracks)

## Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/Emirgzer/spotify-recommender.git
cd spotify-recommender
```

### 2. Set up virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Download dataset and train model

Download the dataset from [Kaggle](https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset) and save as `spotify.csv`, then run the Jupyter notebook to train and save the model.

### 4. Run the app
```bash
python3 app.py
```

Visit `http://localhost:5000`

### 5. Run with Docker
```bash
docker build -t spotify-recommender .
docker run -p 5000:5000 spotify-recommender
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Web UI |
| POST | `/recommend` | Get recommendations |
| GET | `/search?q=` | Search tracks |

### Example Request
```bash
curl -X POST http://localhost:5000/recommend \
  -H "Content-Type: application/json" \
  -d '{"track_name": "Blinding Lights", "artist": "The Weeknd"}'
```

## Limitations

- Recommendations are based purely on audio features, not listening history
- Results may vary — songs with similar sonic profiles may span different genres
- Dataset popularity scores may not reflect current trends

## Author

Emir Gizer — [GitHub](https://github.com/Emirgzer)