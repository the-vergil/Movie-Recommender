# Movie-Recommender
- Movie Reecommendation System is a machine language project
- It uses natural language processing for the text text preprocessing of data
- It takes an input movie from the user and then it recommends ten similar movies to that movie basesd on cosine similarity rule

## Dataset
- This dataset is an ensemble of data collected from TMDB and GroupLens.
- The Movie Details, Credits and Keywords have been collected from the TMDB Open API. This product uses the TMDb API but is not endorsed or certified by TMDb. Their API also provides access to data on many additional movies, actors and actresses, crew members, and TV shows.
- The dataset only contains the data of movies before 2017
- The dataset is downloaded from kaggle : https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset

## App
- The movie-recommender app is deployed using streamlit and github
- The app consists of three pages:
  - Recommendation Page : This page is used for recommending movies
  - Explore Page : This page consists of some fancy user-interactive visualizations from the dataset
  - Contacts Page : This page contains the information of how to reach me

## Tools Used
- Google Colab : For cleaning, eda, visualizations and making rcommendation engine
- Streamlit : For the deployment of app
- Git : For pushing code to github

## Libraries Used
### Data Manipulation
1. Numpy
2. Pandas
### Data Visualization
1. Matplotlib
2. Plotly
### Text Preprocessing
1. NLTK
  - Tokenization
  - Stopwords
  - Stemming
### Text to Numerical data
1. Scikit-learn
  - CountVectorizer
  - Cosine Similarity
