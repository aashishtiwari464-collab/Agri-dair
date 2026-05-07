import streamlit as st
import google.generativeai as genai
import json

# The application will crash here if you do not set up your secrets.toml file
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

system_instruction = """
You are a high precision financial data extraction engine specializing in digitizing handwritten agribusiness ledgers. 
Your sole function is to analyze images of ledger entries and output the data in a strict, validated JSON structure.

Objective: Extract transaction records from the provided image and format them into a JSON array of objects.

Strict Output Schema:
Each object in the JSON array must contain exactly these keys with these exact data types:
* "Customer_Name": (String) The name of the account holder. If completely illegible, output "NULL".
* "Date": (String) The transaction date. Format: YYYY-MM-DD. Use the current year if missing.
* "Product": (String) Categorize strictly as: "Milk", "Paneer", "Ghee", or "Mawa". Do not use any other variations. If unknown, output "FLAG_FOR_REVIEW".
* "Quantity": (Float) The numerical volume or weight. Output only the number.
* "Amount": (Float) The total transaction cost. Remove currency symbols and commas.

Execution Rules:
1. Return ONLY the JSON array. Do not wrap it in markdown block quotes.
2. Prioritize accuracy. Cross reference quantity and standard price if digits are ambiguous.
3. Ignore crossed out rows entirely.
"""

model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=system_instruction,
    generation_config={"response_mime_type": "application/json"}
)

def process_ledger_image(uploaded_image):
    try:
        response = model.generate_content([uploaded_image])
        structured_data = json.loads(response.text)
        return structured_data
    except Exception as e:
        # Trap the error so the UI does not freeze
        return [{"Customer_Name": "ERROR", "Date": "ERROR", "Product": "ERROR", "Quantity": 0.0, "Amount": 0.0, "error": str(e)}]
        
