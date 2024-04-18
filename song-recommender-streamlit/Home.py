from helpers import recommend_song
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

# Getting the client_id and client_secret variables created earlier using cmd
c_id = os.getenv('SPOTIFY_CLIENT_ID')
c_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

#Initialize SpotiPy with user credentias
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=c_id,
                                                           client_secret=c_secret))

st.title(":green[Spotify Song Recommender]")
st.write("---")
col1, col2 = st.columns([.5, .5])

st.write("---")

song = col1.text_input('Song')
artist = col2.text_input('Artist')

st.header("Press enter to get your recommended song")

if artist and song:
    song_recommended = recommend_song(song, artist)
else:
    st.stop()
st.header(song_recommended, divider='rainbow')