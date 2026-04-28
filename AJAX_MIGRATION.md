# Migração de Formulários para AJAX

## Problema

Formulários HTML tradicionais (`<form method="POST">`) não funcionam bem com:
- Frontend estático (Netlify)
- Backend em outro servidor (Render, Railway, etc)
- Autenticação JWT

## Solução: AJAX + JSON

Converter formulários tradicionales para requisições AJAX.

---

## Exemplo 1: Login

### Antes (Form tradicional - ❌ Não funciona)
```html
<form method="POST" action="/login">
  <input type="text" name="username" required />
  <input type="password" name="password" required />
  <button type="submit">Login</button>
</form>
```

### Depois (AJAX - ✅ Funciona)
```html
<form id="loginForm">
  <input type="text" id="username" placeholder="Usuário" required />
  <input type="password" id="password" placeholder="Senha" required />
  <button type="submit">Login</button>
  <div id="error" style="color: red; display: none;"></div>
</form>

<script>
const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000';

document.getElementById('loginForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;
  const errorDiv = document.getElementById('error');
  
  try {
    errorDiv.style.display = 'none';
    
    const response = await fetch(`${API_URL}/api/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ username, password })
    });
    
    if (!response.ok) {
      const error = await response.json();
      errorDiv.textContent = error.error || 'Erro no login';
      errorDiv.style.display = 'block';
      return;
    }
    
    const data = await response.json();
    
    // Armazenar token
    localStorage.setItem('token', data.token);
    
    // Redirecionar
    window.location.href = '/dashboard.html';
    
  } catch (error) {
    errorDiv.textContent = 'Erro de conexão com servidor';
    errorDiv.style.display = 'block';
  }
});
</script>
```

---

## Exemplo 2: CRUD (Criar/Ler/Atualizar/Deletar)

### Antes (❌)
```html
<!-- Formulário tradicional -->
<form method="POST" action="/voluntarios/add">
  <input type="text" name="nome" required />
  <input type="email" name="email" required />
  <button type="submit">Adicionar</button>
</form>

<!-- Tabela com links delete -->
<table>
  <tr>
    <td>João</td>
    <td><a href="/voluntarios/delete/1">Deletar</a></td>
  </tr>
</table>
```

### Depois (✅)
```html
<!-- Formulário AJAX -->
<form id="voluntarioForm">
  <input type="text" id="nome" placeholder="Nome" required />
  <input type="email" id="email" placeholder="Email" required />
  <button type="submit">Adicionar</button>
  <div id="formMessage"></div>
</form>

<table id="voluntariosTable">
  <thead>
    <tr><th>Nome</th><th>Email</th><th>Ação</th></tr>
  </thead>
  <tbody></tbody>
</table>

<script>
const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000';

// Helper para requisições autenticadas
async function apiRequest(endpoint, options = {}) {
  const token = localStorage.getItem('token');
  
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers
  };
  
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  
  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers
  });
  
  if (response.status === 401) {
    window.location.href = '/login.html';
    return;
  }
  
  return response;
}

// Carregar voluntários
async function loadVoluntarios() {
  try {
    const response = await apiRequest('/api/voluntarios');
    const data = await response.json();
    
    const tbody = document.querySelector('#voluntariosTable tbody');
    tbody.innerHTML = '';
    
    data.voluntarios.forEach(vol => {
      const row = tbody.insertRow();
      row.innerHTML = `
        <td>${vol.nome}</td>
        <td>${vol.email}</td>
        <td>
          <button onclick="deleteVoluntario(${vol.id})">Deletar</button>
          <button onclick="editVoluntario(${vol.id})">Editar</button>
        </td>
      `;
    });
  } catch (error) {
    console.error('Erro ao carregar:', error);
  }
}

// Adicionar voluntário
document.getElementById('voluntarioForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const nome = document.getElementById('nome').value;
  const email = document.getElementById('email').value;
  const message = document.getElementById('formMessage');
  
  try {
    const response = await apiRequest('/api/voluntarios', {
      method: 'POST',
      body: JSON.stringify({ nome, email })
    });
    
    if (response.ok) {
      message.textContent = 'Adicionado com sucesso!';
      message.style.color = 'green';
      document.getElementById('voluntarioForm').reset();
      loadVoluntarios();
      
      setTimeout(() => {
        message.textContent = '';
      }, 3000);
    } else {
      const error = await response.json();
      message.textContent = error.error || 'Erro ao adicionar';
      message.style.color = 'red';
    }
  } catch (error) {
    message.textContent = 'Erro de conexão';
    message.style.color = 'red';
  }
});

// Deletar voluntário
async function deleteVoluntario(id) {
  if (!confirm('Tem certeza?')) return;
  
  try {
    const response = await apiRequest(`/api/voluntarios/${id}`, {
      method: 'DELETE'
    });
    
    if (response.ok) {
      loadVoluntarios();
    } else {
      alert('Erro ao deletar');
    }
  } catch (error) {
    alert('Erro de conexão');
  }
}

