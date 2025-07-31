import google.generativeai as genai
import PIL.Image
import io
import os

# Configure the generative AI model
if os.getenv("GOOGLE_API_KEY"):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- DIAGNOSTIC BLOCK ---
print("\n--- Listing Models ---")
try:
    found_vision_model = False
    for m in genai.list_models():
        if "generateContent" in m.supported_generation_methods:
            print(f"- Name: {m.name}, Supported Methods: {m.supported_generation_methods}, Input Token Limit: {m.input_token_limit}")
            if m.name == "models/gemini-1.0-pro-vision":
                found_vision_model = True
except Exception as e:
    print(f"Error listing models: {e}")
print(f"--- Found models/gemini-1.0-pro-vision: {found_vision_model} ---\n")
# --- END DIAGNOSTIC BLOCK ---


def process_image_query(image: PIL.Image.Image, prompt: str, chat_history: list) -> str:
    """
    Processes a user query about an image using the gemini-1.0-pro-vision model.
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')# Ensure this is 'gemini-1.0-pro-vision'

        contents = [prompt, image]

        response = model.generate_content(contents)

        return response.text

    except Exception as e:
        error_message = f"Error in Image Understanding Agent: {e}"
        print(error_message)
        return f"I apologize, but I encountered an error while trying to understand the image: {e}"
