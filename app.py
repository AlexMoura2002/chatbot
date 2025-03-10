import streamlit as st
import requests
import google.generativeai as genai
import time

# ------------------------------
# CONFIGURAÇÃO INICIAL
# ------------------------------
st.set_page_config(
    page_title="Chatbot Pokémon",
    layout="centered",
    page_icon="🎮"
)

# ------------------------------
# INICIALIZAÇÕES
# ------------------------------
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# Configurar a API Key do Gemini
genai.configure(api_key="AIzaSyA-ypywLAf4JkiXQCvL1H7EQj_kp5MPDUY")  # https://aistudio.google.com/app/apikey

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
                    <div style='background: #007bff; color: white; padding: 10px; border-radius: 15px; display: inline-block;'>
                        {message}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div style='text-align: left; margin: 10px;'>
                    <div style='color: #666; font-size: 0.8em;'>{timestamp}</div>
                    <div style='background: #f1f0f0; padding: 10px; border-radius: 15px; display: inline-block;'>
                        {message}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            if image_url:
                st.image(image_url, width=150)

def fetch_pokemon_data(pokemon_name):
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}")
    if response.status_code == 200:
        data = response.json()
        pokemon_info = {
            "name": data["name"].capitalize(),
            "id": data["id"],
            "types": [t["type"]["name"] for t in data["types"]],
            "abilities": [a["ability"]["name"] for a in data["abilities"]],
            "base_experience": data["base_experience"],
            "image_url": data["sprites"]["front_default"]
        }
        return pokemon_info
    else:
        return None

# ------------------------------
# CONFIGURAÇÃO DO GEMINI
# ------------------------------
@st.cache_resource
def load_gemini():
    return genai.GenerativeModel('gemini-1.5-pro')

model = load_gemini()

# ------------------------------
# LÓGICA DE RESPOSTAS
# ------------------------------
def generate_response(user_input):
    try:
        start_time = time.time()
        
        # Extraindo nome do Pokémon da pergunta
        words = user_input.lower().split()
        pokemon_data = None
        for word in words:
            pokemon_data = fetch_pokemon_data(word)
            if pokemon_data:
                break
        
        if not pokemon_data:
            return {"text": "Desculpe, não consegui encontrar informações sobre esse Pokémon.", "image_url": None}
        
        # Criando o contexto para o Gemini
        context = f"""
        Nome: {pokemon_data['name']}
        ID: {pokemon_data['id']}
        Tipos: {', '.join(pokemon_data['types'])}
        Habilidades: {', '.join(pokemon_data['abilities'])}
        Experiência Base: {pokemon_data['base_experience']}
        """
        
        prompt = f"""
        Você é um assistente especializado em Pokémon.
        Forneça informações detalhadas usando o contexto abaixo:

        {context}

        Pergunta do usuário: {user_input}

        Resposta:
        """
        
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.0,
                max_output_tokens=200
            )
        )
        
        return {
            "text": response.text if response.text else "Informação não encontrada.",
            "image_url": pokemon_data['image_url']
        }
        
    except Exception as e:
        return {"text": f"Erro no sistema: {str(e)}", "image_url": None}

# ------------------------------
# INTERFACE
# ------------------------------
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png", width=80)  # Pikachu
with col2:
    st.title("Chatbot Pokémon")
    st.caption("Faça perguntas sobre seus Pokémon favoritos!")

with st.container(height=500, border=True):
    display_chat()

with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Digite sua pergunta:", placeholder="Me fale sobre o Pikachu.")
    submit_button = st.form_submit_button("Enviar ➤")

if submit_button and user_input:
    with st.spinner("Buscando dados dos Pokémon..."):
        st.session_state.conversation_history.append({
            "role": "user",
            "message": user_input,
            "timestamp": time.strftime("%H:%M:%S")
        })
        
        resposta = generate_response(user_input)
        
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
        Desenvolvido por Professor Douglas Braga de AI • Versão Pokémon • {time.strftime('%d/%m/%Y')} contato: <a herf
    </div>
    """,
    unsafe_allow_html=True
)
