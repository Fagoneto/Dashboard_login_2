import streamlit as st
import database as db

# Inicializa o banco de dados
db.criar_tabela_usuario()

# Página de Login
def pagina_login():
    st.title("Login")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Login"):
        if db.verificar_login(usuario, senha):
            st.session_state['logado'] = True
            st.session_state['usuario'] = usuario
            st.success("Login realizado com sucesso!")
        else:
            st.error("Usuário ou senha incorretos")

# Página de Cadastro
def pagina_cadastro():
    st.title("Cadastro")
    nome = st.text_input("Nome")
    usuario = st.text_input("Usuário")
    telefone = st.text_input("Telefone")
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")
    if st.button("Cadastrar"):
        db.inserir_usuario(nome, usuario, telefone, email, senha)
        st.success("Cadastro realizado com sucesso!")

# Página Principal
def pagina_principal():
    st.title(f"Bem-vindo, {st.session_state['usuario']}!")
    st.write("Aqui você pode acessar o conteúdo do aplicativo.")

# Navegação
def main():
    if 'logado' not in st.session_state:
        st.session_state['logado'] = False

    if not st.session_state['logado']:
        pagina = st.sidebar.radio("Escolha uma página", ["Login", "Cadastro"])
        if pagina == "Login":
            pagina_login()
        else:
            pagina_cadastro()
    else:
        pagina_principal()

if __name__ == "__main__":
    main()