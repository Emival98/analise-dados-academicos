import numpy as np
import pandas as pd
import streamlit as st
from academico import index
from auth import validar_acesso


def main():
    # 1. Inicializa os estados da sessão
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "username" not in st.session_state:
        st.session_state.username = ""

    # 2. SE O USUÁRIO JÁ ESTIVER LOGADO -> Exibe APENAS o Dashboard
    if st.session_state.logged_in:
        # Botão de Logout na barra lateral
        if st.sidebar.button("🔚Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()  # Recarrega a aplicação para voltar à tela de login

        # Carrega o dashboard do módulo acadêmico
        index()

    # 3. SE NÃO ESTIVER LOGADO -> Exibe APENAS a Tela de Login
    else:
        #

        with st.form("login_form"):
            st.title("Login")
            st.subheader("Digite as suas credenciais")
            username = st.text_input("👤", help="Digite o seu user")
            password = st.text_input("🔑", type="password", help="Digite a sua senha")
            submit = st.form_submit_button("Entrar")

            if submit:
                if validar_acesso(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success(f"✅ Bem-vindo {username}!")
                    st.rerun()  # Força a reexecução imediata para entrar no bloco 'if st.session_state.logged_in'
                else:
                    st.error("❌ Usuário ou senha errada!")


if __name__ == "__main__":
    main()