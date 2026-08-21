import os 
from dotenv import load_dotenv
import json

load_dotenv()

def validar_acesso(usuario, senha):
    dados = os.getenv("USER_ADMIN") 
    credenciais = json.loads(dados) if dados else {}
    if usuario in credenciais and credenciais[usuario] == senha: #and credenciais.get('senha') == senha:
        return True
    return False

