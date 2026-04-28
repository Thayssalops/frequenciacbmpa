# Desenvolvimento Local com Netlify

## Instalação

```bash
# 1. Instalar Netlify CLI globalmente
npm install -g netlify-cli

# 2. Instalar dependências Node (para Netlify Functions)
npm install
```

## Executar Localmente

```bash
# Inicia o servidor de desenvolvimento
netlify dev

# Acessa em: http://localhost:8888
```

## Variáveis de Ambiente Local

Criar arquivo `.env` na raiz:

```env
REACT_APP_BACKEND_URL=http://localhost:5000
API_TIMEOUT=5000
```

O `netlify dev` carrega automaticamente do `.env`.

## Estrutura de Pastas - Desenvolvimento

```
gestao-interna-dtic/
├── public/              ← Arquivos estáticos (servidos como raiz)
│   ├── index.html
│   ├── css/
│   └── js/
├── netlify/
│   └── functions/       ← APIs serverless (TypeScript)
│       └── example.ts
├── netlify.toml         ← Configuração principal
├── .netlifyignore
├── .env                 ← Variáveis locais (não versionar)
└── package.json         ← Dependências Node
```

## Fluxo de Desenvolvimento

1. **Frontend estático**
   - Editar arquivos em `public/`
   - Refresh automático: `http://localhost:8888`

2. **APIs serverless (Node.js)**
   - Editar em `netlify/functions/`
   - Acessar em: `http://localhost:8888/.netlify/functions/example`
   - Hot reload automático

3. **Backend Python (Externo)**
   - Rodar em outro terminal: `python app.py`
   - Configurar URL no `.env`

## Testar APIs

### Função Netlify local
```bash
curl -X POST http://localhost:8888/.netlify/functions/example \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

### Backend Python (se rodando)
```bash
curl http://localhost:5000/api/dados \
  -H "Authorization: Bearer SEU_TOKEN"
```

## Deploy no Netlify

```bash
# Conectar ao Netlify
netlify login
netlify connect

# Deploy automático ao push
git push origin main

# Ou fazer deploy manual
netlify deploy --prod
```

## Monitoramento

- **Functions**: https://app.netlify.com → Site → Functions → Logs
- **Builds**: https://app.netlify.com → Site → Deploys
- **Performance**: https://app.netlify.com → Site → Analytics

## Links Úteis

- [Netlify Dev Docs](https://docs.netlify.com/cli/get-started/#run-a-local-development-environment)
- [Netlify Functions Guide](https://docs.netlify.com/functions/overview/)
- [Netlify CLI Reference](https://docs.netlify.com/api-and-cli-guides/cli-guides/get-started-with-cli/)