// Editar voluntário
async function editVoluntario(id) {
  const nome = prompt('Novo nome:');
  if (!nome) return;
  
  try {
    const response = await apiRequest(`/api/voluntarios/${id}`, {
      method: 'PUT',
      body: JSON.stringify({ nome })
    });
    
    if (response.ok) {
      loadVoluntarios();
    } else {
      alert('Erro ao editar');
    }
  } catch (error) {
    alert('Erro de conexão');
  }
}

// Carregar ao abrir página
if (localStorage.getItem('token')) {
  loadVoluntarios();
} else {
  window.location.href = '/login.html';
}
</script>
```

---

## Padrões Úteis

### 1. Mostrar carregamento
```javascript
const loading = document.getElementById('loading');

loading.style.display = 'block';
try {
  // ... requisição ...
} finally {
  loading.style.display = 'none';
}
```

### 2. Validar antes de enviar
```javascript
function validateForm(data) {
  if (!data.nome || data.nome.trim() === '') {
    return 'Nome é obrigatório';
  }
  if (!data.email || !data.email.includes('@')) {
    return 'Email inválido';
  }
  return null;
}

const error = validateForm({ nome, email });
if (error) {
  alert(error);
  return;
}
```

### 3. Tratamento de erro global
```javascript
async function apiRequest(endpoint, options = {}) {
  const token = localStorage.getItem('token');
  
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers
  };
  
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  
  try {
    const response = await fetch(`${API_URL}${endpoint}`, {
      ...options,
      headers
    });
    
    // Tratamento de erros
    if (response.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login.html';
      return null;
    }
    
    if (response.status === 400) {
      const data = await response.json();
      throw new Error(data.error || 'Erro na requisição');
    }
    
    if (response.status === 500) {
      throw new Error('Erro no servidor');
    }
    
    return response;
    
  } catch (error) {
    console.error('Request failed:', error);
    throw error;
  }
}
```

### 4. Debounce para requisições frequentes
```javascript
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// Uso: busca enquanto digita
const handleSearch = debounce(async (query) => {
  const response = await apiRequest(`/api/search?q=${query}`);
  // ... processar resultado ...
}, 300);

document.getElementById('searchInput').addEventListener('input', (e) => {
  handleSearch(e.target.value);
});
```

---

## Checklist de Migração

Para cada formulário/endpoint:

- [ ] Identificar action e method do form
- [ ] Criar função AJAX equivalente
- [ ] Remover `<form method="...">` e usar `<form id="...">`
- [ ] Adicionar `e.preventDefault()` no submit
- [ ] Usar `JSON.stringify()` para enviar dados
- [ ] Validar response (status, JSON)
- [ ] Atualizar UI com resultado
- [ ] Tratar erros com feedback ao usuário
- [ ] Testar autenticação (JWT)

---

## Exemplo Completo: Sistema de Folhas

```html
<!-- folhas.html -->
<!DOCTYPE html>
<html>
<head>
  <title>Folhas</title>
  <style>
    button { padding: 8px 16px; margin: 5px; cursor: pointer; }
    .loading { display: none; }
    .error { color: red; }
    .success { color: green; }
  </style>
</head>
<body>
  <h1>Gestão de Folhas</h1>
  
  <button onclick="exportFolha('civil')">Exportar Folha Civil</button>
  <button onclick="exportFolha('militar')">Exportar Folha Militar</button>
  
  <div id="loading" class="loading">Processando...</div>
  <div id="message"></div>
  
  <script>
    const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000';
    
    async function apiRequest(endpoint, options = {}) {
      const token = localStorage.getItem('token');
      const headers = { ...options.headers };
      if (token) headers['Authorization'] = `Bearer ${token}`;
      
      return fetch(`${API_URL}${endpoint}`, {
        ...options,
        headers
      });
    }
    
    async function exportFolha(type) {
      const loading = document.getElementById('loading');
      const message = document.getElementById('message');
      
      try {
        loading.style.display = 'block';
        message.textContent = '';
        
        const response = await apiRequest(`/api/folhas/export/${type}`);
        
        if (!response.ok) {
          throw new Error('Erro ao exportar');
        }
        
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `folha_${type}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        
        message.textContent = 'Arquivo baixado com sucesso!';
        message.className = 'success';
        
      } catch (error) {
        message.textContent = error.message;
        message.className = 'error';
      } finally {
        loading.style.display = 'none';
      }
    }
    
    // Proteger página
    if (!localStorage.getItem('token')) {
      window.location.href = '/login.html';
    }
  </script>
</body>
</html>
```

---

## Dicas Finais

1. **Teste com CORS** - use `curl` ou Postman primeiro
2. **Valide no backend** - nunca confie em dados do frontend
3. **Proteja dados sensíveis** - use HTTPS sempre
4. **Feedback ao usuário** - sempre mostre loading, sucesso ou erro
5. **Trate timeouts** - requisições podem falhar
