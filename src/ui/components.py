import streamlit as st

def card_title(title: str, subtitle: str | None = None):
    st.markdown(f"### {title}")
    if subtitle:
        st.caption(subtitle)

def render_artist(a: dict):
    st.markdown(f"**[{a['name']}]({a['url']})**")
    if a.get("image"):
        st.image(a["image"], width=120)
    if a.get("genres"):
        st.caption("Genres: " + ", ".join(a["genres"][:4]))

def render_track(t: dict):
    st.markdown(f"**[{t['title']}]({t['url']})** — {t['artist']}")
    if t.get("cover"):
        st.image(t["cover"], width=160)
    if t.get("preview"):
        st.audio(t["preview"])
