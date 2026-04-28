<img width="1236" height="744" alt="{92F8F0D7-E3CC-4CCB-93A3-E03A3F0296AB}" src="https://github.com/user-attachments/assets/5de02ec8-5ade-495b-a7a3-260b0bc6ec86" />

# Sistema de Gestão de Pessoal - CBMPA/DTIC

Este sistema foi desenvolvido para a **Diretoria de Tecnologia da Informação e Comunicação (DTIC)** do Corpo de Bombeiros Militar do Pará (CBMPA). A aplicação evoluiu para uma solução integrada que realiza a gestão tanto de **Voluntários Civis** quanto de **Militares (Praças)**, automatizando a emissão de folhas de frequência e registros de serviço extraordinário.

## 🚀 Funcionalidades

O sistema é dividido em dois módulos principais, identificados visualmente na interface:

### 🔹 Módulo Voluntários Civis (Painel Azul)

* **Gestão de Efetivo:** Cadastro e remoção de voluntários (Funções: Técnico/Secretária).
* **Folha de Frequência:** Gera relatório em HTML/PDF com preenchimento automático de dias úteis e fins de semana, conforme o mês atual.
* **Base de Dados:** Persistência em arquivo JSON dedicado (`voluntarios.json`).

### 🔺 Módulo Militares / Praças (Painel Vermelho)

* **Gestão de Praças:** Cadastro de militares com graduação (SD, CB, SGT, SUB TEN) e nome de guerra.
* **Serviço Extraordinário:** Geração automática da folha de "Registro de Serviço Extraordinário / Reforço do Expediente".
* **Automação:** O sistema preenche automaticamente os dias do mês, inserindo "SÁBADO" e "DOMINGO" e deixando os dias úteis prontos para assinatura e horário (padrão 17:00).
* **Base de Dados:** Persistência em arquivo JSON dedicado (`militares.json`).

### ⚙️ Características Técnicas

* **Autenticação:** Acesso restrito via senha administrativa definida em variável de ambiente (`.env`).
* **Interface:** Layout responsivo e limpo construído com **Tailwind CSS**.
* **Ambiente Brasileiro:** O container Docker é configurado explicitamente com `locales` `pt_BR.UTF-8` para garantir datas e formatações corretas.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.9
* **Framework Web:** Flask
* **Servidor de Aplicação:** Gunicorn (configurado no Dockerfile)
* **Frontend:** HTML5 + Tailwind CSS (CDN)
* **Containerização:** Docker e Docker Compose

## 📦 Instalação e Execução

### Pré-requisitos

* Docker e Docker Compose instalados na máquina.

### 1. Configuração Inicial

Na raiz do projeto, crie (ou verifique) o arquivo `.env` com a senha de administração:

```bash
ADMIN_PASSWORD=1234  # Altere para sua senha segura

```

### 2. Executando com Docker (Recomendado)

O projeto já inclui um `Dockerfile` otimizado que configura o idioma PT-BR e instala as dependências.

```bash
# Constrói a imagem e sobe o container
docker-compose up --build

```

Após o comando, acesse o sistema em:
👉 **http://localhost:5000**

*(Nota: O container roda internamente na porta 8000, mas o `docker-compose` a mapeia para a 5000)*.

### 3. Execução Manual (Sem Docker)

Caso prefira rodar diretamente no Python:

```bash
# Crie e ative o ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
flask run

```

## 📂 Estrutura de Arquivos

* `app.py`: Lógica principal, rotas e controle de sessão.
* `templates/`:
* `index.html`: Dashboard principal com os dois painéis (Civil/Militar).
* `folha_civil.html` & `folha_militar.html`: Modelos de impressão.


* `static/`: Contém os brasões e logos (CBMPA, DTE, Defesa Civil).
* `*.json`: Arquivos onde os dados são salvos automaticamente.

---

© 2026 CBMPA/DAL OBRAS - [Licença MIT](https://www.google.com/search?q=LICENSE)
