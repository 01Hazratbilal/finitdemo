import streamlit as st

# Access secrets
try:
    service_account_info = st.secrets["gcp_service_account"]
    st.write("Successfully loaded Google Cloud service account secrets.")
    st.write("Project ID:", service_account_info["project_id"])
    # Display more information if needed, but avoid printing sensitive data like private keys
except KeyError:
    st.error("Google Cloud service account secrets not found in Streamlit secrets.")
