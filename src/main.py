import os
import json
import streamlit as st
from openai import OpenAI
from openai import APIConnectionError
import base64
import requests
from openai import AuthenticationError
from streamlit.components.v1 import html
import streamlit.components.v1 as components
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MUST BE THE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="Chinese Tutor Chat",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={}
)

# Updated CSS with better text alignment
st.markdown("""
    <style>
        /* Reset and base styles */
        * {
            margin: 0 !important;
            padding: 0 !important;
            box-sizing: border-box !important;
        }

        /* Main container styles */
        .stApp {
            margin: 0 !important;
            padding: 0 !important;
            max-width: 100% !important;
            overflow: hidden !important;
        }

        /* Chat message container */
        .stChatMessage {
            background-color: transparent !important;
            padding: 0.75rem 1rem !important;
            margin: 0.5rem 0 !important;
        }

        /* Message content alignment */
        .stChatMessage > div {
            padding: 0.5rem !important;
            gap: 0.5rem !important;
        }

        /* Avatar styling */
        .stChatMessage .stAvatar {
            margin-right: 0.75rem !important;
        }

        /* Message text container */
        .stMarkdown {
            padding: 0 !important;
            margin: 0 !important;
        }

        /* Message text styling */
        .stMarkdown p {
            margin: 0.5rem 0 !important;
            line-height: 1.5 !important;
            white-space: pre-wrap !important;
        }

        /* Input container */
        .stChatInputContainer {
            padding: 1rem !important;
            border-top: 1px solid rgba(49, 51, 63, 0.1) !important;
        }

        /* Audio player container */
        .element-container:has(audio) {
            margin-top: 0.5rem !important;
            padding: 0 !important;
        }

        /* Audio player styling */
        audio {
            width: 100% !important;
            max-width: 300px !important;
            margin: 0.5rem 0 !important;
        }

        /* Remove Streamlit elements */
        #MainMenu, div.stApp > header, div.stApp > footer,
        .stDeployButton, [data-testid="stFooterBlock"], 
        [data-testid="stToolbar"], [data-testid="stDecoration"], 
        [data-testid="stStatusWidget"], .stActionButton,
        .viewerBadge_container__1QSob, .stStreamlitFooter,
        .stFooterBranding, .stFooter, footer {
            display: none !important;
        }

        /* Container adjustments */
        .main .block-container {
            padding: 0 !important;
            max-width: 100% !important;
        }

        /* Success message styling */
        .stSuccess {
            padding: 0.5rem 1rem !important;
            margin-bottom: 1rem !important;
        }

        /* Chinese text emphasis */
        .stMarkdown strong {
            font-weight: 600 !important;
        }

        /* Pinyin section spacing */
        .stMarkdown hr {
            margin: 1rem 0 !important;
            border-color: rgba(49, 51, 63, 0.1) !important;
        }

        /* Chat input styling */
        .stChatInput {
            padding: 0.75rem !important;
            border-radius: 0.5rem !important;
        }

        /* Hide Streamlit elements */
        .stApp footer,
        .stApp footer::before,
        .stApp footer::after,
        .viewerBadge_container__1QSob,
        .stDeployButton,
        [data-testid="stFooterBlock"],
        [data-testid="stDecoration"],
        div.element-container div.stMarkdown {
            display: none !important;
        }

        /* Adjust main container */
        .main .block-container {
            padding: 0 !important;
            max-width: 100% !important;
        }

        /* Success message styling */
        .stSuccess {
            background-color: #043927 !important;
            color: white !important;
            padding: 8px !important;
            border-radius: 0 !important;
        }

        /* Chat container adjustments */
        .stChatFloatingInputContainer {
            padding: 0.5rem !important;
            background: transparent !important;
        }

        /* Chat input styling */
        .stChatInput {
            padding: 0.5rem !important;
            border-radius: 20px !important;
        }

        /* Message container */
        .stChatMessage {
            background: transparent !important;
            padding: 1rem !important;
        }

        /* Title adjustments */
        h1 {
            font-size: 1.5rem !important;
            padding: 0.5rem !important;
            margin: 0 !important;
            text-align: center !important;
        }

        /* Remove extra padding */
        .stApp > div:first-child {
            padding-top: 0 !important;
        }

        /* Audio player styling */
        audio {
            width: 100% !important;
            max-width: 300px !important;
            margin: 0.5rem 0 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Load custom avatars with fallback to emojis
working_dir = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(working_dir, "assets")

# Create assets directory if it doesn't exist
if not os.path.exists(ASSETS_DIR):
    os.makedirs(ASSETS_DIR)

# Define avatar paths and fallbacks
TUTOR_AVATAR_PATH = os.path.join(ASSETS_DIR, "tutor_avatar.png")
USER_AVATAR_PATH = os.path.join(ASSETS_DIR, "user_avatar.png")

# Use emoji fallbacks if images don't exist
TUTOR_AVATAR = TUTOR_AVATAR_PATH if os.path.exists(TUTOR_AVATAR_PATH) else "👩‍🏫"
USER_AVATAR = USER_AVATAR_PATH if os.path.exists(USER_AVATAR_PATH) else "👤"

# Use environment variable instead of config.json
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# Create OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Test the API connection before starting
try:
    test_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "test"}],
        max_tokens=5
    )
    st.success("✅ Successfully connected to OpenAI API")
except AuthenticationError:
    st.error("❌ Invalid API key. Please check your OpenAI API key in config.json")
    st.stop()
except APIConnectionError:
    st.error("❌ Connection error. Please check your internet connection")
    st.stop()
except Exception as e:
    st.error(f"❌ Unexpected error: {str(e)}")
    st.stop()

def text_to_speech(text):
    """Convert text to speech using OpenAI's TTS"""
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text
        )
        
        # Save the audio to a temporary file
        audio_file_path = "temp_audio.mp3"
        response.stream_to_file(audio_file_path)
        
        # Read the audio file and create a base64 string
        with open(audio_file_path, "rb") as audio_file:
            audio_bytes = audio_file.read()
        audio_base64 = base64.b64encode(audio_bytes).decode()
        
        # Remove temporary file
        os.remove(audio_file_path)
        
        # Create HTML audio element
        audio_html = f"""
            <audio id="audio" controls>
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
            """
        return audio_html
    except Exception as e:
        return f"Error generating audio: {str(e)}"

