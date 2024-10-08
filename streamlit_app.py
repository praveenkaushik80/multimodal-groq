import streamlit as st
from groq import Groq
from PIL import Image
import PIL
import time
import os
from io import BytesIO
import base64

# Function to analyze an image from a URL with retry mechanism
def analyze_image(image_url, retries=3, delay=2):
    for attempt in range(retries):
        try:
            client = Groq()
            completion = client.chat.completions.create(
                model="llava-v1.5-7b-4096-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "What's in this image?"},
                            {"type": "image_url", "image_url": {"url": image_url}},
                        ]
                    }
                ],
                temperature=1,
                max_tokens=1024,
                top_p=1,
                stream=False,
                stop=None,
            )
            return completion.choices[0].message.content
        except Exception as e:
            if attempt < retries - 1:
                st.error(f"API issue encountered: {e}. Retrying in {delay} seconds...")
            else:
                return f"Failed after {retries} attempts. Error: {e}"
            time.sleep(delay)  # Wait before retrying

# Streamlit app
st.title("Image Analyzer with Groq")
st.write(
    "Type image url below and Groq will describe the image! "
    "To use this app, you need to provide an Groq API key, which you can get [here](https://console.groq.com/keys). "
)
st.write("Enter an image URL to describe the image.")
model_options = [
    "llava-v1.5-7b-4096-preview",
    "llama-3.2-1b-preview",
    "llama-3.2-3b-preview",
]
with st.sidebar:
    selected_model = st.selectbox("Select any Groq Model", model_options)
    groq_api_key = st.text_input("Groq API Key", type="password")
    if not groq_api_key:
        st.info("Please add your Groq API key to continue.", icon="🗝️")
    else:
        # Set it as an environment variable
        os.environ["GROQ_API_KEY"] = groq_api_key
# Main section
try:
    image_url = st.text_input("Enter Image URL")
    if image_url:
        ai_response = analyze_image(image_url)
        st.image(image_url, use_column_width=True)
        st.write("AI's Response:", ai_response)
except Exception as e:
     st.error(f"API issue encountered: {e}.")
    
