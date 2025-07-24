import streamlit as st
import pandas as pd
import joblib
import numpy as np

st.set_page_config(page_title="Music Recommender", page_icon="🎵")


@st.cache_resource
def load_all():
    try:
        df = pd.read_csv("spotify_clustered.csv")
        df['popularity'] = pd.to_numeric(df['popularity'], errors='coerce').fillna(0)
        model = joblib.load("nn_model.joblib")
        features = np.array(df['pca_features'].apply(lambda x: eval(x) if isinstance(x, str) else x).tolist())
        return df, model, features
    except FileNotFoundError:
        return None, None, None


df, nn_model, features = load_all()

st.title("Music Recommendation System 🎶")

if df is None or nn_model is None:
    st.error("ERROR: Make sure 'spotify_clustered.csv' and 'nn_model.joblib' are in the same folder.")
else:
    st.sidebar.header("Options")
    model_choice = st.sidebar.radio(
        "Choose a recommendation algorithm:",
        ('K-Nearest Neighbors', 'K-Means')
    )

    song_list = sorted(df['name'].dropna().unique())
    selected_song = st.selectbox("Choose a song you like:", options=song_list)

    num_recs_to_show = st.sidebar.slider(
        "Number of recommendations:", min_value=3, max_value=15, value=5, step=1
    )


    def get_knn_recommendations(song_name, dataframe, model, feature_matrix, num_recs):
        try:
            song_index = dataframe[dataframe['name'] == song_name].index[0]
            song_features = feature_matrix[song_index].reshape(1, -1)

            distances, indices = model.kneighbors(song_features)

            neighbor_indices = indices.flatten()[1:]

            return dataframe.iloc[neighbor_indices].sample(n=num_recs)
        except (IndexError, KeyError):
            return None


    def get_kmeans_recommendations(song_name, dataframe, num_recs):
        try:
            song_row = dataframe[dataframe['name'] == song_name].iloc[0]
            cluster_id = song_row['cluster']

            pool = dataframe[(dataframe['cluster'] == cluster_id) & (dataframe['name'] != song_name)]
            if pool.empty: return None

            weights = pool['popularity'].clip(lower=0).fillna(0) + 1
            return pool.sample(n=min(num_recs, len(pool)), weights=weights)
        except (IndexError, KeyError):
            return None


    if st.button("Find Recommendations"):
        recommendations = None
        if model_choice == 'K-Nearest Neighbors':
            st.write("Using KNN for recommendations...")
            recommendations = get_knn_recommendations(selected_song, df, nn_model, features, num_recs_to_show)
        else:
            st.write("Using K-Means for recommendations...")
            recommendations = get_kmeans_recommendations(selected_song, df, num_recs_to_show)

        if recommendations is not None and not recommendations.empty:
            st.dataframe(recommendations[['name', 'artists', 'year']])
        else:
            st.warning("Sorry, we couldn't find any recommendations.")