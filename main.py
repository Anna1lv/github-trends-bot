import os
from dotenv import load_dotenv
from email_sender import enviar_email
from github_api import buscar_repositorios_em_alta

load_dotenv()

EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE")
SENHA_APP = os.getenv("SENHA_APP")
EMAIL_DESTINATARIO = os.getenv("EMAIL_DESTINATARIO")

if __name__ == "__main__":
    print("🔎 Buscando repositórios em alta (Top Geral)...")

    # Chamando sem especificar linguagem = traz o Top Geral!
    repos = buscar_repositorios_em_alta(quantidade=5)

    if repos:
        print("✉️ Enviando e-mail...")
        enviar_email(
            remetente=EMAIL_REMETENTE,
            senha_app=SENHA_APP,
            destinatario=EMAIL_DESTINATARIO,
            assunto="GitHub Trends: Os projetos mais quentes da semana 🔥",
            repositorios=repos,
        )
    else:
        print("⚠️ Nenhum repositório encontrado.")