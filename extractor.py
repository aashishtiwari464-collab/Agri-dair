import google.generativeai as genai
import json

# Initialize the model and embed the prompt as a system instruction
# The response_mime_type constraint is critical. It forces the API to only return JSON.
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction='''[INSERT THE ENTIRE EXTRACTION PROMPT HERE]''',
    generation_config={"response_mime_type": "application/json"}
)

def process_ledger_image(uploaded_image):
    # 1. Execute the API call
    response = model.generate_content([uploaded_image])

    # 2. The Validation Gate
    try:
        # You must convert the text string into a native Python dictionary
        structured_data = json.loads(response.text)
        return structured_data
    except json.JSONDecodeError:
        # If the model disobeys and returns raw text, trap the error here.
        # Do not let this crash your Streamlit frontend.
        return [{"error": "OCR failed to return valid JSON. Manual entry required."}]
      
