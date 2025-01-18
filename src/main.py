# Add this after your imports and before any other Streamlit commands
st.set_page_config(
    page_title="Chinese Tutor Chat",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={}
)

# Updated CSS with background color fixes
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
            background-color: #ffffff !important;
            margin: 0 !important;
            padding: 0 !important;
            max-width: 100% !important;
            overflow: hidden !important;
        }

        /* Chat container styles */
        .stChatFloatingInputContainer {
            background-color: #ffffff !important;
            padding: 1rem !important;
            border-top: 1px solid #f0f0f0 !important;
        }

        .stChatMessage {
            background-color: #ffffff !important;
            padding: 1rem !important;
        }

        /* Remove all Streamlit elements */
        #MainMenu, div.stApp > header, div.stApp > footer,
        .stDeployButton, [data-testid="stFooterBlock"], 
        [data-testid="stToolbar"], [data-testid="stDecoration"], 
        [data-testid="stStatusWidget"], .stActionButton,
        .viewerBadge_container__1QSob, .stStreamlitFooter,
        .stFooterBranding, .stFooter, footer, footer::before, footer::after {
            display: none !important;
            opacity: 0 !important;
            height: 0 !important;
            visibility: hidden !important;
            position: absolute !important;
            top: -9999px !important;
        }

        /* Container adjustments */
        .main .block-container, div.stApp > div {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
            background-color: #ffffff !important;
        }

        /* Element spacing */
        .element-container, .stMarkdown, .stChatMessage {
            padding: 0.5rem 1rem !important;
            margin: 0 !important;
            background-color: #ffffff !important;
        }

        /* Body styles */
        body {
            background-color: #ffffff !important;
            margin: 0 !important;
            padding: 0 !important;
            min-height: 100vh !important;
        }

        /* Chat message styles */
        .stChatMessage {
            border-radius: 0 !important;
            border: none !important;
            box-shadow: none !important;
        }

        /* Input container */
        .stChatInputContainer {
            padding: 1rem !important;
            background-color: #ffffff !important;
            border-top: 1px solid #f0f0f0 !important;
        }

        /* Audio player styling */
        audio {
            width: 100% !important;
            max-width: 300px !important;
            margin-top: 0.5rem !important;
        }
    </style>
""", unsafe_allow_html=True)
