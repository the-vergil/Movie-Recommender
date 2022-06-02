from click import option
import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image

st.set_page_config(
   page_title="Movie Recommendation System",
   page_icon="",
   layout="wide",
   initial_sidebar_state="collapsed",
)

page = st.sidebar.selectbox("Recommend or Explore or Contacts", ("Recommend", "Explore", "Contacts"))

@st.cache
def get_data_for_indices() :
    data1 = pd.read_csv("final_data2.csv")
    return data1

@st.cache
def get_data_for_results() :
    data2 = pd.read_csv("final_data.csv")
    return data2

@st.cache(suppress_st_warning=True)
def get_viz_data() :
    data = pd.read_csv("dat_viz.csv")
    return data

@st.cache
def similarity() :
    cosine_sim = pickle.load(open("cosine_similarity.pkl", "rb"))
    return cosine_sim

def get_indices() :
    indices = pd.Series(data1['title'])
    return indices

## save movie titles in a list for select box
@st.cache(ttl=24*60*60)
def get_titles() :
    titles = list(data2["title"])
    return titles

## recommender function
@st.cache
def recommend(title):
    title = title.lower()
    recommended_movies_id = []
    idx = indices[indices == title].index[0]
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)
    top_10_indices = list(score_series.iloc[1:11].index)
    
    for i in top_10_indices:
        recommended_movies_id.append(list(data2['id'])[i])
    
    df = data2[data2["id"].isin(recommended_movies_id)]
    df = df[["title", "release_year", "imdb_link"]].reset_index(drop=True)
    df = df.set_index(pd.Index([1,2,3,4,5,6,7,8,9,10]))
    df.columns = ["Title", "Release Year", "IMDB Link"]
    
    return df 


#####
## Pages : Start
#####

### Recommendation page
if page=="Recommend" :
    st.title('Movie Recommendation System')

    ## run get_data_for_indices function
    data1 = get_data_for_indices()

    ## loading get_data_for_results function for results
    data2 = get_data_for_results()

    ## load cosine_similarity
    cosine_sim = similarity()

    ## load indices
    indices = get_indices()

    option = st.selectbox("Select a movie", get_titles())

    movie = st.write('You selected:', option)

    button = st.button("Recommend")
    if button :
        st.write(recommend(option))


