import streamlit as st
import json

# Load the credentials from Streamlit secrets
try:
    credentials_info = json.loads(st.secrets["gcs_connections"]["GOOGLE_APPLICATION_CREDENTIALS"])
    st.write("Credentials loaded successfully!")
except KeyError as e:
    st.write(f"Error: {e} - Check your secrets configuration.")
except Exception as e:
    st.write(f"An error occurred: {e}")
