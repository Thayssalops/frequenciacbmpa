# Guia de Hospedagem no Netlify - Gestão Interna DTIC

## ⚠️ Limitações Importantes

O Netlify é uma plataforma de **hospedagem estática + serverless JavaScript/Go**. 
Seu projeto Flask (Python) **NÃO pode rodar integralmente no Netlify**.

Referência: https://docs.netlify.com/functions/overview/

---

## ✅ Solução Recomendada: Frontend + Backend Separados

### Arquitetura:
```
Frontend (Netlify)              Backend (Outro Serviço)
├── HTML/CSS/JS estático       ├── Flask Python app
├── Formulários                 ├── Autenticação
└── Comunicação via API REST    └── JSON database
```

---

## 📋 Passo 1: Preparar o Frontend para Netlify

### 1.1 Arquivos estáticos (já no lugar correto)
- `static/` → CSS, JS, assets
- `templates/` → HTML files
- Copiar para pasta `public/` ou ajustar `netlify.toml`

### 1.2 Converter templates para SPA (Single Page App)

Atualize seus templates para fazer chamadas AJAX em vez de formulários tradicionais:

```javascript
// Exemplo: autenticação via API
async function login(username, password) {
  const response = await fetch('https://SEU_BACKEND_URL/api/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  
  const data = await response.json();
  localStorage.setItem('token', data.token);
  // Redirecionar ou atualizar interface
}
```

---

## 🖥️ Passo 2: Escolher Hospedagem para Backend Python

### Opções (com Docker suportado):

| Plataforma | Preço | Suporte | Docs |
|-----------|-------|--------|------|
| **Render** | Grátis/pago | Excelente | https://render.com/docs |
| **Railway** | Pago | Bom | https://railway.app/docs |
| **Heroku** | Pago | Bom | https://devcenter.heroku.com/ |
| **AWS** | Pago | Completo | https://aws.amazon.com/ |
| **DigitalOcean** | Pago | Bom | https://docs.digitalocean.com/ |

**Recomendação**: Render (integração com GitHub, suporte a Docker nativo)

---

## 🚀 Passo 3: Configurar Netlify

### 3.1 Instalar Netlify CLI
```bash
npm install -g netlify-cli
```

### 3.2 Autenticar
```bash
netlify login
```

### 3.3 Conectar repositório Git
```bash
netlify connect
```

Ou via dashboard: https://app.netlify.com

### 3.4 Configurar Variáveis de Ambiente

No Netlify Dashboard → Settings → Build & Deploy → Environment:
```
REACT_APP_BACKEND_URL=https://seu-backend-url.com
API_BASE=https://seu-backend-url.com/api
```

---

## 📁 Estrutura Recomendada do Projeto

```
gestao-interna-dtic/
├── netlify.toml          ✅ Já criado
├── .netlifyignore        ✅ Já criado
├── public/               ← Frontend (estático)
│   ├── index.html
│   ├── css/
│   └── js/
├── backend/              ← Backend Python (separado)
│   ├── app.py
│   ├── requirements.txt
│   └── ...
├── netlify/
│   └── functions/        ← Opcional: APIs Node.js
│       └── example.ts
└── README.md
```

---

## 🔄 Fluxo de Autenticação Recomendado

1. **Login (Frontend)**
   ```
   POST /api/login → Backend Flask
   ↓
   Retorna JWT token
   ↓
   LocalStorage: token
   ```

2. **Requisições Autenticadas**
   ```
   GET /api/dados
   Header: Authorization: Bearer {token}
   ↓
   Valida no Backend
   ```

3. **Logout**
   ```
   LocalStorage.removeItem('token')
   ```

---

## 🔗 CORS e Variáveis de Ambiente

### Backend (app.py)
```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=[
    "https://seu-site.netlify.app",
    "http://localhost:3000"  # Dev local
])
```

### Frontend
```javascript
const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000';

fetch(`${API_URL}/api/login`, {
  // ... request
})
```

---

## 📦 Deploy Steps

### Backend (Render.com exemplo):
1. Push código para GitHub
2. Criar app no Render
3. Conectar repositório
4. Definir comando: `gunicorn app:app`
5. Definir variável `PORT=5000`

### Frontend (Netlify):
1. Atualizar `netlify.toml` com URL do backend
2. Push para `main` branch
3. Netlify faz deploy automático

---

## ✨ Próximos Passos

- [ ] Separar backend (copiar Flask para pasta `backend/`)
- [ ] Escolher plataforma para backend
- [ ] Refatorar templates para SPA/AJAX
- [ ] Implementar autenticação via JWT
- [ ] Testar CORS
- [ ] Deploy backend
- [ ] Configurar Netlify com URL do backend
- [ ] Deploy frontend Netlify

---

## 📚 Documentação Útil

- **Netlify**: https://docs.netlify.com/
- **Netlify Functions**: https://docs.netlify.com/functions/overview/
- **Netlify CLI**: https://docs.netlify.com/api-and-cli-guides/cli-guides/get-started-with-cli/
- **Netlify Redirects**: https://docs.netlify.com/manage/routing/redirects/

---

## ⚡ Alternativa: Usar Express.js no Netlify Functions

Se preferir manter tudo no Netlify, pode converter Flask → Express.js e usar Netlify Functions:

```bash
npm init -y
npm install express cors
mkdir netlify/functions
```

Mas isso exigiria reescrever `app.py` em JavaScript/TypeScript.

---

**Dúvidas?** Consulte a documentação oficial:
https://docs.netlify.com/
