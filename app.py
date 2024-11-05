import os
import json
import streamlit as st

google_credentials = st.secrets("GOOGLE_CREDENTIALS")
st.write(google_credentials)  # Log the credentials
credentials = json.loads(google_credentials)
