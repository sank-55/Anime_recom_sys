import streamlit as st
import pandas as pd
import requests
import pickle
import html
import random
import urllib.parse

# Load model
with open('anime_recommender.pkl', 'rb') as f:
    model = pickle.load(f)

anime_df = model['anime']
cosine_sim = model['cosine_sim']
anime_indices = model['anime_indices']
anime_df['name'] = anime_df['name'].apply(lambda x: html.unescape(x) if isinstance(x, str) else x)

# Custom styles
def apply_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Quicksand', sans-serif;
    }
    .genre-pill {
        display: inline-block;
        background: linear-gradient(to right, #4f46e5, #9333ea);
        color: white;
        padding: 3px 12px;
        margin: 3px 5px 3px 0;
        font-size: 12px;
        border-radius: 999px;
    }
    .anime-card {
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 30px;
        box-shadow: 0 0 12px rgba(0,0,0,0.4);
        transition: 0.3s ease;
    }
    .anime-card:hover {
        box-shadow: 0 0 20px rgba(253, 216, 53, 0.4);
        transform: scale(1.02);
    }
    .anime-title {
        font-size: 24px;
        font-weight: bold;
        color: #fdd835;
        margin: 10px 0;
    }
    .anime-meta {
        font-size: 14px;
        font-style: italic;
        color: #ccc;
    }
    .rating-bar {
        height: 8px;
        border-radius: 4px;
        background: linear-gradient(to right, #facc15 calc(var(--rating) * 10%), #444 calc(var(--rating) * 10%));
        margin-bottom: 15px;
    }
    .trailer-link {
        font-size: 14px;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Fetch poster
def fetch_image(anime_id):
    try:
        res = requests.get(f"https://api.jikan.moe/v4/anime/{anime_id}", timeout=5)
        return res.json()['data']['images']['jpg']['image_url']
    except:
        return "https://via.placeholder.com/300x450.png?text=Image+Unavailable"

# Fetch overview
def fetch_overview(title):
    query = '''
    query ($search: String) {
      Media(search: $search, type: ANIME) {
        description(asHtml: false)
      }
    }'''
    try:
        res = requests.post('https://graphql.anilist.co', json={'query': query, 'variables': {'search': title}})
        return res.json()['data']['Media']['description']
    except:
        return "Overview not available."

# Generate YouTube search link
def get_trailer_link(title):
    query = urllib.parse.quote(f"{title} anime trailer")
    return f"https://www.youtube.com/results?search_query={query}"

# Recommend logic
def recommend_anime(title):
    if title not in anime_indices:
        return [], [], [], [], [], []
    idx = anime_indices[title]
    scores = sorted(list(enumerate(cosine_sim[idx])), key=lambda x: x[1], reverse=True)[1:6]
    names, posters, genres, ratings, overviews, trailers = [], [], [], [], [], []
    for i in scores:
        row = anime_df.iloc[i[0]]
        name = row['name']
        names.append(name)
        posters.append(fetch_image(row['anime_id']))
        genres.append(row['genre'])
        ratings.append(row['rating'])
        overviews.append(fetch_overview(name))
        trailers.append(get_trailer_link(name))
    return names, posters, genres, ratings, overviews, trailers

# Smart surprise
def smart_surprise(df):
    top_df = df[df['rating'] >= df['rating'].quantile(0.95)]
    return random.choice(top_df['name'].tolist()) if not top_df.empty else random.choice(df['name'].tolist())

# Filter logic
def filter_anime(df, genre, type_, rating):
    df_filt = df.copy()
    if genre != "All":
        df_filt = df_filt[df_filt['genre'].str.contains(genre)]
    if type_ != "All":
        df_filt = df_filt[df_filt['type'] == type_]
    return df_filt[df_filt['rating'] >= rating]

# App layout
st.set_page_config(page_title="Smart Anime Recommender", layout="wide")
apply_styles()

# Sidebar
st.sidebar.title("🎌 Anime Filters")
genre = st.sidebar.selectbox("Genre", ["All"] + sorted({g for gset in anime_df['genre'].dropna() for g in gset.split(', ')}))
type_ = st.sidebar.selectbox("Type", ["All"] + sorted(anime_df['type'].dropna().unique()))
min_rating = st.sidebar.slider("Min Rating", 1.0, 10.0, 7.5)

filtered_df = filter_anime(anime_df, genre, type_, min_rating)
selected_anime = st.sidebar.selectbox("🎥 Pick an Anime", filtered_df['name'].tolist())
col1, col2 = st.sidebar.columns(2)
recommend = col1.button("🎯 Recommend")
surprise = col2.button("🎲 Surprise Me")

# Title
st.markdown("<h1 style='color:white; text-align:center;'>🌌 Smart Anime Recommender</h1>", unsafe_allow_html=True)

# Trigger
if surprise:
    surprise_title = smart_surprise(filtered_df)
    st.toast(f"🎲 Surprise Pick: {surprise_title}")
    results = recommend_anime(surprise_title)
elif recommend:
    results = recommend_anime(selected_anime)
else:
    results = None

# Display
if results:
    names, posters, genres, ratings, overviews, trailers = results
    for i in range(len(names)):
        genre_tags = ''.join(f"<span class='genre-pill'>{g}</span>" for g in genres[i].split(', '))
        st.markdown("<div class='anime-card'>", unsafe_allow_html=True)
        st.image(posters[i], width=200)
        st.markdown(f"<div class='anime-title'>{names[i]}</div>", unsafe_allow_html=True)
        st.markdown(genre_tags, unsafe_allow_html=True)
        st.markdown(f"<div class='anime-meta'>⭐ Rating: {ratings[i]}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='rating-bar' style='--rating: {float(ratings[i])/10};'></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='anime-overview'>{overviews[i]}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='trailer-link'><a href='{trailers[i]}' target='_blank'>▶ Watch Trailer on YouTube</a></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
