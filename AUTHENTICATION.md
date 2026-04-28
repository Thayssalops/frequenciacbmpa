# Migração para Autenticação JWT

## Problema com Sessions

Seu código atual usa `flask.session` (cookie-based):
```python
if 'logged_in' not in session:
    return redirect(url_for('login'))
```

**Problema**: Sessions server-side não funcionam bem com frontend estático + backend em outro servidor.

## Solução: JWT (JSON Web Tokens)

JWT é stateless e ideal para arquitetura separada.

### Fluxo:

```
1. Login (Frontend → Backend)
   POST /api/login
   { "username": "...", "password": "..." }
   ↓
   Backend valida e retorna JWT token

2. Armazenar (Frontend)
   localStorage.setItem('token', token)

3. Requisição Autenticada (Frontend → Backend)
   GET /api/dados
   Header: Authorization: Bearer {token}
   ↓
   Backend valida JWT

4. Logout (Frontend)
   localStorage.removeItem('token')
```

---

## Implementação Backend (Python/Flask)

### 1. Instalar dependência
```bash
pip install PyJWT
```

### 2. Atualizar `app.py`

```python
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import jsonify

# Configuração
SECRET_KEY = os.getenv('SECRET_KEY', 'sua-chave-secreta-mudamojá')
JWT_EXPIRATION_HOURS = 24

# Função para gerar JWT
def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

# Decorator para validar JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Procurar token no header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token missing'}), 401
        
        try:
            # Validar e decodificar JWT
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.user_id = payload['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    
    return decorated

# Endpoint de login
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Validar credenciais
    if password != ADMIN_PASSWORD:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Gerar token
    token = generate_token(username)
    
    return jsonify({
        'token': token,
        'expires_in': JWT_EXPIRATION_HOURS * 3600
    }), 200

# Endpoint protegido
@app.route('/api/dados', methods=['GET'])
@token_required
def api_get_dados():
    # request.user_id contém o ID do usuário
    # Carregar dados...
    return jsonify({'data': []}), 200
```

---

## Implementação Frontend (JavaScript/HTML)

### 1. Login com AJAX

```html
<!-- login.html -->
<form id="loginForm">
  <input type="text" id="username" placeholder="Usuário" required />
  <input type="password" id="password" placeholder="Senha" required />
  <button type="submit">Login</button>
</form>

<script>
const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000';

document.getElementById('loginForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;
  
  try {
    const response = await fetch(`${API_URL}/api/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    
    if (!response.ok) {
      alert('Credenciais inválidas');
      return;
    }
    
    const data = await response.json();
    
    // Armazenar token
    localStorage.setItem('token', data.token);
    localStorage.setItem('token_expires', Date.now() + data.expires_in * 1000);
    
    // Redirecionar
    window.location.href = '/dashboard.html';
    
  } catch (error) {
    console.error('Erro:', error);
    alert('Erro no servidor');
  }
});
</script>
```

### 2. Requisições Autenticadas

```javascript
async function apiRequest(endpoint, options = {}) {
  const token = localStorage.getItem('token');
  
  if (!token) {
    window.location.href = '/login.html';
    return;
  }
  
  const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  };
  
  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers: { ...headers, ...options.headers }
  });
  
  if (response.status === 401) {
    // Token expirou
    localStorage.removeItem('token');
    window.location.href = '/login.html';
    return;
  }
  
  return response.json();
}

// Uso:
async function loadDados() {
  const data = await apiRequest('/api/dados');
  console.log(data);
}
```

### 3. Logout

```javascript
function logout() {
  localStorage.removeItem('token');
  localStorage.removeItem('token_expires');
  window.location.href = '/login.html';
}
```

### 4. Verificar se usuário está logado

```javascript
function isLoggedIn() {
  const token = localStorage.getItem('token');
  const expires = localStorage.getItem('token_expires');
  
  if (!token || !expires) {
    return false;
  }
  
  // Verificar se token expirou
  if (Date.now() > parseInt(expires)) {
    logout();
    return false;
  }
  
  return true;
}

// Proteger páginas
if (!isLoggedIn()) {
  window.location.href = '/login.html';
}
```

---

## Configurar CORS no Backend

```python
from flask_cors import CORS

CORS(app, 
     origins=[
         "https://seu-site.netlify.app",
         "http://localhost:8888",  # dev local
         "http://localhost:3000"    # dev frontend
     ],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"],
     expose_headers=["Content-Type"],
     supports_credentials=False  # JWT não precisa de credentials
)
```

---

## Variáveis de Ambiente

### Backend (.env)
```env
SECRET_KEY=sua-chave-super-secreta-de-produção-aqui
ADMIN_PASSWORD=senha-admin-segura
FLASK_ENV=production
```

### Frontend (.env)
```env
REACT_APP_BACKEND_URL=https://seu-backend.render.com
```

---

## Testes

### Testar login
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"sua-senha"}'
```

**Resposta:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 86400
}
```

### Usar token em requisição
```bash
TOKEN="seu-token-aqui"

curl -X GET http://localhost:5000/api/dados \
  -H "Authorization: Bearer $TOKEN"
```

---

## Checklist de Migração

- [ ] Instalar PyJWT no backend
- [ ] Adicionar funções JWT ao `app.py`
- [ ] Criar endpoint `/api/login`
- [ ] Converter rotas para usar `@token_required`
- [ ] Retornar JSON em vez de redirecionamentos
- [ ] Configurar CORS
- [ ] Atualizar templates para AJAX
- [ ] Adicionar JavaScript de autenticação
- [ ] Testar localmente
- [ ] Fazer deploy

---

## Referências

- [JWT.io](https://jwt.io/)
- [PyJWT Docs](https://pyjwt.readthedocs.io/)
- [Flask-CORS](https://flask-cors.readthedocs.io/)
- [MDN: HTTP Authentication](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication)
