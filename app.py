import json
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta, timezone
import pytz
import re
import nltk
nltk.download('stopwords')
from wordcloud import WordCloud, STOPWORDS
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import time


st.set_page_config(
        page_title="Twitch Dashboard",
        page_icon="👾👾",
        layout="centered",
    )

def run_app():
    def process_time(x):
        try:
            return re.findall(r'\d+',x)[0]
        except:
            return None

    with st.empty():
        while True:

            #@st.cache(show_spinner=False)
            def load_datasets():
                with open('load_messages/messages_all.json', "r") as file:
                    data = json.load(file)
                df = pd.DataFrame(data)
                df['date'] = pd.to_datetime(df['tmi-sent-ts'].map(lambda x: process_time(x)).astype(float), unit='ms')
                local = pytz.timezone("America/Argentina/Buenos_Aires")
                local_dt = local.localize(datetime.now(), is_dst=None)
                utc_dt = local_dt.astimezone(pytz.utc)
                #df_vol = df[df['date'] > (utc_dt - timedelta(minutes=5)).replace(tzinfo=None)]
                #return df_vol
                return df


            df_vol = load_datasets()


            comment_words = ''

            # iterate through the csv file
            for val in df_vol.msg:

                # typecaste each val to string
                val = str(val)

                # split the value
                tokens = val.split()

                # Converts each token into lowercase
                for i in range(len(tokens)):
                    tokens[i] = tokens[i].lower()

                comment_words += " ".join(tokens)+" "

            wordcloud = WordCloud(width = 800, height = 800,
                            background_color ='white',
                            stopwords = stopwords.words('spanish'),
                            min_font_size = 10).generate(comment_words)

            # dashboard title
            st.title("Real-Time / Live Data Science Dashboard")
            st.markdown("### First Chart")
            plt.figure(figsize = (5, 5), facecolor = None)
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            plt.show()
            st.pyplot()
            time.sleep(5)

run_app()

