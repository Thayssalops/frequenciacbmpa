# Gestão Interna DTIC - Pronto para Netlify

Projeto preparado para hospedagem em **Netlify** (frontend estático) + **Render.com** (backend Python).

---

## 📦 Documentação

Leia na ordem:

1. **[NETLIFY_GUIDE.md](./NETLIFY_GUIDE.md)** - Visão geral e arquitetura
2. **[CHECKLIST.md](./CHECKLIST.md)** - Próximos passos (prioridade!)
3. **[DEVELOPMENT.md](./DEVELOPMENT.md)** - Desenvolvimento local
4. **[AUTHENTICATION.md](./AUTHENTICATION.md)** - Migrar para JWT
5. **[AJAX_MIGRATION.md](./AJAX_MIGRATION.md)** - Converter formulários
6. **[DEPLOYMENT_RENDER.md](./DEPLOYMENT_RENDER.md)** - Hospedar backend

---

## 🚀 Quick Start (2 minutos)

```bash
# 1. Instalar Netlify CLI
npm install -g netlify-cli

# 2. Instalar dependências
npm install

# 3. Desenvolvimento local
netlify dev

# Acessa em: http://localhost:8888
```

---

## 📋 Status da Preparação

✅ **Já Feito:**
- `netlify.toml` - Configuração Netlify
- `.netlifyignore` - Arquivos a ignorar
- `package.json` - Dependências Node
- Estrutura Netlify Functions criada
- 6 guias de implementação completos

⚠️ **Falta Fazer:**
1. Separar código Python para `backend/`
2. Refatorar templates HTML para AJAX
3. Implementar autenticação JWT
4. Configurar CORS
5. Deploy backend em Render.com
6. Deploy frontend em Netlify

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────┐
│         Navegador do Usuário                │
└────────────────┬────────────────────────────┘
                 │
        ┌────────┴─────────┐
        │                  │
┌───────▼─────────┐    ┌──▼──────────────┐
│  Frontend       │    │   Backend       │
│  (Netlify)      │    │   (Render.com)  │
│                 │    │                 │
│ • HTML/CSS/JS   │◄──►│ • Flask Python  │
│ • AJAX/Fetch    │    │ • JWT auth      │
│ • SPA            │    │ • JSON files    │
└─────────────────┘    └─────────────────┘
  https://seu        https://seu-api
  -site.netlify      .onrender.com
  .app
```

---

## 🔑 Principais Mudanças

### 1. **Arquitetura Separada**
   - Frontend: site estático no Netlify
   - Backend: Python em container no Render

### 2. **Autenticação JWT** (não sessions)
   - Mais simples para arquitetura distribuída
   - Ver: [AUTHENTICATION.md](./AUTHENTICATION.md)

### 3. **API REST + CORS**
   - Comunicação via JSON
   - Endpoints `/api/*`
   - CORS configurado

### 4. **Requisições AJAX** (não form submits)
   - Frontend envia JSON via `fetch()`
   - Backend retorna JSON
   - Feedback em tempo real

---

## 📁 Estrutura Final (após preparação)

```
gestao-interna-dtic/
├── public/                    ← Frontend estático
│   ├── index.html
│   ├── login.html
│   ├── dashboard.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── api.js
│       └── app.js
│
├── backend/                   ← Backend Python
│   ├── app.py                 (com JWT, CORS)
│   ├── requirements.txt        (PyJWT, Flask-CORS)
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── militares.json
│   └── voluntarios.json
│
├── netlify/                   ← Netlify Functions (opcional)
│   └── functions/
│       └── example.ts
│
├── netlify.toml               ✅ Pronto
├── .netlifyignore             ✅ Pronto
├── package.json               ✅ Pronto
├── NETLIFY_GUIDE.md           ✅ Pronto
├── CHECKLIST.md               ✅ Pronto
├── DEVELOPMENT.md             ✅ Pronto
├── AUTHENTICATION.md          ✅ Pronto
├── AJAX_MIGRATION.md          ✅ Pronto
├── DEPLOYMENT_RENDER.md       ✅ Pronto
└── README.md
```

---

## 🔄 Fluxo de Deploy

```
1. Desenvolvimento Local
   └─ netlify dev

2. Separar Backend
   └─ mkdir backend
   └─ mover Python files

3. Refatorar Frontend
   └─ converter formulários para AJAX
   └─ implementar JWT

4. Deploy Backend (Render)
   └─ git push
   └─ Render deploy automático
   └─ Obter URL: https://meu-api.onrender.com

5. Configurar Netlify
   └─ Adicionar URL backend em netlify.toml
   └─ Definir variáveis de ambiente

6. Deploy Frontend (Netlify)
   └─ git push
   └─ Netlify deploy automático
   └─ Site online: https://meu-site.netlify.app
```

---

## 📚 Próximos Passos

### Imediato (Hoje)
- [ ] Ler [CHECKLIST.md](./CHECKLIST.md)
- [ ] Ler [AUTHENTICATION.md](./AUTHENTICATION.md)
- [ ] Ler [AJAX_MIGRATION.md](./AJAX_MIGRATION.md)

### Curto Prazo (Esta semana)
- [ ] Separar `backend/` e `public/`
- [ ] Implementar JWT no `app.py`
- [ ] Converter 1 formulário para AJAX
- [ ] Testar localmente com `netlify dev`

### Médio Prazo (Próxima semana)
- [ ] Criar conta Render.com
- [ ] Deploy backend
- [ ] Obter URL final
- [ ] Deploy frontend Netlify
- [ ] Testar integração

### Longo Prazo
- [ ] Monitorar performance
- [ ] Adicionar CI/CD automático
- [ ] Escalar conforme demanda

---

## 🆘 Dúvidas Frequentes

### Q: Netlify não suporta Python?
**A:** Correto. Netlify é para front-end estático. Python roda em outro servidor (Render, etc).

### Q: Quanto custa?
**A:** 
- Netlify: Free tier generoso
- Render: Free (com sleep) ou $7/mês (recomendado)

### Q: Preciso reescrever tudo?
**A:** Não. Apenas separar frontend/backend e converter formulários para AJAX.

### Q: E o banco de dados JSON?
**A:** Funciona. Usar Render.com para hospedar backend com arquivos JSON. Considerar SQLite/PostgreSQL após crescimento.

### Q: Como fazer CORS?
**A:** Ver [AUTHENTICATION.md](./AUTHENTICATION.md#configurar-cors-no-backend)

---

## 🔗 Links Úteis

### Documentação Oficial
- [Netlify Docs](https://docs.netlify.com/)
- [Render Docs](https://render.com/docs)
- [Flask-CORS](https://flask-cors.readthedocs.io/)
- [PyJWT](https://pyjwt.readthedocs.io/)

### Ferramentas
- [Netlify CLI](https://docs.netlify.com/cli/get-started/)
- [Postman (testar APIs)](https://www.postman.com/)
- [cURL (testar via terminal)](https://curl.se/)

### Tutoriais
- [JWT Explicado](https://jwt.io/introduction)
- [CORS Explicado](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)

---

## 📞 Suporte

Se tiver dúvidas durante a implementação:

1. Consulte o guia correspondente
2. Verifique os links na seção de documentação
3. Teste localmente com `netlify dev`
4. Veja os logs: Render Dashboard → Logs

---

**Versão:** 1.0  
**Última atualização:** Abril 2026  
**Baseado em:** [docs.netlify.com](https://docs.netlify.com/)
