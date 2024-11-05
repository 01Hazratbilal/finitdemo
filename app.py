import streamlit as st

# Check available secrets
st.write(st.secrets)  # This will show all available secrets, remove it after testing.
# Google Analytics setup
PROPERTY_ID = "465906322"

# Load credentials from GitHub secrets
if "GOOGLE_CREDENTIALS" in st.secrets:
    json_credentials = st.secrets["GOOGLE_CREDENTIALS"]
else:
    st.error("Google credentials are not set in the environment variables.")
    st.stop()  # Stop the execution if the secret is not found

# Authentication
credentials = service_account.Credentials.from_service_account_info(json_credentials)
client = BetaAnalyticsDataClient(credentials=credentials)
