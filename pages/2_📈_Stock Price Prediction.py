import pandas as pd
import os
import yfinance as yf
import streamlit as st
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np
import base64

st.set_page_config("📈 Stock Price Prediction")

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
background-size: 1000%;
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


# Add some CSS to customize the appearance
#st.set_page_config(page_title="Stock Price Prediction",page_icon="📈")

st.markdown("""
    <style>
      .main {
            background-color: #f0f0f0;
        }
      
        }
      .stButton:hover {
            background-color: #3e8e41;
        }
      .stTable {
            font-size: 12px;
            border-collapse: collapse;
            width: 100%;
        }
      .stTable th,.stTable td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
      .stTable th {
            background-color: #f0f0f0;
        }
      .stTable tr:nth-child(even) {
            background-color: #f2f2f2;
        }
      .stTable tr:hover {
            background-color: #ddd;
        }
    </style>
""", unsafe_allow_html=True)

# Add Streamlit code here
st.title("Stock Price Prediction")
st.header("Enter Stock Details")

ticker = st.text_input("Enter Stock Name: ")
start_date = "2010-07-19"

if st.button("Get Data"):
    if ticker == "":
        st.write("Please enter a stock name.")
    else:
        data = yf.download(ticker, start=start_date)
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df.index)

        st.subheader("Stock Information")
        st.write(f"Stock : {ticker}")
        st.write(f"Current Price: {df['Close'].iloc[-1]:.2f}")
        st.write(f"High Price: {df['High'].max():.2f}")
        st.write(f"Low Price: {df['Low'].min():.2f}")
        st.subheader(f"Data Set : {ticker} ")
        st.write(df.head())
        st.subheader(f"Tail of {ticker}")
        st.write(df.tail())
        st.subheader("Candlestick Chart")
        fig = go.Figure(data=[go.Candlestick(x=df['date'],
                                         open=df['Open'],
                                         high=df['High'],
                                         low=df['Low'],
                                         close=df['Close'])])
        fig.update_layout(title=ticker,yaxis_title='Price (₹)',xaxis_rangeslider_visible=False)
        st.plotly_chart(fig)
        
        st.subheader(f"Volume of {ticker}")
        fig3 = go.Figure(data=[go.Line(x=df.index, y=df['Volume'])])
        fig3.update_layout(title=f"Volume of {ticker}",yaxis_title='Volume',xaxis_title="Year")
        st.plotly_chart(fig3)

        df.drop(['date','Volume'], axis=1, inplace = True)
        df.reset_index(drop=True, inplace= True)

        X = df[['Open','Close','High','Low','Adj Close']]
        y = df['Close']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=52)

        rf = RandomForestRegressor(n_estimators=100, random_state=42)
        rf.fit(X_train, y_train)

        y_pred = rf.predict(X_test)

        # Add a line chart of closing prices
        st.subheader("Closing Prices Over Time")
        fig2 = go.Figure(data=[go.Line(x=df.index, y=df['Close'])])
        fig2.update_layout(title=f"Closing Prices of {ticker}",yaxis_title='Price (₹)')
        st.plotly_chart(fig2)

        mse = mean_squared_error(y_test,y_pred)
        st.subheader(f"Mean Squared Error")
        st.write(f"Mean Squared Error : {mse}")

        new_data = np.array([df.iloc[-1]])
        predicted_price = rf.predict(new_data)
        st.subheader("Predicted Stock Price")
        st.write(f"Predicted Stock Price : {predicted_price[0]}")