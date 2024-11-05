import streamlit as st

def main():
    # Check if GOOGLE_CREDENTIALS is available
    if 'GOOGLE_CREDENTIALS' in st.secrets:
        st.success("GOOGLE_CREDENTIALS found!")
        
        # Print the GOOGLE_CREDENTIALS to check its content
        st.json(st.secrets['GOOGLE_CREDENTIALS'])
    else:
        st.error("GOOGLE_CREDENTIALS not found.")

if __name__ == "__main__":
    main()
