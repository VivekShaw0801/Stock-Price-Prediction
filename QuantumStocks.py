import base64
import streamlit as st
#import plotly.express as px

st.set_page_config("Quantam Stocks")

@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


img = get_img_as_base64("image.jpg")

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://png.pngtree.com/thumb_back/fh260/background/20230408/pngtree-rainbow-curves-abstract-colorful-background-image_2164067.jpg");
background-size: 600%;
background-position: top left;
background-repeat: no-repeat;
background-attachment: local;
}}

[data-testid="stSidebar"] > div:first-child {{
background-image: url("data:image/png;base64,{img}");
background-position: center; 
background-repeat: no-repeat;
background-attachment: fixed;
}}

[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}

[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

st.header("Welcome to QuantumStocks")
st.subheader("Understanding Stock Price Prediction")
st.write("I.Stock markets are dynamic and influenced by various factors such as economic indicators, company performance, and investor sentiment.")
st.write("II.Predicting future stock prices is essential for investors, traders, and financial institutions to make informed decisions and manage risks effectively.")
st.subheader("Random Forest Regression (RFR)")
st.write("I. Random Forest Regression, a machine learning technique that uses multiple decision trees to predict numerical values. It's effective for regression tasks where the goal is to predict continuous outcomes.")
st.write("II. In Random Forest Regression (RFR), the model consists of a collection of decision trees, where each tree is built on a random subset of the training data and a random subset of features.")
st.write("III. During training, each decision tree is constructed independently, and the final prediction is the average (or median) of the predictions made by all the individual trees.")
