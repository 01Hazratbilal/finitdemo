import streamlit as st
from google.oauth2 import service_account
import json

# Load Google credentials from Streamlit secrets
try:
    json_credentials = st.secrets["general"]["GOOGLE_CREDENTIALS"]
    credentials_dict = json.loads(json_credentials)
    credentials = service_account.Credentials.from_service_account_info(credentials_dict)
except KeyError:
    st.error("Google credentials are not set in the environment variables.")
    st.stop()
except json.JSONDecodeError:
    st.error("Failed to decode JSON from GOOGLE_CREDENTIALS.")
    st.stop()
except Exception as e:
    st.error(f"An error occurred: {e}")
    st.stop()
