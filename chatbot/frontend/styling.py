import streamlit as st
import html
from io import BytesIO
import base64
from PIL import Image, ImageSequence

def slow_down_gif(gif_path):
    """Slows down a GIF animation by increasing frame duration."""
    
    img = Image.open(gif_path)
    frames = []
    durations = []
    factor = 10   # Factor for the gif to be slowed by

    for frame in ImageSequence.Iterator(img):
        frames.append(frame.copy())
        
        # Multiply original frame duration by 10
        durations.append(frame.info.get("duration", 100) * factor)   # 10 times slower

    # Write slowed GIF into memory
    buffer = BytesIO()
    frames[0].save(
        buffer,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        disposal=2
    )
    buffer.seek(0)

    # Encode to base64 for embedding in CSS
    gif_b64 = base64.b64encode(buffer.read()).decode("utf-8")
    return f"data:image/gif;base64,{gif_b64}"

def apply_styling():
    """Injects CSS for sidebar, background, and chat box styling."""
    
    slowed_gif = slow_down_gif("background.gif")
    
    st.markdown(
        """
        <style>
        /* Sidebar dark green */
        [data-testid="stSidebar"] {
            background-color: #013220 !important;
        }

        /* Background GIF only on main chat area */
        .stApp {
            background: black !important;
        }

        [data-testid="stChatMessageContainer"] {
            background-image: url('{slowed_gif}');
            background-size: cover;
            background-position: center;
        }

        /* Chat message custom styling */
        .user-box {
            background-color:#2f2f2f;
            color:white;
            padding:10px;
            border-radius:10px;
            margin-bottom:5px;
        }

        .ai-box {
            background-color:#1a1a1a;
            color:white;
            padding:10px;
            border-radius:10px;
            margin-bottom:5px;
        }

        .chat-header {
            font-weight:bold;
            font-size:1.5em;
            margin-bottom:5px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def render_user_message(message):
    """Render user chat bubble with custom styling."""
    st.markdown(
        f"""
        <div class="user-box">
            <div class="chat-header">USER:</div>
            {html.escape(message)}
        </div>
        """,
        unsafe_allow_html=True
    )

def render_ai_message(message):
    """Render AI chat bubble with custom styling."""
    st.markdown(
        f"""
        <div class="ai-box">
            <div class="chat-header">TriKnow:</div>
            {html.escape(message)}
        </div>
        """,
        unsafe_allow_html=True
    )
