import streamlit as st
import sqlite3
import pandas as pd
import base64
#import plotly.express as px

st.set_page_config("👨🏻‍💼 Admin")

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
background-size: 500%;
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




# Set up the database connection


st.subheader("Welcome to Admin Login Page")
st.write("Please enter your credentials to login as a Admin.")
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create the contact messages table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS contact_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        message TEXT NOT NULL
    )
''')

# Set up the login form
def login_form():
    user_id = 'vivekshaw476@gmail.com'
    password = '82Gf6790@'
    entered_user_id = st.text_input('User ID')
    entered_password = st.text_input('Password', type='password')
    if st.button('Login'):
        if entered_user_id == user_id and entered_password == password:
            st.success('Logged in successfully')
            return True
        else:
            st.error('Invalid user ID or password')
            return False
    return False

# Display the login form
if not login_form():
    st.stop()

# Add some CSS to customize the appearance
st.markdown("""
    <style>
   .main {
            background-color: #f0f0f0;
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
            font-family: Arial, sans-serif; /* Add this line to change the font */
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

# Display the contact messages
st.title('Contact Messages')

# Fetch the contact messages from the database
cursor.execute('SELECT * FROM contacts')
messages = cursor.fetchall()

# Convert the messages to a Pandas DataFrame
df = pd.DataFrame(messages, columns=['S.No.', 'Name', 'Email', 'Message'])

# Set the 'S.No.' column as the index
df.set_index('S.No.', inplace=True)

# Display the messages in a table
st.table(df)

# Close the database connection
conn.close()
