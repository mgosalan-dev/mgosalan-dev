import os
import re
from github import Github

# Configuração
github_token = os.environ.get("GITHUB_TOKEN")
username = "mgosalan-dev"  # Coloca teu username do GitHub aqui

# Conectar na API
g = Github(github_token)
user = g.get_user(username)

# Pegar todos os repos públicos
repos = [repo for repo in user.get_repos() if not repo.archived and not repo.fork]

# Contar bytes por linguagem
languages = {}
for repo in repos:
    try:
        repo_langs = repo.get_languages()
        for lang, bytes_count in repo_langs.items():
            if lang in languages:
                languages[lang] += bytes_count
            else:
                languages[lang] = bytes_count
    except:
        continue

# Calcular porcentagens
total_bytes = sum(languages.values()) if languages else 1
percentages = {lang: (count / total_bytes) * 100 for lang, count in languages.items()}

# Gerar barras de progresso - 20 caracteres
def generate_bar(percentage):
    filled = int(percentage * 20 / 100)
    return "[" + "█" * filled + "▒" * (20 - filled) + "]"

# Preparar o texto de substituição
html_percent = percentages.get('HTML', 0)
css_percent = percentages.get('CSS', 0)
js_percent = percentages.get('JavaScript', 0)
python_percent = percentages.get('Python', 0)

skill_text = f"""🌟 Skill Tree (Aventureiro Rank SSS)

⚔️ Frontend Warrior
├─ HTML5................: {generate_bar(html_percent)} {html_percent:.2f}% ⭐⭐⭐⭐⭐
├─ CSS3 & Responsividade: {generate_bar(css_percent)} {css_percent:.2f}% ⭐⭐⭐⭐
└─ JavaScript...........: {generate_bar(js_percent)} {js_percent:.2f}% ⭐⭐⭐⭐

🛡️ Backend Explorer
└─ Python...............: {generate_bar(python_percent)} {python_percent:.2f}% ⭐⭐

🧙 Dev Skills
├─ Git/GitHub............: {generate_bar(50)} 50.00% ⭐⭐⭐
├─ Responsividade.......: {generate_bar(75)} 75.00% ⭐⭐⭐⭐
└─ Clean Code...........: {generate_bar(60)} 60.00% ⭐⭐⭐
"""

# Ler o README atual
with open("README.md", "r", encoding="utf-8") as file:
    content = file.read()

# Localizar e substituir a seção de skills
pattern = r"🌟 Skill Tree \(Aventureiro Rank SSS\)(.*?)(?=\n##|\Z)"
updated_content = re.sub(pattern, f"🌟 Skill Tree (Aventureiro Rank SSS){skill_text.split('🌟 Skill Tree (Aventureiro Rank SSS)')[1]}", content, flags=re.DOTALL)

# Salvar o README atualizado
with open("README.md", "w", encoding="utf-8") as file:
    file.write(updated_content)

print("✅ README atualizado com skills reais!")