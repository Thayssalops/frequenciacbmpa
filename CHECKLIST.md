# Checklist de Preparação - Netlify

## ✅ Já Feito
- [x] `netlify.toml` - Configuração principal
- [x] `.netlifyignore` - Arquivos a ignorar no build
- [x] `package.json` - Dependências Node.js
- [x] `netlify/functions/example.ts` - Exemplo de API
- [x] `NETLIFY_GUIDE.md` - Guia completo
- [x] `DEVELOPMENT.md` - Guia de desenvolvimento local

## 📝 Próximos Passos Necessários

### 1. Separar Código Python (Backend)
- [ ] Criar pasta `backend/` e mover arquivos Python lá
  ```bash
  mkdir backend
  cp app.py backend/
  cp requirements.txt backend/
  cp militares.json backend/
  cp voluntarios.json backend/
  ```

- [ ] Criar `backend/Dockerfile` (ajustar se necessário)
- [ ] Criar `backend/.dockerignore`
- [ ] Criar `backend/README.md` com instruções de deploy

### 2. Preparar Frontend (Estático)
- [ ] Copiar templates HTML para `public/`
  ```bash
  mkdir -p public
  cp templates/*.html public/
  ```

- [ ] Refatorar HTML templates para usar AJAX
  - Remover `<form>` tradicionais
  - Adicionar JavaScript para fazer chamadas POST/GET
  - Exemplo em `AJAX_MIGRATION.md` abaixo

- [ ] Copiar/organizar CSS em `public/css/`
- [ ] Organizar JavaScript em `public/js/`

### 3. Implementar Autenticação via JWT
- [ ] Backend Python: gerar JWT tokens
  ```python
  pip install PyJWT
  ```

- [ ] Frontend: armazenar token em localStorage
  - Ver exemplo em `AUTHENTICATION.md` abaixo

### 4. Configurar CORS no Backend
- [ ] Instalar Flask-CORS
  ```python
  pip install flask-cors
  ```

- [ ] Adicionar ao `app.py`:
  ```python
  from flask_cors import CORS
  CORS(app, origins=["https://seu-site.netlify.app"])
  ```

### 5. Variáveis de Ambiente
- [ ] Criar `.env.example`:
  ```env
  ADMIN_PASSWORD=seu_admin_password_aqui
  REACT_APP_BACKEND_URL=http://localhost:5000
  ```

- [ ] Adicionar ao `.gitignore`:
  ```
  .env
  .env.local
  .env.*.local
  ```

### 6. Hospedar Backend Python
- [ ] Escolher plataforma (Render/Railway/Heroku/etc)
- [ ] Criar conta e conectar repositório
- [ ] Definir environment variables
- [ ] Fazer deploy
- [ ] Anotar URL final (exemplo: `https://seu-app.render.com`)

### 7. Configurar Netlify
- [ ] Instalar Netlify CLI:
  ```bash
  npm install -g netlify-cli
  ```

- [ ] Fazer login:
  ```bash
  netlify login
  ```

- [ ] Conectar repositório:
  ```bash
  netlify connect
  ```

- [ ] Atualizar `netlify.toml` com URLs reais:
  ```toml
  [[redirects]]
  from = "/api/*"
  to = "https://seu-backend-url.com/api/:splat"
  ```

- [ ] Definir variáveis de ambiente no Netlify Dashboard:
  - Settings → Build & Deploy → Environment
  - `REACT_APP_BACKEND_URL=https://seu-backend-url.com`

### 8. Testar Localmente
- [ ] Instalar dependências Node:
  ```bash
  npm install
  ```

- [ ] Rodar desenvolvimento local:
  ```bash
  netlify dev
  ```

- [ ] Testar em: `http://localhost:8888`

### 9. Deploy
- [ ] Push no GitHub (se usar)
  ```bash
  git add .
  git commit -m "Preparação para Netlify"
  git push origin main
  ```

- [ ] Fazer deploy no Netlify:
  ```bash
  netlify deploy --prod
  ```

## 📚 Documentação de Suporte

Crie estes arquivos adicionais se necessário:

- **AJAX_MIGRATION.md** - Como converter formulários tradicionais para AJAX
- **AUTHENTICATION.md** - Sistema de autenticação JWT
- **API_SPEC.md** - Documentação das APIs
- **DEPLOYMENT.md** - Instruções de deploy em produção

## 🔗 Links Rápidos

- [Netlify Docs](https://docs.netlify.com/)
- [Netlify CLI](https://docs.netlify.com/api-and-cli-guides/cli-guides/get-started-with-cli/)
- [Netlify Redirects](https://docs.netlify.com/manage/routing/redirects/)
- [Render.com Docs](https://render.com/docs) (para backend Python)
- [Flask-CORS](https://flask-cors.readthedocs.io/)

## ⚠️ Lembrar

- NÃO commitar `.env` no GitHub
- Frontend estático DEVE estar em `public/` ou ajustar `publish` em `netlify.toml`
- Backend Python roda em outro serviço, não no Netlify
- Usar HTTPS em produção (Netlify fornece automaticamente)
- CORS precisa estar configurado corretamente

---

**Prioridade**: Passos 1-4 são essenciais para começar.
