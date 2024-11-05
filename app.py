import streamlit as st
from google.oauth2 import service_account
import json

# Load Google credentials from Streamlit secrets
try:
    # Retrieve the JSON string from the secrets
    json_credentials = st.secrets["GOOGLE_CREDENTIALS"]
    
    # Check if it's a string and convert to dictionary
    if isinstance(json_credentials, str):
        credentials_dict = json.loads(json_credentials)
    else:
        st.error("Invalid format for GOOGLE_CREDENTIALS.")
        st.stop()

    # Create credentials object from the dictionary
    credentials = service_account.Credentials.from_service_account_info(credentials_dict)
except KeyError:
    st.error("Google credentials are not set in the environment variables.")
    st.stop()  # Stop the execution if the secret is not found
except ValueError as e:
    st.error(f"Failed to parse Google credentials: {e}")
    st.stop()
