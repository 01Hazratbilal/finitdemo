import streamlit as st
import json
from google.oauth2 import service_account
from google.cloud import documentai  # or any other Google Cloud library you need

# Load the credentials from Streamlit secrets
credentials_info = json.loads(st.secrets["gcs_connections"]["GOOGLE_APPLICATION_CREDENTIALS"])

# Create credentials object
credentials = service_account.Credentials.from_service_account_info(credentials_info)

# Initialize your client (for example, Document AI client)
client = documentai.DocumentProcessorServiceClient(credentials=credentials)

# Now you can use the client to interact with Google Cloud services
