import pickle
import streamlit as st

# ---------------- LOAD DATA ----------------
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
import requests
import pickle
import os

url = "https://drive.google.com/uc?export=download&id=1KWpOQzeOpX6ZP-zNjFWQ4XFBQWK_cZZW"

if not os.path.exists("similarity.pkl"):
    r = requests.get(url)
    with open("similarity.pkl", "wb") as f:
        f.write(r.content)

similarity = pickle.load(open("similarity.pkl", "rb"))
# ---------------- IMAGE FUNCTION ----------------
def get_image(movie_name):
    return f"https://via.placeholder.com/300x450?text={movie_name.replace(' ', '+')}"

# ---------------- RECOMMEND FUNCTION ----------------
def recommend(movie):
    if movie not in movies['title'].values:
        return [], []

    index = movies[movies['title'] == movie].index[0]
    distances = sorted(enumerate(similarity[index]), key=lambda x: x[1], reverse=True)

    names = []
    images = []

    for i in distances[1:6]:
        movie_title = movies.iloc[i[0]].title
        names.append(movie_title)
        images.append(get_image(movie_title))

    return names, images

# ---------------- UI ----------------
st.set_page_config(page_title="Movie Recommender", layout="wide")

st.title("🎬 Movie Recommender System")

movie_list = movies['title'].values

selected_movie = st.selectbox(
    "Select a movie",
    movie_list
)

# ---------------- BUTTON ----------------
if st.button("Recommend"):
    with st.spinner("Finding similar movies..."):
        names, images = recommend(selected_movie)

    if names:
        cols = st.columns(5)

        for i in range(5):
            with cols[i]:
                st.text(names[i])
                st.image(images[i])
    else:
        st.error("Movie not found!")
