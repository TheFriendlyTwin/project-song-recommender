import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Get the tracks df
tracks_df = pd.read_csv("song-recommender-streamlit/data/tracks.csv")

# Calculate the number of songs per genre
genre_counts = tracks_df['artist_genre'].value_counts().reset_index()

genre_counts.columns = ['artist_genre', 'count']

# Limit the DataFrame to the first 30 genres
top_genres = genre_counts.head(30)

# Setting the color palette to a palette that includes green
sns.set_palette('Greens')

# Plotting
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [1, 4, 9])
sns.barplot(x='artist_genre', y='count', data=top_genres, ax=ax)
ax.set_title('Top 30 Music Genres by Song Count', pad=20)
ax.set_xlabel('Music Genre', labelpad=5)
ax.set_ylabel('Number of Songs', labelpad=5)
plt.xticks(rotation=90)  # Rotate the genre labels for better readability

# Display the plot in a Streamlit app
st.pyplot(fig)