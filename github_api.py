import os
from datetime import datetime, timedelta
import requests


def buscar_repositorios_em_alta(linguagem=None, dias=7, quantidade=5):
    """
    Busca os repositórios mais populares criados recentemente no GitHub.
    Se linguagem for None, busca o Top Geral de todas as linguagens.
    """
    data_limite = (datetime.now() - timedelta(days=dias)).strftime("%Y-%m-%d")

    # Monta a query: se tiver linguagem especificada inclui, senão busca geral
    query = f"created:>{data_limite}"
    if linguagem:
        query += f"+language:{linguagem}"

    url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc"

    headers = {"User-Agent": "GitHub-Trends-Bot-App"}

    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        resposta = requests.get(url, headers=headers)
        resposta.raise_for_status()

        dados = resposta.json()
        repositorios_brutos = dados.get("items", [])[:quantidade]

        repositorios_filtrados = []
        for repo in repositorios_brutos:
            info = {
                "nome": repo["name"],
                "autor": repo["owner"]["login"],
                "descricao": repo["description"]
                or "Sem descrição informada.",
                "estrelas": repo["stargazers_count"],
                "url": repo["html_url"],
                "linguagem": repo["language"] or "Não especificada",
            }
            repositorios_filtrados.append(info)

        return repositorios_filtrados

    except requests.exceptions.RequestException as e:
        print(f"Erro ao conectar com a API do GitHub: {e}")
        return []


if __name__ == "__main__":
    print("🔎 Buscando Top Geral de repositórios em alta no GitHub...\n")
    resultados = buscar_repositorios_em_alta(quantidade=5)

    for idx, repo in enumerate(resultados, 1):
        print(f"{idx}. 🌟 {repo['nome']} (por @{repo['autor']})")
        print(f"   ⭐ Estrelas: {repo['estrelas']}")
        print(f"   🔤 Linguagem: {repo['linguagem']}")
        print(f"   📝 Descrição: {repo['descricao']}")
        print(f"   🔗 Link: {repo['url']}\n")