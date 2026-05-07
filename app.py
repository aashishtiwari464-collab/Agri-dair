import streamlit as st
from PIL import Image
from extractor import process_ledger_image
from database import initialize_database, commit_records_to_db

# Run this once when the app starts to ensure the table exists
initialize_database()

st.set_page_config(layout="wide")
st.title("Supply Chain Ledger Digitization")

# Initialize the session state to prevent data loss on rerun
if "extracted_data" not in st.session_state:
    st.session_state.extracted_data = None

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Upload Ledger")
    uploaded_file = st.file_uploader("Upload Handwritten Image", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Raw Ledger", use_container_width=True)

with col2:
    st.subheader("2. Validate and Commit")
    
    # Only show the extract button if an image is uploaded
    if uploaded_file is not None:
        if st.button("Run OCR Extraction"):
            with st.spinner("Parsing AI data..."):
                # Call the API and save the result into the session state
                st.session_state.extracted_data = process_ledger_image(image)
        
        # If we have data in the session state, display the validation gate
        if st.session_state.extracted_data is not None:
            st.warning("Review the AI extraction carefully. Correct any errors before committing.")
            
            # The data editor allows the user to fix hallucinated numbers
            # We capture the output of this editor into a new variable
            edited_data = st.data_editor(st.session_state.extracted_data, num_rows="dynamic")
            
            if st.button("Commit to Database", type="primary"):
                # Send the clean, human-reviewed data to SQLite
                commit_records_to_db(edited_data)
                st.success("Records successfully written to the database.")
                # Clear the session state to prepare for the next ledger page
                st.session_state.extracted_data = None
                st.rerun()
