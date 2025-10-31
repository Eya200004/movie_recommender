import streamlit as st
from recommender import recommend_advanced, movies

st.set_page_config(page_title="Recommandation de Films", page_icon="🎬", layout="wide")

st.title("🎬 Film Recommender")
st.write("Utilise un ou plusieurs critères pour obtenir des recommandations personnalisées :")

# --- FORMULAIRE ---
genre = st.text_input("🎭 Genre (ex: Action, Comedy, Drama)")
year = st.text_input("📅 Année (ex: 1995)")
title_contains = st.text_input("🔍 Contient dans le titre")
min_rating = st.slider("⭐ Note minimale", 0.0, 5.0, 0.0)
similar_to = st.selectbox(
    "🎞️ Similaire à un film",
    options=[""] + sorted(movies["title"].unique().tolist())
)

# --- BOUTON ---
if st.button("🔎 Recommander"):
    recommendations = recommend_advanced(
        genre=genre if genre else None,
        year=year if year else None,
        title_contains=title_contains if title_contains else None,
        min_rating=min_rating,
        similar_to=similar_to if similar_to != "" else None,
        n=10
    )

    st.subheader("🎥 Résultats :")

    if not recommendations:
        st.error("Aucun film trouvé..")
    else:
        for film in recommendations:
            st.write("✅", film)
