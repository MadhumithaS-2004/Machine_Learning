import streamlit as st
import pickle
import requests

# Load data
movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))

# OMDb API key
OMDB_API_KEY = "6377f162"

# Poster fetch function
def fetch_poster(movie_title):
    try:
        url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
        response = requests.get(url)
        data = response.json()
        if data.get("Response") == "True":
            return data.get("Poster", "https://via.placeholder.com/300x450?text=No+Image")
        else:
            return "https://via.placeholder.com/300x450?text=Not+Found"
    except Exception as e:
        return "https://via.placeholder.com/300x450?text=Error"

# Recommend function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_titles = []
    recommended_posters = []
    for i in distances[1:16]:  # Top 15 movies
        movie_title = movies.iloc[i[0]].title
        recommended_titles.append(movie_title)
        recommended_posters.append(fetch_poster(movie_title))
    return recommended_titles, recommended_posters

# UI
st.header("🎬 Movie Recommender System")
movie_list = movies['title'].values
selected_movie = st.selectbox("Select a movie", movie_list)

# Session state to store current page
if 'page' not in st.session_state:
    st.session_state.page = 0

# Buttons for pagination
col1, col2, col3 = st.columns([1, 6, 1])
with col1:
    if st.button("⬅️ Previous"):
        st.session_state.page = max(st.session_state.page - 1, 0)

with col3:
    if st.button("Next ➡️"):
        st.session_state.page += 1

# Show recommendations
if st.button("Show Recommend"):
    st.session_state.page = 0  # reset to first page
    st.session_state.names, st.session_state.posters = recommend(selected_movie)

# Display current page
if 'names' in st.session_state:
    start = st.session_state.page * 5
    end = start + 5
    cols = st.columns(5)
    for i, col in enumerate(cols):
        if start + i < len(st.session_state.names):
            with col:
                st.image(st.session_state.posters[start + i])
                st.text(st.session_state.names[start + i])



