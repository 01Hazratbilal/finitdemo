import os
import json
from google.oauth2 import service_account
from google.analytics.data import BetaAnalyticsDataClient

# Retrieve the Google credentials as a JSON string from environment variables
google_credentials = os.environ.get('google_credentials')

# Raise an error if the environment variable is missing
if google_credentials is None:
    raise EnvironmentError("Google service account credentials not set.")

# Parse the JSON string into a dictionary
credentials_info = json.loads(google_credentials)
credentials = service_account.Credentials.from_service_account_info(credentials_info)

# Instantiate the Google Analytics client
client = BetaAnalyticsDataClient(credentials=credentials)
