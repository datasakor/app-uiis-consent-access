""" Part 2: Accessing the Token via URL

This part will handle the token access.

#### `app_uiis_consent_access.py`
"""

import streamlit as st
from cryptography.fernet import Fernet
import base64
import ast
from datetime import datetime

# Secret key for token encryption (must match the key used during token generation)



# Function to decode the token
def decode_token(token):
    try:
        data_decoded = cipher_suite.decrypt(token).decode()
        data_decoded = ast.literal_eval(data_decoded)  # Safely evaluate string to dictionary
        expiry = datetime.fromisoformat(data_decoded['Expiry'])
        if datetime.now() < expiry:
            return data_decoded
        else:
            return None
    except Exception as e:
        print(f"Error decoding token: {e}")
        return None


# Streamlit app for accessing the token
st.title("Access PII Information")

# # # Extract the token from the URL
# query_params = st.query_params()

# You can read query params using key notation
token_val = ""
end_to_end_key = ""
try:
    if st.query_params["token"]:
        token_val = st.query_params["token"]
        # st.success(token_val)
        st.text_input("Token from QR Code", value=token_val,type = "password", disabled=True)

    if st.query_params["key"]:
        end_to_end_key = st.query_params["key"]
        # st.success(end_to_end_key)
        st.text_input("Share Key", value=token_val,type = "password", disabled=True)
except Exception as e:
    st.error(f"Invalid request query params : {e}")


# SECRET_KEY = "iKD4HAU4w0p-d3Z5pEMARP3v2KQVtikaFliY8At5jWU="

token_str = st.text_input("Enter token from QR Code", value=token_val, disabled=True)

if token_str:
    if st.button("Verify"):
        try:
            secrete_key = end_to_end_key
            cipher_suite = Fernet(secrete_key)

            token_bytes = base64.urlsafe_b64decode(token_str)
            data = decode_token(token_bytes)
            if data:
                st.write("Access granted. Here is the PII:")
                st.write(data)
            else:
                st.error("Token expired or invalid.")
        except Exception as e:
            st.error(f"Error: {e}")
else:
    st.error("No token provided.")

