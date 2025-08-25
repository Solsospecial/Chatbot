import streamlit as st
import html
import os
from PIL import Image, ImageSequence

def slow_down_gif(input_path: str, output_path: str, factor: int = 10):
    """Slows down a GIF animation by increasing frame duration."""
    img = Image.open(input_path)
    frames = []
    durations = []

    for frame in ImageSequence.Iterator(img):
        frames.append(frame.copy())
        # Multiply original frame duration by factor
        duration = frame.info.get("duration", 100) * factor
        durations.append(duration)

    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        disposal=2
    )

def apply_styling():
    """Injects CSS for sidebar, background, and chat box styling."""
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
            background-image: url('myfolder/background.gif');
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

def render_user_message(message: str):
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

def render_ai_message(message: str):
    """Render AI chat bubble with custom styling."""
    st.markdown(
        f"""
        <div class="ai-box">
            <div class="chat-header">AI:</div>
            {html.escape(message)}
        </div>
        """,
        unsafe_allow_html=True
    )
