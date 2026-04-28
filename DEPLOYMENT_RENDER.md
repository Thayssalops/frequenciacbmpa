# Deployment Backend em Render.com

[Render](https://render.com) é recomendado para hospedar o backend Python com Flask.

## ✅ Vantagens

- ✅ Suporte nativo a Docker
- ✅ Deploy automático via GitHub
- ✅ Certificado HTTPS automático
- ✅ Variáveis de ambiente integradas
- ✅ Logs em tempo real
- ✅ Plano gratuito disponível
- ✅ Simples de configurar

---

## 📋 Pré-requisitos

1. Código Python em GitHub
2. Conta em [render.com](https://render.com) (free)
3. Dockerfile no repositório

---

## 🛠️ Estrutura de Pastas

```
seu-repo/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── militares.json
│   └── voluntarios.json
├── public/
│   └── (frontend estático)
├── netlify.toml
└── README.md
```

---

## 1️⃣ Preparar Dockerfile

Crie `backend/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Expor porta
EXPOSE 5000

# Comando para rodar
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
```

---

## 2️⃣ Configurar requirements.txt

`backend/requirements.txt`:

```
Flask>=2.3
Flask-CORS>=4.0
python-dotenv>=0.19
gunicorn>=20.1.0
PyJWT>=2.6.0
Werkzeug>=2.3
```

---

## 3️⃣ Atualizar app.py para Produção

```python
# Antes
if __name__ == '__main__':
    app.run(debug=True)

# Depois
if __name__ == '__main__':
    # Em produção, gunicorn roda isso
    app.run(debug=False, host='0.0.0.0', port=5000)
```

---

## 4️⃣ Criar .dockerignore

`backend/.dockerignore`:

```
__pycache__/
*.pyc
*.pyo
.env
.git
.gitignore
.pytest_cache/
*.log
venv/
.venv/
```

---

## 5️⃣ Push para GitHub

```bash
# Estrutura esperada no GitHub:
# seu-usuario/seu-repo/
# ├── backend/
# │   ├── app.py
# │   ├── requirements.txt
# │   ├── Dockerfile
# │   └── ...
# ├── public/
# └── netlify.toml

git add .
git commit -m "Preparação para Render.com"
git push origin main
```

---

## 6️⃣ Criar Aplicação no Render

### Acesso:
1. Ir para [dashboard.render.com](https://dashboard.render.com)
2. Fazer login/cadastro

### Criar Web Service:
1. Clique em **New** → **Web Service**
2. Conectar repositório GitHub
3. Preencher:
   - **Name**: `gestao-interna-api` (ou seu nome)
   - **Root Directory**: `backend`
   - **Runtime**: `Docker`
   - **Build Command**: deixar em branco (usa Dockerfile)
   - **Start Command**: deixar em branco (usa Dockerfile)

### Variáveis de Ambiente:
Na aba **Environment**, adicione:

```
ADMIN_PASSWORD=sua-senha-super-secreta
SECRET_KEY=sua-chave-jwt-aleatoria
FLASK_ENV=production
```

### Plano:
- **Free** (bom para teste)
- Ou **Starter** ($7/mês) para garantir uptime

### Deploy:
Clique em **Create Web Service** e aguarde.

---

## 7️⃣ Obter URL da Aplicação

Após deploy sucesso, você terá uma URL como:
```
https://gestao-interna-api.onrender.com
```

---

## 8️⃣ Configurar Netlify com URL do Render

Atualizar `netlify.toml`:

```toml
[[redirects]]
from = "/api/*"
to = "https://gestao-interna-api.onrender.com/api/:splat"
status = 200
force = false
```

Ou no Netlify Dashboard:
- **Settings** → **Environment**
- Adicionar: `REACT_APP_BACKEND_URL=https://gestao-interna-api.onrender.com`

---

## 9️⃣ Testar Integração

```bash
# Testar login
curl -X POST https://gestao-interna-api.onrender.com/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"sua-senha"}'

# Resposta esperada:
# {"token":"eyJhbGciOiJIUzI1NiIs...","expires_in":86400}
```

---

## 🔟 Monitoramento

### Acessar Logs:
No dashboard Render → seu serviço → **Logs**

### Problema: Aplicação não inicia
1. Verifique erros nos Logs
2. Testar Dockerfile localmente:
   ```bash
   cd backend
   docker build -t gestao-test .
   docker run -p 5000:5000 gestao-test
   ```

### Problema: CORS não funciona
Verificar em `app.py`:
```python
from flask_cors import CORS

CORS(app, origins=[
    "https://seu-site.netlify.app",
    "http://localhost:8888"
])
```

### Problema: Timeout (>30s)
- Pode ser limite de execução
- Revisar lógica de processamento
- Usar Background Jobs para tarefas longas

---

## 📦 Atualizar Código

Quando fizer mudanças:

```bash
# 1. Fazer commit
git add backend/
git commit -m "Atualização backend"

# 2. Push
git push origin main

# 3. Render detecta automaticamente
# Você pode ver na aba Deploys
```

---

## 💰 Custos

- **Free**: Aplicação dorme após 15min de inatividade
- **Starter ($7/mês)**: Uptime garantido
- **Standard+**: Para escalabilidade

Para teste/desenvolvimento, Free é suficiente.

---

## ✅ Checklist

- [ ] Dockerfile criado em `backend/`
- [ ] requirements.txt atualizado
- [ ] .dockerignore criado
- [ ] app.py configurado para produção
- [ ] CORS configurado com origem Netlify
- [ ] Code pushed em GitHub
- [ ] Conta Render criada
- [ ] Web Service criado
- [ ] Variáveis de ambiente definidas
- [ ] Deploy bem-sucedido
- [ ] URL obtida (ex: https://meu-api.onrender.com)
- [ ] Netlify configurado com URL
- [ ] Teste de login funcionando

---

## 🔗 Referências

- [Render Docs - Docker](https://render.com/docs/docker)
- [Render Docs - Environment](https://render.com/docs/environment-variables)
- [Render Docs - Deploy Web Service](https://render.com/docs/deploy-web-service)
- [Gunicorn Docs](https://gunicorn.org/)

---

## 🆘 Suporte

- Render: [docs.render.com](https://render.com/docs)
- Community: [answers.render.com](https://answers.render.com)
