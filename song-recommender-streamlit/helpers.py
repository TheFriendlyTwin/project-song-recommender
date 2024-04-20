import pandas as pd
import spotipy
import pickle
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from spotipy.oauth2 import SpotifyClientCredentials
from sklearn.metrics import pairwise_distances_argmin_min

# Get scaled df
scaled_df = pd.read_csv("song-recommender-streamlit/data/scaled_tracks.csv")

with open("song-recommender-streamlit/data/scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

with open("song-recommender-streamlit/data/kmeans.pkl", "rb") as f:
    kmeans = pickle.load(f)


# Function that recommends a song with similar music features 
def recommend_song(sp, song, artist):
    cols = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
    
    try: 
        # get song id
        results = sp.search(q=f'track:{song} - {artist}', limit=1)
        
        # Ensure there are results before proceeding
        if results['tracks']['items']:
            track_id = results['tracks']['items'][0]['id']
            chosen_song_name = results['tracks']['items'][0]['name']  # Store chosen song's name
            chosen_artist_name = results['tracks']['items'][0]['artists'][0]['name']  # Store chosen artist's name
            
             # get song features with the obtained id
            audio_features = sp.audio_features(track_id)

            # create dataframe
            df_ = pd.DataFrame(audio_features)
            new_features = df_[cols]

            # scale features
            scaled_x = scaler.transform(new_features)

            # predict cluster
            cluster = kmeans.predict(scaled_x)

            # filter dataset to predicted cluster
            filtered_df = scaled_df[scaled_df['cluster'] == cluster[0]]

            # Add a filter to exclude the chosen song
            filtered_df = filtered_df[~((filtered_df['song name'].str.lower() == chosen_song_name.lower()) &
                                        (filtered_df['artist'].str.lower() == chosen_artist_name.lower()))]

            filtered_array = np.array(filtered_df[cols], order="C")

            # get closest song from filtered dataset
            closest, _ = pairwise_distances_argmin_min(scaled_x, filtered_array)
            
            # return it in a readable way
            print('\n[RECOMMENDED SONG]')
            recommended_song = filtered_df.iloc[closest[0]]  # Accessing the first closest match
            return ' - '.join([recommended_song['song name'], recommended_song['artist']])
            
        else:
            return 'No results found for the specified song. Please try again with a different song.'

    except IndexError as e:
        return f"An error occurred: {e}"
    


