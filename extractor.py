import streamlit as st
import google.generativeai as genai
import json

# Ensure your secrets.toml file is configured correctly
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# HARDCODED BUSINESS LOGIC
# These are your local market rates in INR. Update these if prices fluctuate.
STANDARD_PRICES = {
    "Milk": 60.0,
    "Paneer": 350.0,
    "Ghee": 800.0,
    "Mawa": 400.0
}

system_instruction = """
You are a high precision financial data extraction engine specializing in digitizing handwritten agribusiness ledgers. 
Your sole function is to analyze images of ledger entries and output the data in a strict, validated JSON structure.

Objective: Extract transaction records from the provided image and format them into a JSON array of objects.

Strict Output Schema:
Each object in the JSON array must contain exactly these keys with these exact data types:
* "Customer_Name": (String) The name of the account holder at the top of the page (e.g., "Arjun Bhaiya"). If completely illegible, output "NULL".
* "Date": (String) The transaction date. Format: YYYY-MM-DD. Assume the year is 2026. If an item like Paneer or Ghee is written on the side without a specific date, assign it the most recent date listed in the primary column.
* "Product": (String) Categorize strictly as: "Milk", "Paneer", "Ghee", or "Mawa". Do not use any other variations.
* "Quantity": (Float) The numerical volume or weight. Output only the number. 
* "Amount": (Float) Always output 0.0. The backend system will calculate this.

Execution Rules:
1. Return ONLY the JSON array. Do not wrap it in markdown block quotes.
2. Prioritize accuracy. Cross reference quantity if digits are ambiguous.
3. Ignore crossed out rows entirely.
"""

# Upgraded to the latest flash model string to resolve the 404 error
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash-latest',
    system_instruction=system_instruction,
    generation_config={"response_mime_type": "application/json"}
)

def process_ledger_image(uploaded_image):
    try:
        response = model.generate_content([uploaded_image])
        structured_data = json.loads(response.text)
        
        # THE FINANCIAL INTERCEPTION LAYER
        # We calculate the real cash flow here based on standard pricing, not AI guesses.
        for item in structured_data:
            product = item.get("Product")
            quantity = item.get("Quantity", 0.0)
            
            if product in STANDARD_PRICES:
                item["Amount"] = quantity * STANDARD_PRICES[product]
            else:
                # Flag the amount as 0.0 if the product category is unknown
                item["Amount"] = 0.0
                
        return structured_data
        
    except Exception as e:
        # Trap the error so the UI does not freeze
        return [{"Customer_Name": "ERROR", "Date": "ERROR", "Product": "ERROR", "Quantity": 0.0, "Amount": 0.0, "error": str(e)}]
