from dotenv import load_dotenv
import streamlit as st
import requests
from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os

load_dotenv()

category  = [
    'business',
    'entertainment',
    'general',
    'health',
    'science',
    'sports',
    'technology'
]

malayalam_dialogues = [
    "Nee po mone Dinesha",  # From the movie 'Narasimham'
    "Thallipogathey! Baaki ullathu venel njan parayam." , # From the movie 'Premam'
    "Mothiravadi, aa rajakumariyude sthaanathil njaan annu nilkunnu." , # From the movie 'Ustad Hotel'
    "Ormayundo ee mukham?" , # From the movie 'Nadodikattu'
    "Pavada veedu pavada vachal kazhuthakal veenu" ,
    "Eda Mwone" # From the movie 'Kireedam'
]
domain = [
    "Movies",
    "News"
]
selected_headline = ""

# Fetch the API key from the .env file
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# Streamlit UI
st.title("Trend Based Ad Content Generator")
st.write("Select a domain to generate ad content for your restaurant:")

selectedDomain= st.selectbox("Select Domain", domain)

if selectedDomain == "Movies":
    selectedDialogue = st.selectbox("Movie Dialogue", malayalam_dialogues)
elif selectedDomain == "News":
    selectedCategory = st.selectbox("News Category", category)

# Function to fetch trending news

    def fetch_trending_news(api_key, country='in', page_size=8, category=selectedCategory):
        url = 'https://newsapi.org/v2/top-headlines'
        params = {
            'apiKey': api_key,
            'country': country,
            'pageSize': page_size,
            'category': category
        }
        response = requests.get(url, params=params)
        return response.json()


    news_data = fetch_trending_news(NEWS_API_KEY)
    headlines = [article['title'] for article in news_data['articles']]
    selected_headline = headlines[4]




#selected_headline = st.selectbox("News Headlines", headlines)





if st.button("Generate Ad Content"):
    # Set up prompt and model for ad content generation
    if selectedDomain == "Movies":
        prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", "You are an expert ad content writer. Generate creative and engaging ad content for my restaurant based on the malayalam movie dialogue provided, taking into account the sentiment of the dialogue."),
                    ("user", "Movie Dialogue: {dialogue}")
                ]
            )
        groqApi = ChatGroq(model="llama3-70b-8192", temperature=0, api_key=GROQ_API_KEY)
        outputparser = StrOutputParser()
        chainSec = prompt | groqApi | outputparser
            
            # Generate ad content
        response = chainSec.invoke({'dialogue': selectedDialogue})
            
        st.write("Generated Ad Content:")
        st.write(response)

    elif selectedDomain == "News":
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are an expert ad content writer. Generate creative and engaging ad content for my restaurant based on the news headline provided, taking into account the sentiment of the article."),
                ("user", "News Headline: {headline}")
            ]
        )
        
        groqApi = ChatGroq(model="llama3-70b-8192", temperature=0, api_key=GROQ_API_KEY)
        outputparser = StrOutputParser()
        chainSec = prompt | groqApi | outputparser
        
        # Generate ad content
        response = chainSec.invoke({'headline': selected_headline})
        
        st.write("Generated Ad Content:")
        st.write(response)
