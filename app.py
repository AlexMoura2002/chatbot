import streamlit as st
import requests
import time

# ------------------------------
# CONFIGURAÇÃO INICIAL
# ------------------------------
st.set_page_config(
    page_title="Chatbot Rick and Morty",
    layout="centered",
    page_icon="🚀"
)

# ------------------------------
# INICIALIZAÇÕES
# ------------------------------
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# ------------------------------
# ESTILO GLOBAL PERSONALIZADO
# ------------------------------
st.markdown("""
    <style>
        body {
            background-color: #f8f9fa;
        }
        .chat-bubble {
            padding: 12px 18px;
            border-radius: 18px;
            margin: 6px 0;
            display: inline-block;
            max-width: 80%;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            font-size: 15px;
            line-height: 1.4;
        }
        .chat-user {
            background-color: #007bff;
            color: white;
            text-align: right;
            margin-left: auto;
        }
        .chat-assistant {
            background-color: #ffffff;
            border: 1px solid #ddd;
            color: #333;
            text-align: left;
            margin-right: auto;
        }
        .timestamp {
            font-size: 0.75em;
            color: #999;
            margin-bottom: 2px;
        }
        .input-style {
            background-color: #f1f3f5;
            border-radius: 10px;
            padding: 10px;
            border: 1px solid #ced4da;
            width: 100%;
            font-size: 15px;
        }
        .stButton>button {
            background-color: #007bff;
            color: white;
            border-radius: 10px;
            border: none;
            padding: 10px 20px;
            font-weight: bold;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #0056b3;
        }
    </style>
""", unsafe_allow_html=True)

# ------------------------------
# FUNÇÃO DE EXIBIÇÃO
# ------------------------------
def display_chat():
    for entry in st.session_state.conversation_history:
        role = entry["role"]
        message = entry["message"]
        image_url = entry.get("image_url", None)
        timestamp = entry.get("timestamp", "")

        if role == "user":
            st.markdown(
                f"""
                <div style='text-align: right; margin: 10px;'>
                    <div class='timestamp'>{timestamp}</div>
                    <div class='chat-bubble chat-user'>{message}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div style='text-align: left; margin: 10px;'>
                    <div class='timestamp'>{timestamp}</div>
                    <div class='chat-bubble chat-assistant'>{message}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            if image_url:
                st.image(image_url, width=150)

# ------------------------------
# API Rick and Morty
# ------------------------------
def fetch_rick_and_morty_data(query):
    base_url = "https://rickandmortyapi.com/api"
    response = requests.get(f"{base_url}/character/?name={query.lower()}")
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            character = data['results'][0]
            return {
                "text": f"**Personagem:** {character['name']}\n**Espécie:** {character['species']}\n**Status:** {character['status']}",
                "image_url": character['image']
            }
    return {"text": "Desculpe, não encontrei informações relacionadas.", "image_url": None}

# ------------------------------
# INTERFACE
# ------------------------------
col1, col2 = st.columns([1, 4])
with col1:
    st.image("assets/rickandmorty.png", width=120)
with col2:
    st.title("Chatbot Rick and Morty")
    st.caption("Faça perguntas sobre os personagens de Rick and Morty!")

with st.container(height=500, border=True):
    display_chat()

with st.form(key="chat_form", clear_on_submit=True):
    st.markdown("#### Digite o nome do personagem:")
    user_input = st.text_input("", placeholder="Ex: Rick Sanchez ou Morty Smith", label_visibility="collapsed")
    submit_button = st.form_submit_button("Enviar ➤")

if submit_button and user_input:
    with st.spinner("Buscando dados..."):
        st.session_state.conversation_history.append({
            "role": "user",
            "message": user_input,
            "timestamp": time.strftime("%H:%M:%S")
        })

        resposta = fetch_rick_and_morty_data(user_input)

        st.session_state.conversation_history.append({
            "role": "assistant",
            "message": resposta["text"],
            "image_url": resposta["image_url"],
            "timestamp": time.strftime("%H:%M:%S")
        })

        st.rerun()

st.markdown("---")
st.markdown(
    f"""
    <div style='text-align: center; font-size: 0.9em; color: #666; margin-top: 20px;'>
        Desenvolvido por Alex Moura • Versão Rick and Morty • {time.strftime('%d/%m/%Y')}<br>
        Contato: <a href='mailto:alexmoura@example.com'>alexmoura@example.com</a>
    </div>
    """,
    unsafe_allow_html=True
)
