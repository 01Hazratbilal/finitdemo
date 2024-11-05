import streamlit as st
import json

st.write(st.secrets)

# Check if 'gcs_connections' exists in st.secrets
if "gcs_connections" in st.secrets:
    credentials_info = json.loads(st.secrets["gcs_connections"]["GOOGLE_APPLICATION_CREDENTIALS"])
    st.write("Credentials loaded successfully!")
else:
    st.write("Error: 'gcs_connections' key not found in secrets.")
