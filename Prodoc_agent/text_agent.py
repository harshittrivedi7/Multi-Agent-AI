import google.generativeai as genai
import os

# Configure the generative AI model (API key will be set in app.py's environment)
# The `genai.configure` function is idempotent, so calling it multiple times is safe.
# We ensure the API key is set if available in the environment.
if os.getenv("GOOGLE_API_KEY"):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def process_text_query(prompt: str, chat_history: list) -> str:
    """
    Processes a general text-based user query using an available Gemini model.

    Args:
        prompt (str): The user's text prompt.
        chat_history (list): The ongoing list of chat messages for context.
                             This list should be in the format expected by Gemini API:
                             [{"role": "user", "parts": [{"text": "..."}]},
                              {"role": "model", "parts": [{"text": "..."}]}]

    Returns:
        str: The agent's generated text response.
    """
    try:
        # --- CHANGE THIS LINE ---
        # Use a model confirmed to be in your list_models() output, e.g., 'gemini-1.5-pro'
        model = genai.GenerativeModel('gemini-1.5-pro') # Or 'gemini-1.5-flash' if you prefer

        # Start a chat with the provided history to maintain context
        # The `start_chat` method handles the multi-turn conversation automatically.
        convo = model.start_chat(history=chat_history)

        # Send the user's new message
        response = convo.send_message(prompt)

        # Return the generated text
        return response.text

    except Exception as e:
        error_message = f"Error in Text Generation Agent: {e}"
        print(error_message) # Print to console for debugging
        return f"I apologize, but I encountered an error while trying to respond: {e}"
