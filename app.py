import streamlit as st
import pandas as pd
import plotly.express as px
from google.oauth2 import service_account
from google.analytics.data import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunRealtimeReportRequest, Dimension, Metric
from datetime import datetime, timedelta

# Google Analytics setup
PROPERTY_ID = "465906322"

import json
st.write(st.secrets)
