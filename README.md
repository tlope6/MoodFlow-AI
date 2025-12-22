🎧 MoodFlow AI

Audio-Driven Music Recommendation System using Spotify

MoodFlow AI is an end-to-end machine learning application that analyzes user-uploaded audio to infer mood and genre, then generates personalized music recommendations (artists, tracks, and playlists) using the Spotify Web API.

This project demonstrates applied digital signal processing, ML inference, API integration, and product-level system design.

🚀 Features

🎵 Upload an audio file (MP3/WAV/OGG)

📊 Extract audio features using DSP techniques

🧠 Predict mood and genre from raw audio

🔎 Retrieve relevant Spotify artists, tracks, and playlists

🎶 Generate playlist-style recommendations using Spotify audio features

🖥 Interactive web interface with audio previews and album art

🧩 Modular, scalable project architecture

🧠 System Architecture
User Audio Upload
        ↓
Audio Feature Extraction (Librosa)
        ↓
Mood & Genre Inference (ML / Heuristics)
        ↓
Spotify API Integration
        ↓
Artists • Tracks • Playlists • Explanations
        ↓
Streamlit UI


Each component is isolated into its own module to reflect real-world ML system design.

🛠️ Tech Stack

Languages

Python

Libraries & Frameworks

Librosa (audio signal processing)

NumPy / Pandas

Scikit-learn

Spotipy (Spotify Web API wrapper)

Streamlit (UI)

APIs

Spotify Web API (search, recommendations, audio features)

📁 Project Structure
MoodFlow/
├── src/
│   ├── audio/          # Audio loading & feature extraction
│   ├── ml/             # Mood & genre inference logic
│   ├── api/            # Spotify API client
│   ├── recommender/    # Playlist & similarity engines
│   ├── explain/        # Recommendation explanations
│   ├── ui/             # Streamlit interface
│   └── utils/          # Helpers & history tracking
│
├── data/
│   └── history/        # User session history
│
├── tests/              # Unit test placeholders
├── requirements.txt
└── README.md



⚙️ Setup & Installation
1️⃣ Clone the repository
git clone https://github.com/yourusername/moodflow-ai.git
cd moodflow-ai

2️⃣ Create & activate a virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Set up Spotify API credentials

Create the file:

src/secrets/spotify_keys.py


Add:

CLIENT_ID = "your_spotify_client_id"
CLIENT_SECRET = "your_spotify_client_secret"


⚠️ This file is excluded via .gitignore.

▶️ Running the App

From the project root:

streamlit run src/ui/app.py


Then open:

http://localhost:8501

🧪 Example Workflow

Upload a song file

System extracts audio features (tempo, MFCCs, spectral centroid, etc.)

Mood & genre are inferred from the audio profile

Spotify API returns relevant:

Artists

Tracks with previews

Playlists

UI displays recommendations with explanations

🧩 Design Highlights

Modular architecture: clean separation of concerns (audio, ML, API, UI)

Defensive programming: handles missing Spotify data safely

Explainability: provides insight into why recommendations were made

Scalable foundation: easy to replace heuristics with trained ML models

🔮 Future Improvements

Train supervised ML models for genre & mood classification

Add user login and personalized Spotify playlist creation

Improve genre-to-Spotify mapping using clustering

Add similarity scoring using cosine distance on audio features

Deploy as a hosted web service

Expand unit test coverage

📌 Why This Project

This project was built to explore:

Applied machine learning

Digital signal processing

Real-world API integration

End-to-end system design
