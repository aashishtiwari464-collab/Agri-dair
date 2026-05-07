import streamlit as st
from PIL import Image
from extractor import process_ledger_image
from database import initialize_database, commit_records_to_db
import pandas as pd

# Enforce schema on startup
initialize_database()

st.set_page_config(page_title="Dairy Ledger OCR", layout="wide")
st.title("Patel Dairy Farm Cash Flow Engine")

# Prevent data wiping upon Streamlit UI updates
if "extracted_data" not in st.session_state:
    st.session_state.extracted_data = None

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Ingest Ledger")
    uploaded_file = st.file_uploader("Upload Handwritten Image", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Raw Physical Ledger", use_container_width=True)

with col2:
    st.subheader("2. Validate & Commit")
    
    if uploaded_file is not None:
        if st.button("Execute Extraction Pipeline"):
            with st.spinner("Processing through vision model..."):
                st.session_state.extracted_data = process_ledger_image(image)
        
        if st.session_state.extracted_data is not None:
            st.warning("You must verify these numbers manually before committing.")
            
            # Allow manual overrides of the AI data
            edited_data = st.data_editor(st.session_state.extracted_data, num_rows="dynamic", use_container_width=True)
            
            if st.button("Commit Verified Data to SQLite", type="primary"):
                # Handle Pandas conversion if Streamlit auto-casts the data
                if hasattr(edited_data, 'to_dict'):
                    data_to_commit = edited_data.to_dict(orient='records')
                else:
                    data_to_commit = edited_data
                    
                commit_records_to_db(data_to_commit)
                st.success("Ledger successfully digitized and stored.")
                
                # Wipe the temporary memory for the next upload
                st.session_state.extracted_data = None
                st.rerun()
