import streamlit as st

def card_title(title: str, subtitle: str | None = None):
    st.markdown(f"### {title}")
    if subtitle:
        st.caption(subtitle)

def render_track(t: dict):
    title = t.get("title", "Unknown Track")
    artist = t.get("artist", "Unknown Artist")
    url = t.get("url")
    preview = t.get("preview")
    cover = t.get("cover")

    if url:
        st.markdown(f"**[{title}]({url})** — {artist}")
    else:
        st.markdown(f"**{title}** — {artist}")

    if preview:
        st.audio(preview)

    if cover:
        st.image(cover, width=160)


def render_artist(a: dict):
    name = a.get("name", "Unknown Artist")
    url = a.get("url")
    image = a.get("image")

    if url:
        st.markdown(f"**[{name}]({url})**")
    else:
        st.markdown(f"**{name}**")

    if image:
        st.image(image, width=120)