# initialize chat session in streamlit if not already present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Add this near your other session state initialization
if "audio_elements" not in st.session_state:
    st.session_state.audio_elements = {}

# streamlit page title
st.title("Chinese Language Tutor")

# display chat history with custom avatars
for message in st.session_state.chat_history:
    with st.chat_message(message["role"], avatar=TUTOR_AVATAR if message["role"] == "assistant" else USER_AVATAR):
        st.markdown(message["content"])
        # Display stored audio if it exists for this message
        if message["role"] == "assistant" and message.get("id") in st.session_state.audio_elements:
            st.markdown(st.session_state.audio_elements[message["id"]], unsafe_allow_html=True)

# input field for user's message
user_prompt = st.chat_input("Ask your Chinese tutor...")

def format_chinese_response(text, pinyin):
    """Format the response with Chinese and pinyin"""
    return f"{text}\n\n---\nPinyin: {pinyin}"

if user_prompt:
    try:
        # add user's message to chat and display it with custom avatar
        with st.chat_message("user", avatar=USER_AVATAR):
            st.markdown(user_prompt)
        st.session_state.chat_history.append({"role": "user", "content": user_prompt})

        # send user's message to GPT-4o and get a response
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """You are a cute and demure Chinese language teacher. 
                Follow these rules in every response:
                1. Always start with Chinese endearing terms like '亲爱的' or '宝贝' first, followed by their meaning in brackets
                2. Speak in Chinese first, then provide English translation in brackets
                3. Format your responses in this structure:
                   - Chinese text first
                   - English translation in brackets
                   - Emojis for emotions
                4. Keep your tone cheerful, encouraging, and slightly playful
                5. Always teach something about Chinese language or culture
                6. Put English translations in brackets () right after each Chinese phrase
                7. Add pinyin at the bottom after '---'

                Example response:
                亲爱的！今天我们学习中文！(Darling! Today we are learning Chinese!)
                你说中文说得很好！(Your Chinese is very good!) 🌟
                让我们一起练习！(Let's practice together!) ✨

                ---
                Pinyin:
                亲爱的 (qīn'ài de)
                今天我们学习中文 (jīn tiān wǒ men xué xí zhōng wén)
                你说中文说得很好 (nǐ shuō zhōng wén shuō dé hěn hǎo)
                让我们一起练习 (ràng wǒ men yī qǐ liàn xí)"""},
                *st.session_state.chat_history
            ]
        )

        # Generate a unique ID for this message
        message_id = len(st.session_state.chat_history)
        
        assistant_response = response.choices[0].message.content
        st.session_state.chat_history.append({
            "role": "assistant", 
            "content": assistant_response,
            "id": message_id
        })

        # display tutor's response with custom avatar
        with st.chat_message("assistant", avatar=TUTOR_AVATAR):
            st.markdown(assistant_response)
            
            # Extract only the Chinese text for TTS
            main_text = assistant_response.split('---')[0].strip()
            chinese_only = ' '.join(
                part.split('(')[0].strip() 
                for part in main_text.split('\n') 
                if part.strip()
            )
            
            # Add audio player for the response
            audio_html = text_to_speech(chinese_only)
            # Store the audio element
            st.session_state.audio_elements[message_id] = audio_html
            st.markdown(audio_html, unsafe_allow_html=True)
            
    except APIConnectionError as e:
        st.error(f"Connection Error: Unable to connect to OpenAI API. Please check your internet connection and API key. Error: {str(e)}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
