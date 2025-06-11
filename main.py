
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Configuração da API key e Modelo
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Utilizando o modelo especificado
try:
    model = genai.GenerativeModel("gemini-2.0-flash")
except Exception as e:
    st.error(f"Erro ao carregar o modelo do Gemini especificado: {e}")
    st.info("Verifique se o nome do modelo está correto e se sua chave API tem acesso a ele")
    st.stop()

def gerar_resposta_gemini(prompt_completo):
    try:
        response = model.generate_content(prompt_completo)

        if response.parts:
            return response.text
        else:
            if response.prompt_feedback:
                st.warning(f"O prompt foi bloqueado. Razão: {response.prompt_feedback}")
                if response.prompt_feedback.safety_ratings:
                    for rating in response.prompt_feedback.safety_ratings:
                        st.caption(f"Categoria: {rating.category}, Probabilidade: {rating.probability}")
            return "A IA não pôde gerar uma resposta para este prompt. Verifique as mensagens acima ou tente reformular seu pedido."
    except Exception as e:
        st.error(f"Erro ao gerar resposta da IA: {str(e)}")
        if hasattr(e, 'message'):
            st.error(f"Detalhe da API Gemini: {e.message}")
        return None
    
# Configuração da página
st.set_page_config(page_title="Histórias Interativas - IA")

# Título do sistema
st.title("Criador de Histórias Interativas com IA")
st.markdown("Crie sua própria história dos sonhos com a ajuda da Inteligência Artificial!")

# Entradas do usuário
nome_protagonista = st.text_input("Forneça um nome para o(a) protagonista:")

genero_literario = st.selectbox(
    "Escolha um Gênero Literário:",
    ["Fantasia", "Ficção Científica", "Mistério", "Aventura"]
)

local_inicial = st.radio(
    "Escolha um local inicial:",
    ["Uma floresta antiga", "Uma cidade futurista", "Um castelo assombrado", "Uma nave espacial à deriva"]
)

frase_efeito = st.text_area("Adicione uma frase de efeito ou desafio inicial:")

if st.button("Gerar Ínicio da História"):
    if not nome_protagonista:
        st.warning("Por favor, informe um nome para o(a) protagonista.")
    elif not genero_literario:
        st.warning("Por favor, informe um gênero literário.")
    elif not local_inicial:
        st.warning("Por favor, informe um local inicial.")
    else:
        prompt_aluno = (
            f"Crie o início de uma história de '{genero_literario}' com o protagonista chamado '{nome_protagonista}'. A história começa em '{local_inicial}'. Incorpore a seguinte frase ou desafio no início: '{frase_efeito}'."
        )

        st.markdown("---")
        st.markdown("**Prompt que será enviado para a IA (para fins de aprendizado)**")
        st.text_area("", prompt_aluno, height=250)
        st.markdown("---")

        st.info("Aguarde, a IA está montando o início da história...")
        resposta_ia = gerar_resposta_gemini(prompt_aluno)

        if resposta_ia:
            st.markdown("### Sugestão de História da IA:")
            st.markdown(resposta_ia)
        else:
            st.error("Não foi possível gerar o roteiro. Verifique as mensagens acima ou tente novamente mais tarde.")