### Explore page
if page=="Explore" :
    st.title("Exploring the dataset")
    st.header("The Movies Dataset")
    st.subheader("Acknowledgements :")
    st.write('''
            This dataset is an ensemble of data collected from TMDB and GroupLens.
            The Movie Details, Credits and Keywords have been collected from the TMDB Open API. 
            This product uses the TMDb API but is not endorsed or certified by TMDb. Their API also provides access to data on many additional movies, actors and actresses, crew members, and TV shows.

            The Movie Links and Ratings have been obtained from the Official GroupLens website.
            
            The dataset is downloaded from kaggle : https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset 
            This dataset only contains the data of movies released before 2017. ''')

    #####
    ##  Chart functions : Start
    #####

    data3 = get_viz_data()

    ## revenue chart function
    @st.cache(suppress_st_warning=True)
    def get_revenue_chart() :
        top_15_max_revenue_movies = data3["revenue"].nlargest(15)
        top_15_max_revenue_movies_indices = top_15_max_revenue_movies.index
        max_revenue_movies = data3.iloc[top_15_max_revenue_movies_indices]
        fig1 = px.bar(        
            max_revenue_movies,
            x = "title",
            y = "revenue",
            color = "revenue",
            labels=dict(title="Movie", revenue="Revenue")
        )
        fig1.update_layout(
                        autosize=False,
                        width=900,
                        height=500,)

        return fig1
    fig1 = get_revenue_chart()


    ## pie chart of adult movies
    @st.cache(suppress_st_warning=True)
    def get_adult_chart() :
        adult_counts = data3.adult.value_counts()
        adult_counts = pd.DataFrame(adult_counts).reset_index()
        adult_counts.columns = ["Adult", "Counts"]

        fig2 = go.Figure(
                        go.Pie(
                        labels = adult_counts.Adult,
                        values = adult_counts.Counts,
                        hoverinfo = "label+percent",
                        textinfo = "value"
                        )
                        )
        return fig2
    fig2 = get_adult_chart()
        

    ## bar chart of popularity :
    @st.cache(suppress_st_warning=True)
    def get_popularity_chart() :
        top_15_max_popularity_movies = data3["popularity"].nlargest(20)
        top_15_max_popularity_movies_indices = top_15_max_popularity_movies.index
        max_popularity_movies = data3.iloc[top_15_max_popularity_movies_indices]
        fig3 = px.bar(        
            max_popularity_movies,
            x = "title",
            y = "popularity",
            color = "popularity",
            labels=dict(title="Movie", popularity="Popularity")
        )
        fig3.update_layout(
                        autosize=False,
                        width=900,
                        height=500,)

        return fig3
    fig3 = get_popularity_chart()   


    ## line chart of language
    @st.cache(suppress_st_warning=True)
    def get_language_chart() :
        language_counts = pd.DataFrame(data3.original_language.value_counts())
        language_counts = language_counts.reset_index()
        language_counts.columns = ["language", "counts"]
        fig4 = px.line(        
            language_counts,
            x = "language",
            y = "counts",
            labels=dict(language="Language", counts="Language count of Movies")
        )

        fig4.update_traces(line_color = "maroon")
        fig4.update_layout(xaxis=dict(showgrid=False, gridwidth=0.5),
                yaxis=dict(gridwidth=0.3)
        )
        fig4.update_layout(
                        autosize=False,
                        width=900,
                        height=500,)
        return fig4
    fig4 = get_language_chart()


    ## word cloud of genres
    @st.cache(suppress_st_warning=True)
    def get_genre_chart() :
        image1 = Image.open('Images/07 - genres.png')
        return image1
    image1 = get_genre_chart()


    ## word cloud of keywords
    @st.cache(suppress_st_warning=True)
    def get_keywords_chart() :
        image2 = Image.open('Images/08 - keywords.png')
        return image2
    image2 = get_keywords_chart()

    ## bar chart of movie budget
    @st.cache(suppress_st_warning=True)
    def get_budget_chart() :
        top_15_max_budget_movies = data3["budget"].nlargest(15)
        top_15_max_budget_movies_indices = top_15_max_budget_movies.index
        max_budget_movies = data3.iloc[top_15_max_budget_movies_indices]
        fig5 = px.bar(        
            max_budget_movies,
            x = "title",
            y = "budget",
            color = "budget",
            labels=dict(title="Movie", budget="Budget")
        )
        fig5.update_layout(
                        autosize=False,
                        width=900,
                        height=500,)

        return fig5
    fig5 = get_budget_chart()

    #####
    ## Chart functions : End
    #####

    st.subheader("Let's start our exploration :")

    ## revenue chart of revenue
    st.header("Movies with maximum revenues")
    st.plotly_chart(fig1)

    ## pie chart of adult
    st.header("Adult Movies Count in the Dataset")
    st.plotly_chart(fig2)


    ## bar chart of popularity
    st.header("Most Popular Movies")
    st.plotly_chart(fig3)


    ## line chart of language
    st.header("Language counts of movies")
    st.plotly_chart(fig4)


    ## word cloud of genres
    st.header("Word Cloud of Genres")
    st.image(image1, width=900)


    ## bar chart of movie budget
    st.header("Maximum budget movies")
    st.plotly_chart(fig5)


    ## word cloud of keywords
    st.header("Word Cloud of most common keywords")
    st.image(image2, width=900)    


### Contacts page
if page=="Contacts" :
    st.header("Reach out to me via : ")
    st.subheader("Email : ")
    st.write(" chetmani1033@gmail.com ")

    st.subheader("Linkedin : ")
    st.write(" https://www.linkedin.com/in/chet-mani-singh-b27314205/ ")

    st.subheader("Github : ")
    st.write(" https://github.com/the-vergil/ ")


#####
## Pages : End
#####