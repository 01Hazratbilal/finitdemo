import streamlit as st

# Check if 'gcs_connections' exists in st.secrets
if "gcs_connections" in st.secrets:
    st.write("gcs_connections key found!")
else:
    st.write("Error: 'gcs_connections' key not found in secrets.")
