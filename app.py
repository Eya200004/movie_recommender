import streamlit as st
from recommender import recommend_advanced, movies

st.set_page_config(
    page_title="Recommandation de Films",
    page_icon="🎬",
    layout="wide"
)

st.markdown("""
<style>

/* Background dégradé */
.stApp {
    background: linear-gradient(135deg, #1d1d1d, #2c2c2c);
    color: white;
}

/* Labels des champs */
.css-1p3g8cg, label, .stSelectbox label, .stTextInput label {
    color: #f5c518 !important; /* Jaune IMDb */
    font-weight: 600;
}

/* Text input + select + slider narration */
input, select, textarea {
    background-color: #3a3a3a !important;
    color: white !important;
    border: 1px solid #555 !important;
    border-radius: 10px !important;
    padding: 8px !important;
}

/* Forces slider text and other tooltip text to white */
div[data-baseweb="slider"] * {
    color: white !important;
}

/* Cards */
.card {
    background-color:#222;
    padding:15px;
    margin:10px;
    border-radius:15px;
    box-shadow:0 0 10px rgba(255,255,255,0.1);
}

h1, h2, h3 {
    color: #f5c518 !important;
}

</style>
""", unsafe_allow_html=True)

# --- TITRE ---
st.markdown("<h1 style='text-align:center;'>🎬 Film Recommender Pro</h1>", unsafe_allow_html=True)
st.write("<p style='text-align:center; font-size:18px;'>Un système intelligent de recommandation multi-critères.</p>", unsafe_allow_html=True)

st.markdown("---")

# --- COLONNES ---
col1, col2, col3 = st.columns(3)

with col1:
    genre = st.text_input(" Genre (ex: Action, Comedy, Drama)")
    year = st.text_input("Année (ex: 1995)")

with col2:
    title_contains = st.text_input(" Contient dans le titre")
    min_rating = st.slider("⭐ Note minimale", 0.0, 5.0, 2.5)

with col3:
    similar_to = st.selectbox(
        "Similaire à un film",
        options=[""] + sorted(movies["title"].unique().tolist())
    )

st.markdown(" ")
center = st.columns(3)
with center[1]:
    run = st.button(" Recommander", use_container_width=True)

if run:
    st.markdown("---")
    st.markdown("<h2> Films recommandés :</h2>", unsafe_allow_html=True)

    recommendations = recommend_advanced(
        genre=genre or None,
        year=year or None,
        title_contains=title_contains or None,
        min_rating=min_rating,
        similar_to=similar_to or None,
        n=12
    )

    if not recommendations:
        st.error("❌ Aucun film trouvé...")
    else:
        cols = st.columns(3)

        for i, film in enumerate(recommendations):
            with cols[i % 3]:
                st.markdown(
                    f"""
                    <div class="card">
                        <h4 style="color:#f5c518;">🎬 {film}</h4>
                        <p style="opacity:0.8;">Recommandé selon vos critères</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
