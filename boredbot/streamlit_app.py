import random

import streamlit as st

from boredbot import content
from boredbot.bot import Chatbot


st.set_page_config(page_title="BoredBot", page_icon="B", layout="centered")

st.markdown(
    """
    <style>
    :root {
        --ink: #1f2933;
        --muted: #65707f;
        --panel: #fffdf7;
        --paper: #f7f2e8;
        --line: #ded5c6;
        --mint: #2d7d7a;
        --coral: #e4572e;
        --gold: #f3a712;
        --sidebar: #20232b;
    }
    .stApp {
        background:
            radial-gradient(circle at top left, rgba(243, 167, 18, 0.20), transparent 30rem),
            radial-gradient(circle at top right, rgba(45, 125, 122, 0.18), transparent 28rem),
            linear-gradient(135deg, #fffaf0 0%, #edf7f5 46%, #f9efe8 100%);
        color: var(--ink);
    }
    [data-testid="stHeader"] {
        background: transparent;
    }
    [data-testid="stToolbar"] {
        display: none;
    }
    [data-testid="stAppViewContainer"],
    [data-testid="stAppViewContainer"] * {
        color: var(--ink);
    }
    .block-container {
        max-width: 980px;
        padding-top: 4.5rem;
        padding-bottom: 7rem;
    }
    [data-testid="stAppViewContainer"] h1 {
        color: var(--ink);
        letter-spacing: 0;
        font-size: 3rem;
        line-height: 1;
        margin-bottom: 0.35rem;
    }
    .bot-hero {
        border: 1px solid rgba(31, 41, 51, 0.12);
        border-radius: 8px;
        background: rgba(255, 253, 247, 0.86);
        box-shadow: 0 22px 55px rgba(31, 41, 51, 0.12);
        padding: 1.25rem 1.35rem;
        margin-bottom: 1.25rem;
    }
    .bot-kicker {
        color: var(--coral);
        font-size: 0.78rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 0.35rem;
    }
    .bot-subtitle {
        color: var(--muted);
        font-size: 1rem;
        margin-top: 0;
        margin-bottom: 1rem;
    }
    .bot-stats {
        display: grid;
        gap: 0.75rem;
        grid-template-columns: repeat(3, minmax(0, 1fr));
    }
    .bot-stat {
        border: 1px solid rgba(31, 41, 51, 0.10);
        border-radius: 8px;
        background: #ffffff;
        padding: 0.75rem 0.85rem;
    }
    .bot-stat strong {
        display: block;
        font-size: 1.25rem;
        color: var(--mint);
    }
    .bot-stat span {
        color: var(--muted);
        font-size: 0.82rem;
    }
    .stChatMessage {
        border-radius: 8px;
        border: 1px solid rgba(31, 41, 51, 0.12);
        background: rgba(255, 255, 255, 0.92);
        box-shadow: 0 12px 32px rgba(31, 41, 51, 0.08);
        margin-bottom: 0.75rem;
        padding: 0.45rem 0.2rem;
    }
    .stChatMessage [data-testid="chatAvatarIcon-assistant"] {
        background: var(--gold);
    }
    .stChatMessage [data-testid="chatAvatarIcon-user"] {
        background: var(--mint);
    }
    .stChatMessage *,
    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] * {
        color: var(--ink);
    }
    [data-testid="stChatInput"] {
        background: rgba(32, 35, 43, 0.96);
        border-top: 1px solid rgba(255, 255, 255, 0.10);
    }
    [data-testid="stChatInput"] > div {
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.12);
        background: #2b2e38;
    }
    [data-testid="stChatInput"] textarea,
    [data-testid="stChatInput"] textarea::placeholder {
        color: #f5f5f0;
    }
    div[data-testid="stSidebar"] {
        background:
            linear-gradient(180deg, rgba(228, 87, 46, 0.12), transparent 16rem),
            var(--sidebar);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    div[data-testid="stSidebar"],
    div[data-testid="stSidebar"] *,
    div[data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
    div[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] * {
        color: #f5f5f0;
    }
    .stButton > button {
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.18);
        background: rgba(255, 255, 255, 0.96);
        color: var(--ink);
        font-weight: 700;
        min-height: 3rem;
        box-shadow: 0 8px 18px rgba(0, 0, 0, 0.14);
        transition: transform 120ms ease, border-color 120ms ease, box-shadow 120ms ease;
    }
    .stButton > button:hover {
        border-color: var(--gold);
        color: #155e5b;
        transform: translateY(-1px);
        box-shadow: 0 12px 22px rgba(0, 0, 0, 0.18);
    }
    @media (max-width: 700px) {
        .block-container {
            padding-top: 3rem;
        }
        [data-testid="stAppViewContainer"] h1 {
            font-size: 2.25rem;
        }
        .bot-stats {
            grid-template-columns: 1fr;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def get_bot() -> Chatbot:
    if "bot" not in st.session_state:
        st.session_state.bot = Chatbot()
    return st.session_state.bot


def get_messages() -> list[dict[str, str]]:
    if "messages" not in st.session_state:
        bot = get_bot()
        greeting = "Hey, I am BoredBot. Type help for commands."
        if bot.user_name:
            greeting = f"Hey {bot.user_name}, welcome back. Type help for commands."
        st.session_state.messages = [{"role": "assistant", "content": greeting}]
    return st.session_state.messages


def send_message(text: str) -> None:
    prompt = text.strip()
    if not prompt:
        return

    messages = get_messages()
    messages.append({"role": "user", "content": prompt})

    if prompt.lower() in {"quit", "exit", "bye"}:
        reply = f"Bye. {random.choice(content.RESPONSES['farewell'])}"
    else:
        reply = get_bot().respond(prompt)

    messages.append({"role": "assistant", "content": reply})


messages = get_messages()

st.markdown(
    f"""
    <section class="bot-hero">
        <div class="bot-kicker">Terminal bot, now with a face</div>
        <h1>BoredBot</h1>
        <p class="bot-subtitle">
            Ask for a joke, start a tiny game, save a name, or teach it a custom reply.
        </p>
        <div class="bot-stats">
            <div class="bot-stat"><strong>{len(messages)}</strong><span>messages this session</span></div>
            <div class="bot-stat"><strong>7</strong><span>quick commands</span></div>
            <div class="bot-stat"><strong>SQLite</strong><span>memory enabled</span></div>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.subheader("Quick Commands")
    shortcuts = [
        ("Joke", "joke"),
        ("Question", "question"),
        ("Challenge", "challenge"),
        ("Story", "story"),
        ("Time", "time"),
        ("Game", "game"),
        ("Help", "help"),
    ]
    for index, (label, shortcut) in enumerate(shortcuts):
        if st.button(label, key=f"shortcut_{index}", use_container_width=True):
            send_message(shortcut)
            st.rerun()

    st.divider()

    if st.button("Reset Chat", use_container_width=True):
        st.session_state.pop("messages", None)
        st.session_state.pop("bot", None)
        st.rerun()


for message in messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


if prompt := st.chat_input("Message BoredBot"):
    send_message(prompt)
    st.rerun()
