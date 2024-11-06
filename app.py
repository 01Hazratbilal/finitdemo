import os
import json

# Print the environment variable for debugging
print("Environment Variable 'google':", os.environ.get("google"))

# Load JSON only if environment variable is not None
google_env = os.environ.get("google")
if google_env is None:
    raise EnvironmentError("The 'google' environment variable is not set.")

credentials_info = json.loads(google_env)  # Parse the JSON
