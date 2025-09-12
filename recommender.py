import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies = pd.read_csv("movies.csv")
ratings = pd.read_csv("ratings.csv")

movies["genres"] = movies["genres"].fillna("")

mean_ratings = ratings.groupby("movieId")["rating"].mean()
movies = movies.merge(mean_ratings, on="movieId", how="left")
movies["rating"] = movies["rating"].fillna(0)

tfidf = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf.fit_transform(movies["genres"])

cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

indices = pd.Series(movies.index, index=movies["title"]).drop_duplicates()

#fonctions de recommandation
def recommend_advanced(genre=None, year=None, title_contains=None, min_rating=0, n=10, similar_to=None):
    filtered = movies.copy()

    if genre:
        filtered = filtered[filtered["genres"].str.lower().str.contains(genre.lower())]

    if year:
        filtered = filtered[filtered["title"].str.contains(str(year))]

    if title_contains:
        filtered = filtered[filtered["title"].str.lower().str.contains(title_contains.lower())]

    filtered = filtered[filtered["rating"] >= min_rating]
    
    if similar_to:
        if similar_to not in indices:
            print(f"❌ Le film '{similar_to}' n'existe pas dans la base.")
        else:
            idx = indices[similar_to]
            sim_scores = list(enumerate(cosine_sim[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:]  
            sim_indices = [i[0] for i in sim_scores]
            similar_movies = movies.iloc[sim_indices]
            filtered = pd.merge(filtered, similar_movies, how="inner", on=movies.columns[0])

    if filtered.empty:
        return "❌ Aucun film trouvé avec ces critères."

    return filtered.sample(min(n, len(filtered)))["title"].tolist()


#l’utilisateur
print("🎬 Movie Recommender Avancé 🎬")
print("Vous pouvez combiner plusieurs critères pour obtenir des recommandations :\n")

genre = input("Genre (Action, Comedy, Drama…) : ")
année = input("Année de sortie (ex: 1995) : ")
titre = input("Contient le mot dans le titre (ex: Star) : ")
min_rating = input("Note minimale (0-5) : ")
similaire = input("Similaire à un film (ou rien) : ")

min_rating = float(min_rating) if min_rating else 0

results = recommend_advanced(
    genre=genre,
    year=année,
    title_contains=titre,
    min_rating=min_rating,
    n=10,
    similar_to=similaire if similaire else None
)

print("\n👉 Films recommandés :")
print(results)
