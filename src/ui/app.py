import streamlit as st
from typing import Optional

from src.audio.analyze import analyze_audio
from src.ml.mood_model import predict_mood
from src.ml.genre_model import predict_genre

from src.api.spotify_user_client import SpotifyUserClient
from src.api.spotify_client_public import SpotifyClientPublic
from src.api.spotify_genres import SPOTIFY_SEED_GENRES, GENRE_MAP

from src.recommender.playlist_engine import PlaylistEngine


def normalize_spotify_genre(raw: str) -> str:
    g = raw.lower().strip()
    return g if g in SPOTIFY_SEED_GENRES else "pop"


def main():
    st.set_page_config(
        page_title="MoodFlow AI",
        page_icon="🎧",
        layout="wide"
    )

    st.title("🎧 MoodFlow AI — Music Intelligence Assistant")

    # ---------------------------
    # Sidebar: Spotify Login
    # ---------------------------
    with st.sidebar:
        st.header("Spotify Access")

        use_login = st.checkbox(
            "Login for personalized recommendations",
            value=True
        )

        sp_user: Optional[SpotifyUserClient] = None
        sp_public = SpotifyClientPublic()

        if use_login:
            try:
                client = SpotifyUserClient()
                user = client.me()
                sp_user = client
                st.success(f"Connected as {user.get('display_name', 'Spotify User')} ✅")
            except Exception:
                st.warning("Spotify login not completed. Using guest mode.")
        else:
            st.info("Guest mode enabled.")

    # ---------------------------
    # Upload audio
    # ---------------------------
    uploaded = st.file_uploader(
        "Upload an audio file",
        type=["mp3", "wav", "ogg"]
    )

    if not uploaded:
        st.info("Upload a song to analyze mood and generate recommendations.")
        return

    st.audio(uploaded)

    # ---------------------------
    # Analyze audio
    # ---------------------------
    with st.spinner("Analyzing audio..."):
        user_features = analyze_audio(uploaded)

    mood = predict_mood(user_features)
    raw_genre = predict_genre(user_features)
    genre = normalize_spotify_genre(raw_genre)
    
    # Let user override the predicted genre
    st.info(f"🤖 AI predicted: **{raw_genre}** (mapped to **{genre}**)")
    
    # Show genre selector
    all_genres = sorted(list(SPOTIFY_SEED_GENRES))
    genre_index = all_genres.index(genre) if genre in all_genres else 0
    
    selected_genre = st.selectbox(
        "Adjust genre if needed:",
        options=all_genres,
        index=genre_index
    )
    
    # Use the selected genre instead
    genre = selected_genre
    
    # Try to find this song on Spotify to use as a seed
    seed_track_id = None
    uploaded_track_name = None
    uploaded_artist_name = None
    uploaded_artist_id = None
    
    # Extract filename without extension as a search query
    filename = uploaded.name.rsplit('.', 1)[0]
    
    try:
        # Search Spotify for this song
        search_results = sp_public.sp.search(q=filename, type='track', limit=1)
        if search_results and search_results.get('tracks', {}).get('items'):
            found_track = search_results['tracks']['items'][0]
            seed_track_id = found_track['id']
            uploaded_track_name = f"{found_track['name']} by {found_track['artists'][0]['name']}"
            uploaded_artist_name = found_track['artists'][0]['name']
            uploaded_artist_id = found_track['artists'][0]['id']
            st.info(f"🎵 Found match on Spotify: {uploaded_track_name}")
    except:
        st.caption("Could not find this song on Spotify, using genre-based recommendations")


    # ---------------------------
    # Top layout
    # ---------------------------
    colA, colB = st.columns([1, 1])

    with colA:
        st.markdown("### Your Analysis")
        st.write(f"**Mood:** `{mood}`")
        st.write(f"**Genre:** `{genre}` (predicted `{raw_genre}`)")

        with st.expander("Extracted audio features"):
            st.json(user_features)

    with colB:
        st.markdown("### Top Artists")
        
        # If we found the uploaded song, show RELATED artists to that specific artist
        if uploaded_artist_id:
            try:
                # Try to get related artists
                related = sp_public.sp.artist_related_artists(uploaded_artist_id)
                
                if related and 'artists' in related and len(related['artists']) > 0:
                    # Show the original artist + top 5 related
                    try:
                        original_artist = sp_public.sp.artist(uploaded_artist_id)
                        if original_artist:
                            st.markdown(f"**{original_artist['name']}** ⭐ (Your song)")
                            if original_artist.get('images'):
                                st.image(original_artist['images'][0]['url'], width=100)
                    except:
                        st.markdown(f"**{uploaded_artist_name}** ⭐ (Your song)")
                    
                    for artist in related['artists'][:5]:
                        st.markdown(f"**{artist['name']}**")
                        if artist.get('images'):
                            st.image(artist['images'][0]['url'], width=100)
                else:
                    # No related artists found, use genre fallback
                    raise Exception("No related artists")
                    
            except Exception as e:
                print(f"Could not get related artists: {e}")
                # Fallback to curated list
                from src.recommender.genre_strategies import GENRE_SEED_ARTISTS, ARTIST_FOCUSED_GENRES
                
                st.caption("Showing popular artists in this genre")
                
                if genre in ARTIST_FOCUSED_GENRES:
                    seed_artists = GENRE_SEED_ARTISTS.get(genre, [])[:6]
                    for artist_name in seed_artists:
                        st.markdown(f"**{artist_name}**")
                else:
                    artists = sp_public.get_artists_from_genre(genre, limit=6)
                    for a in artists:
                        st.markdown(f"**{a.get('name', 'Unknown')}**")
                        if a.get('image'):
                            st.image(a['image'], width=100)
        else:
            # No uploaded song found - use curated lists
            from src.recommender.genre_strategies import GENRE_SEED_ARTISTS, ARTIST_FOCUSED_GENRES
            
            if genre in ARTIST_FOCUSED_GENRES:
                seed_artists = GENRE_SEED_ARTISTS.get(genre, [])[:6]
                for artist_name in seed_artists:
                    try:
                        results = sp_public.sp.search(q=f"artist:{artist_name}", type='artist', limit=1)
                        if results and 'artists' in results and results['artists']['items']:
                            artist = results['artists']['items'][0]
                            st.markdown(f"**{artist['name']}**")
                            if artist.get('images'):
                                st.image(artist['images'][0]['url'], width=100)
                    except:
                        st.markdown(f"**{artist_name}**")
            else:
                artists = sp_public.get_artists_from_genre(genre, limit=6)
                for a in artists:
                    st.markdown(f"**{a.get('name', 'Unknown')}**")
                    if a.get('image'):
                        st.image(a['image'], width=100)

    st.divider()

    # ---------------------------
    # Tabs
    # ---------------------------
    tab1, tab2, tab3 = st.tabs(
        ["Tracks", "Playlist Builder", "Albums"]
    )

    # ---------------------------
    # Tracks (public)
    # ---------------------------
    with tab1:
        st.markdown("### Tracks in this genre")
        
        # If we have the uploaded artist, show their tracks + related artists' tracks
        if uploaded_artist_id:
            all_genre_tracks = []
            
            try:
                # Get related artists
                related = sp_public.sp.artist_related_artists(uploaded_artist_id)
                artists_to_show = [uploaded_artist_name]
                
                if related and 'artists' in related and len(related['artists']) > 0:
                    artists_to_show.extend([a['name'] for a in related['artists'][:3]])
                
                # Get recent tracks from these artists
                for artist_name in artists_to_show:
                    try:
                        results = sp_public.sp.search(
                            q=f'artist:"{artist_name}"', 
                            type='track', 
                            limit=2
                        )
                        if results and 'tracks' in results:
                            all_genre_tracks.extend(results['tracks']['items'])
                    except:
                        continue
                
                # Display tracks
                if len(all_genre_tracks) > 0:
                    for t in all_genre_tracks[:8]:
                        if t:
                            st.markdown(f"**{t['name']}** by {t['artists'][0]['name']}")
                            if t.get('album', {}).get('images'):
                                st.image(t['album']['images'][0]['url'], width=100)
                            if t.get('external_urls', {}).get('spotify'):
                                st.markdown(f"[Open on Spotify]({t['external_urls']['spotify']})")
                else:
                    raise Exception("No tracks found")
                    
            except Exception as e:
                print(f"Could not get artist tracks: {e}")
                # Fallback to standard search
                from src.recommender.genre_strategies import GENRE_SEED_ARTISTS, ARTIST_FOCUSED_GENRES
                
                if genre in ARTIST_FOCUSED_GENRES:
                    seed_artists_for_tracks = GENRE_SEED_ARTISTS.get(genre, [])[:3]
                    all_genre_tracks = []
                    
                    for artist_name in seed_artists_for_tracks:
                        try:
                            results = sp_public.sp.search(
                                q=f'artist:"{artist_name}" year:2023-2024', 
                                type='track', 
                                limit=3
                            )
                            if results and 'tracks' in results:
                                all_genre_tracks.extend(results['tracks']['items'])
                        except:
                            continue
                    
                    for t in all_genre_tracks[:8]:
                        if t:
                            st.markdown(f"**{t['name']}** by {t['artists'][0]['name']}")
                            if t.get('album', {}).get('images'):
                                st.image(t['album']['images'][0]['url'], width=100)
                            if t.get('external_urls', {}).get('spotify'):
                                st.markdown(f"[Open on Spotify]({t['external_urls']['spotify']})")
                else:
                    tracks = sp_public.get_tracks_from_genre(genre, limit=8)
                    for t in tracks:
                        st.markdown(f"**{t.get('title', 'Unknown')}** by {t.get('artist', 'Unknown')}")
                        if t.get('cover'):
                            st.image(t['cover'], width=100)
                        if t.get('url'):
                            st.markdown(f"[Open on Spotify]({t['url']})")
        
        # For artist-focused genres without uploaded song, use curated artists
        elif genre in ARTIST_FOCUSED_GENRES:
            seed_artists_for_tracks = GENRE_SEED_ARTISTS.get(genre, [])[:3]
            all_genre_tracks = []
            
            for artist_name in seed_artists_for_tracks:
                try:
                    results = sp_public.sp.search(
                        q=f'artist:"{artist_name}" year:2023-2024', 
                        type='track', 
                        limit=3
                    )
                    if results and 'tracks' in results:
                        all_genre_tracks.extend(results['tracks']['items'])
                except:
                    continue
            
            for t in all_genre_tracks[:8]:
                if t:
                    st.markdown(f"**{t['name']}** by {t['artists'][0]['name']}")
                    if t.get('album', {}).get('images'):
                        st.image(t['album']['images'][0]['url'], width=100)
                    if t.get('external_urls', {}).get('spotify'):
                        st.markdown(f"[Open on Spotify]({t['external_urls']['spotify']})")
        else:
            # Standard search for other genres
            tracks = sp_public.get_tracks_from_genre(genre, limit=8)
            for t in tracks:
                st.markdown(f"**{t.get('title', 'Unknown')}** by {t.get('artist', 'Unknown')}")
                if t.get('cover'):
                    st.image(t['cover'], width=100)
                if t.get('url'):
                    st.markdown(f"[Open on Spotify]({t['url']})")

    # ---------------------------
    # Playlist Builder (OAuth)
    # ---------------------------
    with tab2:
        st.markdown("### MoodFlow Playlist Builder")
        st.caption("Genre-based recommendations from Spotify")

        if sp_user is None:
            st.error("Spotify authentication required.")
            st.stop()

        engine = PlaylistEngine(sp_user)
        ranked = engine.recommend_ranked(
            genre=genre,
            mood=mood,  # Note: mood is ignored in simplified version
            limit=10
        )

        if not ranked:
            st.warning("No recommendations returned.")
        else:
            for item in ranked:
                track = item["track"]

                # Display track info
                col1, col2 = st.columns([1, 4])
                
                with col1:
                    if track.get("album", {}).get("images"):
                        st.image(track["album"]["images"][0]["url"], width=80)
                
                with col2:
                    st.markdown(f"**{track['name']}**")
                    st.caption(f"by {track['artists'][0]['name']}")
                    
                    if track.get("preview_url"):
                        st.audio(track["preview_url"])
                    
                    if track.get("external_urls", {}).get("spotify"):
                        st.markdown(f"[Open on Spotify]({track['external_urls']['spotify']})")
                
                st.divider()

            if st.button("Save this playlist to my Spotify"):
                uris = [
                    f"spotify:track:{item['track']['id']}"
                    for item in ranked
                    if item["track"].get("id")
                ]

                playlist = sp_user.create_playlist(
                    name=f"MoodFlow — {mood.title()} {genre.title()}",
                    description="Generated by MoodFlow AI based on genre",
                    public=False
                )

                sp_user.add_tracks_to_playlist(
                    playlist_id=playlist["id"],
                    uris=uris
                )

                st.success("Playlist saved to your Spotify 🎉")
                st.markdown(
                    f"[Open playlist on Spotify]({playlist['external_urls']['spotify']})"
                )

    # ---------------------------
    # Albums
    # ---------------------------
    with tab3:
        st.markdown("### Recommended Albums")
        st.caption(f"Popular {genre} albums you might enjoy")
        
        # For artist-focused genres, show albums by curated artists
        if genre in ARTIST_FOCUSED_GENRES:
            seed_artists_for_albums = GENRE_SEED_ARTISTS.get(genre, [])[:4]
            all_genre_albums = []
            
            for artist_name in seed_artists_for_albums:
                try:
                    results = sp_public.sp.search(
                        q=f'artist:"{artist_name}"', 
                        type='album', 
                        limit=2
                    )
                    if results and 'albums' in results:
                        all_genre_albums.extend(results['albums']['items'])
                except:
                    continue
            
            # Display albums
            for album in all_genre_albums[:8]:
                if album:
                    col1, col2 = st.columns([1, 3])
                    
                    with col1:
                        if album.get('images'):
                            st.image(album['images'][0]['url'], width=120)
                    
                    with col2:
                        st.markdown(f"**{album['name']}**")
                        if album.get('artists'):
                            st.caption(f"by {album['artists'][0]['name']}")
                        
                        if album.get('release_date'):
                            st.caption(f"Released: {album['release_date']}")
                        
                        if album.get('total_tracks'):
                            st.caption(f"{album['total_tracks']} tracks")
                        
                        if album.get('external_urls', {}).get('spotify'):
                            st.markdown(f"[Open on Spotify]({album['external_urls']['spotify']})")
                    
                    st.divider()
        else:
            # Use standard method for other genres
            albums = sp_public.get_albums_from_genre(genre, limit=8)
            
            if not albums:
                st.info("No albums found for this genre.")
            else:
                for album in albums:
                    col1, col2 = st.columns([1, 3])
                    
                    with col1:
                        if album.get("image"):
                            st.image(album["image"], width=120)
                    
                    with col2:
                        st.markdown(f"**{album['name']}**")
                        st.caption(f"by {album['artist']}")
                        
                        if album.get("release_date"):
                            st.caption(f"Released: {album['release_date']}")
                        
                        if album.get("total_tracks"):
                            st.caption(f"{album['total_tracks']} tracks")
                        
                        if album.get("url"):
                            st.markdown(f"[Open on Spotify]({album['url']})")
                    
                    st.divider()


if __name__ == "__main__":
    main()