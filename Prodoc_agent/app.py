import streamlit as st
import PIL.Image
import io
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import our agent modules (these should now use 'gemini-1.5-flash' or similar)
from image_agent import process_image_query
from text_agent import process_text_query

# --- Streamlit UI Configuration ---
st.set_page_config(
    page_title="Prodoc AI Multi-Agent System",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="auto"
)

st.title("🤖 Prodoc AI Multi-Agent System")
st.markdown("Choose your interaction mode: **Image Q&A** or **General Chat**.")

# --- API Key Input (for demonstration, recommend .env for production) ---
google_api_key = os.getenv("GOOGLE_API_KEY")

if not google_api_key:
    st.warning("Please set your Google API Key in a `.env` file (e.g., `GOOGLE_API_KEY='your_key'`) or enter it below.")
    google_api_key = st.text_input("Enter your Google API Key:", type="password")
    if google_api_key:
        os.environ["GOOGLE_API_KEY"] = google_api_key # Set for current session
        # Configure genai immediately after the key is available
        import google.generativeai as genai
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    else:
        st.stop() # Stop execution if no key is provided
else:
    # Configure genai if the key is already in environment variables
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# --- Session State Initialization ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [] # Stores text-based chat for text_agent
if "current_image" not in st.session_state:
    st.session_state.current_image = None # Stores the PIL Image object
if "image_filename" not in st.session_state:
    st.session_state.image_filename = None # Stores the filename for display
if "mode" not in st.session_state:
    st.session_state.mode = "Text" # Default mode

# --- Mode Selection ---
st.subheader("1. Select Interaction Mode")
mode_selection = st.radio(
    "Choose how you want to interact:",
    ("Text (General Chat)", "Image (Image Q&A)"),
    index=0 if st.session_state.mode == "Text" else 1, # Set initial index based on session state
    key="mode_radio", # Unique key for the widget
    horizontal=True
)

# Update session state based on user selection
if mode_selection == "Text (General Chat)":
    st.session_state.mode = "Text"
    # Clear image-related session state if switching to text mode
    st.session_state.current_image = None
    st.session_state.image_filename = None
elif mode_selection == "Image (Image Q&A)":
    st.session_state.mode = "Image"

# --- Conditional Content Display ---

user_prompt = "" # Initialize user_prompt outside of the conditional blocks

if st.session_state.mode == "Image":
    st.subheader("2. Upload an Image")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "webp"])

    if uploaded_file is not None:
        # Check if a new file is uploaded or if the file is different from the current one
        if st.session_state.image_filename != uploaded_file.name or st.session_state.current_image is None:
            image = PIL.Image.open(uploaded_file)
            st.session_state.current_image = image
            st.session_state.image_filename = uploaded_file.name
            st.image(image, caption=f"Uploaded Image: {uploaded_file.name}", use_container_width=True) # FIX: use_container_width
            st.success("Image uploaded successfully! You can now ask questions about it.")
        else:
            # If the same file is uploaded again, just display it
            st.image(st.session_state.current_image, caption=f"Uploaded Image: {st.session_state.image_filename}", use_container_width=True) # FIX: use_container_width
    else:
        st.session_state.current_image = None
        st.session_state.image_filename = None
        st.info("Please upload an image to use the Image Q&A mode.")

    st.subheader("3. Ask Your Question about the Image")
    user_prompt = st.text_area("Type your message here:", height=100, placeholder="e.g., What is in this image? Describe this document.", key="image_prompt_input")

elif st.session_state.mode == "Text":
    st.subheader("2. Start Your Chat")
    user_prompt = st.text_area("Type your message here:", height=100, placeholder="e.g., Tell me a joke? Explain machine learning.", key="text_prompt_input")
    # No image upload section for text mode

# --- Submit Button ---
if st.button("Get Response", use_container_width=True):
    if not user_prompt.strip():
        st.warning("Please enter a message.")
    elif st.session_state.mode == "Image" and st.session_state.current_image is None:
        st.warning("Please upload an image before asking a question in Image Q&A mode.")
    else:
        with st.spinner("Agent is thinking..."):
            response_text = ""
            # --- Orchestrator Logic ---
            if st.session_state.mode == "Image" and st.session_state.current_image is not None:
                st.info(f"Routing to Image Understanding Agent for '{st.session_state.image_filename}'...")
                response_text = process_image_query(
                    st.session_state.current_image,
                    user_prompt,
                    st.session_state.chat_history # Pass chat history for context
                )
            elif st.session_state.mode == "Text":
                st.info("Routing to Text Generation Agent...")
                response_text = process_text_query(
                    user_prompt,
                    st.session_state.chat_history
                )
            else:
                response_text = "Please select an interaction mode and provide valid input."

            # Update chat history (for text-based context)
            st.session_state.chat_history.append({"role": "user", "parts": [{"text": user_prompt}]})
            st.session_state.chat_history.append({"role": "model", "parts": [{"text": response_text}]})

            st.subheader("Agent's Response:")
            st.write(response_text)

# --- Display Chat History ---
# Display history for the current mode only for clarity, or filter
st.subheader("Conversation History:")
# You might want to filter history here based on mode, or clear it when switching modes significantly.
# For simplicity, keeping a single history for now.
for message in reversed(st.session_state.chat_history): # Display latest first
    if message["role"] == "user":
        st.text_area("You:", value=message["parts"][0]["text"], height=70, disabled=True)
    elif message["role"] == "model":
        st.text_area("Agent:", value=message["parts"][0]["text"], height=70, disabled=True)

st.markdown("---")
st.markdown("Built for Prodoc AI Intern Assignment")
