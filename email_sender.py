import email.message
import smtplib


def gerar_html_email(repositorios):
    """Gera o corpo do e-mail em formato HTML moderno e minimalista."""
    itens_html = ""
    for repo in repositorios:
        itens_html += f"""
        <div style="border: 1px solid #e1e4e8; border-radius: 8px; padding: 18px; margin-bottom: 16px; background-color: #ffffff; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                <h3 style="margin: 0; font-size: 16px; color: #0969da;">
                    <a href="{repo['url']}" style="text-decoration: none; color: #0969da; font-weight: 600;">{repo['nome']}</a>
                </h3>
                <span style="font-size: 12px; color: #57606a; background-color: #f6f8fa; padding: 2px 8px; border-radius: 12px; border: 1px solid #d0d7de;">
                    ★ {repo['estrelas']}
                </span>
            </div>
            <p style="color: #57606a; font-size: 12px; margin: 0 0 10px 0;">por <strong>@{repo['autor']}</strong></p>
            <p style="color: #24292f; font-size: 14px; line-height: 1.5; margin: 0 0 12px 0;">{repo['descricao']}</p>
            <div style="font-size: 12px; color: #57606a;">
                <span style="display: inline-block; width: 10px; height: 10px; background-color: #3572A5; border-radius: 50%; margin-right: 4px;"></span>
                <span>{repo['linguagem']}</span>
            </div>
        </div>
        """

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
    </head>
    <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f6f8fa; padding: 24px 12px; color: #24292f; margin: 0;">
        <div style="max-width: 580px; margin: 0 auto; background: #ffffff; border-radius: 12px; padding: 28px; border: 1px solid #d0d7de;">
            
            <!-- Header -->
            <div style="border-bottom: 1px solid #d0d7de; padding-bottom: 16px; margin-bottom: 20px;">
                <h2 style="color: #24292f; margin: 0 0 6px 0; font-size: 20px; font-weight: 600;">Github Trends Digest</h2>
                <p style="color: #57606a; margin: 0; font-size: 14px;">Os projetos mais populares criados no GitHub nos últimos 7 dias.</p>
            </div>

            <!-- Content -->
            {itens_html}

            <!-- Footer -->
            <footer style="margin-top: 28px; text-align: center; font-size: 12px; color: #57606a; border-top: 1px solid #d0d7de; padding-top: 16px;">
                GitHub Trends Bot &bull; Automação semanal personalizada
            </footer>
        </div>
    </body>
    </html>
    """
    return html


def enviar_email(
    remetente, senha_app, destinatario, assunto, repositorios
):
    """Envia o e-mail formatado via servidor SMTP (Gmail)."""
    corpo_html = gerar_html_email(repositorios)

    msg = email.message.Message()
    msg["Subject"] = assunto
    msg["From"] = remetente
    msg["To"] = destinatario
    msg.add_header("Content-Type", "text/html")
    msg.set_payload(corpo_html, charset="utf-8")

    try:
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(remetente, senha_app)
        s.sendmail(remetente, [destinatario], msg.as_string().encode("utf-8"))
        s.quit()
        print("✅ E-mail enviado com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao enviar e-mail: {e}")
        return False