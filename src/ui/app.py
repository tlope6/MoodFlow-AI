import streamlit as st

from src.audio.analyze import analyze_audio
from src.ml.mood_model import predict_mood
from src.ml.genre_model import predict_genre
from src.api.spotify_client import SpotifyClient
from src.recommender.playlist_engine import PlaylistEngine
from src.explainer.explainer import explain_recommendation
from src.utils.history_manager import append_history, read_history
from src.ui.components import card_title, render_artist, render_track


def main():
    st.set_page_config(page_title="MoodFlow AI", page_icon="🎧", layout="wide")
    st.title("🎧 MoodFlow AI — Spotify Music Assistant")

    with st.sidebar:
        st.header("History")
        if st.button("Refresh history"):
            pass
        hist = read_history()
        if not hist:
            st.caption("No sessions yet.")
        else:
            # show last 5
            for h in hist[-5:][::-1]:
                st.caption(f"{h.get('timestamp','')} • mood={h.get('mood')} • genre={h.get('genre')}")

    uploaded = st.file_uploader("Upload an audio file", type=["mp3", "wav", "ogg"])
    if not uploaded:
        st.info("Upload a song to get recommendations.")
        return

    st.audio(uploaded)

    with st.spinner("Analyzing audio..."):
        user_features = analyze_audio(uploaded)

    mood = predict_mood(user_features)
    genre_guess = predict_genre(user_features)

    sp = SpotifyClient()
    seed_genres = set(sp.available_seed_genres())

    # Spotify has a fixed list of genres; map your guess to a valid one.
    # We'll improve mapping later; for now, fallback to 'pop' if not valid.
    genre = genre_guess if genre_guess in seed_genres else "pop"

    append_history({"mood": mood, "genre": genre})

    colA, colB = st.columns([1, 1])

    with colA:
        card_title("Your Analysis")
        st.write(f"**Mood:** `{mood}`")
        st.write(f"**Genre seed:** `{genre}` (guess was `{genre_guess}`)")
        with st.expander("Debug: extracted features"):
            st.json(user_features)

        card_title("Why these recommendations?")
        st.markdown(explain_recommendation(mood, genre, user_features))

    with colB:
        card_title("Spotify Artists")
        artists = sp.get_artists_from_genre(genre, limit=6)
        for a in artists:
            render_artist(a)

    st.divider()

    tab1, tab2, tab3 = st.tabs(["Tracks", "Playlist Builder", "Playlists"])

    with tab1:
        card_title("Tracks in this genre")
        tracks = sp.get_tracks_from_genre(genre, limit=8)
        for t in tracks:
            render_track(t)

    with tab2:
        card_title("Auto-playlist (Spotify Recommendations)", "Uses mood → target energy/valence/danceability")
        engine = PlaylistEngine(sp)
        rec_tracks = engine.build(seed_genre=genre, mood=mood, limit=10)

        # Fetch audio-features to enrich explanation later
        track_ids = [t["id"] for t in rec_tracks if t.get("id")]
        af = sp.audio_features(track_ids) if track_ids else []
        af_by_id = {f["id"]: f for f in af}

        for t in rec_tracks:
            t_dict = {
                "title": t["name"],
                "artist": t["artists"][0]["name"] if t.get("artists") else "Unknown",
                "url": t["external_urls"]["spotify"],
                "preview": t.get("preview_url"),
                "cover": t["album"]["images"][0]["url"] if t.get("album", {}).get("images") else None,
            }
            render_track(t_dict)
            f = af_by_id.get(t["id"])
            if f:
                st.caption(f"energy={f.get('energy',0):.2f} • valence={f.get('valence',0):.2f} • danceability={f.get('danceability',0):.2f}")

    with tab3:
        card_title("Playlists")
        pls = sp.playlists_for_genre(genre, limit=8)
        for p in pls:
            st.markdown(f"**[{p['name']}]({p['url']})** — {p.get('owner','')}")
            if p.get("image"):
                st.image(p["image"], width=200)


if __name__ == "__main__":
    main()
