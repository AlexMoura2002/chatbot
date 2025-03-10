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
# FUNÇÕES AUXILIARES
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
                    <div style='color: #666; font-size: 0.8em;'>{timestamp}</div>
                    <div style='background: #007bff; color: white; padding: 10px; border-radius: 15px; display: inline-block;'>{message}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div style='text-align: left; margin: 10px;'>
                    <div style='color: #666; font-size: 0.8em;'>{timestamp}</div>
                    <div style='background: #f1f0f0; padding: 10px; border-radius: 15px; display: inline-block;'>{message}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            if image_url:
                st.image(image_url, width=150)

# Função para buscar personagens de Rick and Morty
def fetch_rick_and_morty_data(query):
    base_url = "https://rickandmortyapi.com/api"
    
    # Buscando por personagens (ajustado para aceitar qualquer nome de personagem)
    response = requests.get(f"{base_url}/character/?name={query.lower()}")
    if response.status_code == 200:
        data = response.json()
        if data['results']:  # Verifique se há resultados
            character = data['results'][0]  # Pega o primeiro resultado
            return {
                "text": f"Personagem: {character['name']}\nEspécie: {character['species']}\nStatus: {character['status']}",
                "image_url": character['image']
            }

    # Caso não encontre resultados
    return {"text": "Desculpe, não encontrei informações relacionadas.", "image_url": None}

# ------------------------------
# INTERFACE
# ------------------------------
col1, col2 = st.columns([1, 4])
with col1:
    # Usando uma imagem alternativa para testar
    st.image("https://upload.wikimedia.org/wikipedia/commons/a/a2/Rick_and_Morty_logo.svg", width=80)  # Logo do Rick and Morty
with col2:
    st.title("Chatbot Rick and Morty")
    st.caption("Faça perguntas sobre os personagens de Rick and Morty!")


with st.container(height=500, border=True):
    display_chat()

with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Digite o nome do personagem:", placeholder="Me fale sobre o Rick ou Morty.")
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
    <div style='text-align: center; font-size: 0.9em; color: #666;'>
        Desenvolvido por Alex Moura • Versão Rick and Morty • {time.strftime('%d/%m/%Y')} contato: <a href='mailto:alexmoura@example.com'>alexmoura@example.com</a>
    </div>
    """,
    unsafe_allow_html=True
)
