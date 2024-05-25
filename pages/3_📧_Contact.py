import streamlit as st
import sqlite3
import re
import base64

st.set_page_config("☎ Contact")
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

# Connect to the SQLite database
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Create the contacts table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY, name TEXT, email TEXT, message TEXT)''')

# Add a contact page
st.title("Contact Us")

# Define CSS styling
contact_form_style = """
<style>
.contact-form {
    max-width: 500px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 5px;
    box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
}
.contact-form h3 {
    text-align: center;
    margin-bottom: 20px;
}
.contact-form input[type="text"], .contact-form input[type="email"], .contact-form textarea {
    width: 100%;
    padding: 10px;
    margin-bottom: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
    box-shadow: 0px 0px 5px rgba(0,0,0,0.1);
    resize: none;
}
.contact-form input[type="submit"] {
    width: 100%;
    padding: 10px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}
.contact-form input[type="submit"]:hover {
    background-color: #3e8e41;
}
</style>
"""

# Add CSS styling to the page
st.markdown(contact_form_style, unsafe_allow_html=True)

# Add a container for the contact form
contact_form = st.container()

with contact_form:
    with st.form("contact_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        message = st.text_area("Message")

        if st.form_submit_button("Submit"):
            with st.spinner("Sending message..."):
                # Check if the email is valid
                if re.match(r"[^@]+@[^@]+\.[^@]+", email):
                    # Insert the user input into the SQLite table
                    c.execute("INSERT INTO contacts (name, email, message) VALUES (?,?,?)", (name, email, message))
                    conn.commit()
                    st.success("Message sent!")
                else:
                    st.error("Invalid email address")

# Close the database connection
conn.close()