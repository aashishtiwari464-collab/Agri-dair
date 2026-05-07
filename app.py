import streamlit as st
from PIL import Image
# Import the function you saved in your new extractor.py file
from extractor import process_ledger_image

st.set_page_config(layout="wide")
st.title("Agribusiness Ledger Digitization")

# Create two columns for the Phase 2 Validation Gate
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Upload Ledger")
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        # Streamlit requires PIL to display the image properly
        image = Image.open(uploaded_file)
        st.image(image, caption="Raw Handwritten Ledger", use_container_width=True)

with col2:
    st.subheader("2. Validate Data")
    if uploaded_file is not None:
        if st.button("Run OCR Extraction"):
            with st.spinner("Parsing data..."):
                # Call the function from your separated backend file
                # You must pass the PIL image object, not the raw uploaded file
                extracted_data = process_ledger_image(image)
                
                # Display the extracted JSON as a table for review
                st.data_editor(extracted_data, num_rows="dynamic")
              
