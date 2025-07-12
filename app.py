import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(
    page_title="Recommandation de Musique",
    page_icon="🎵",
    layout="centered"
)

@st.cache_data
def load_data():
    df = pd.read_parquet("spotify_data_features.parquet")
    return df

df = load_data()

st.title("Système de Recommandation de Musique 🎶")
st.write("Cliquez sur le bouton pour découvrir de nouvelles recommandations à chaque fois !")

song_list = df['name'].unique()
selected_song = st.selectbox(
    "Choisissez une chanson que vous aimez :",
    options=song_list
)

def get_randomized_recommendations(song_name, dataframe, pool_size=20, num_recs=5):
    try:
        song_row = dataframe[dataframe['name'] == song_name].iloc[0]
    except IndexError:
        return None
        
    cluster_id = song_row['prediction']
    song_features = [song_row['pca_features']]

    cluster_df = dataframe[
        (dataframe['prediction'] == cluster_id) & (dataframe['name'] != song_name)
    ].copy()

    features_list = cluster_df['pca_features'].tolist()
    similarities = cosine_similarity(song_features, features_list)[0]

    cluster_df['similarity'] = similarities
    
    top_similar_songs = cluster_df.sort_values(by='similarity', ascending=False).head(pool_size)
    
    num_to_sample = min(num_recs, len(top_similar_songs))
    
    return top_similar_songs.sample(n=num_to_sample)

if st.button("Trouver des recommandations"):
    if selected_song:
        
        recommendations = get_randomized_recommendations(selected_song, df)
        
        if recommendations is not None and not recommendations.empty:
            st.write(f"Parce que vous avez aimé **{selected_song}**, voici quelques suggestions :")
            st.dataframe(recommendations[['name', 'artists', 'popularity']])
        else:
            st.warning("Désolé, nous n'avons pas pu trouver de recommandations pour cette chanson.")