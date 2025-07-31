Prodoc AI Multi-Agent System 🤖
A multi-agent AI application built with Streamlit and powered by the Google Gemini API. This system features two distinct agents—a Text Agent for general conversation and an Image Agent for visual question-answering—managed by a central orchestrator.

📸 Demo

Text Mode

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/0413fae2-0949-4556-bd08-2a34c7f86f30" />


Image Mode 

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/3be8e895-aef0-482a-90bc-250f2808c359" />



✨ Features
Multi-Agent Architecture: Implements two specialized agents:

Text Agent: Handles general knowledge questions, conversation, and text generation.

Image Agent: Analyzes uploaded images to answer specific questions about their content.

Dynamic UI: The user interface, built with Streamlit, dynamically changes based on the selected interaction mode.

Central Orchestrator: Simple yet effective logic routes the user's prompt to the appropriate agent.

Image Q&A: Users can upload images (jpg, png, webp) and ask questions directly about them.

Conversation History: The session state is used to maintain a running history of the conversation for context.

Secure API Key Handling: Uses a .env file to securely manage the Google API key, with a fallback to manual input.

🛠️ Tech Stack
Language: Python

Framework: Streamlit

AI Model: Google Gemini (gemini-1.5-flash or similar)

Libraries:

google-generativeai

Pillow

python-dotenv
