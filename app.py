from flask import Flask, render_template, request, redirect, url_for, session, flash
from dotenv import load_dotenv
from functools import wraps
import json
import os
import re
import calendar
from datetime import datetime, timedelta, date
import locale
import time
from markupsafe import Markup, escape

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração de Caminhos Absolutos
basedir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(basedir, 'templates')
static_dir = os.path.join(basedir, 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

DB_CIVIL = os.path.join(basedir, 'voluntarios.json')
DB_MILITAR = os.path.join(basedir, 'militares.json')

# Chave secreta para gerenciamento de sessão
app.config['SECRET_KEY'] = os.urandom(24)
# Configurar tempo de sessão (5 minutos)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')



# Tenta configurar local para PT-BR
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
except:
    try:
        locale.setlocale(locale.LC_ALL, 'pt_BR') 
    except:
        pass 

# Decorator para exigir login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        # Verifica se a sessão expirou (5 minutos = 300 segundos)
        if 'session_start' in session:
            if time.time() - session['session_start'] > 300:
                session.clear()
                flash('Sua sessão expirou. Faça login novamente.')
                return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Manipulador de erro 403
@app.errorhandler(403)
def forbidden_error(error):
    flash('Acesso negado. Redirecionando para home.')
    return redirect(url_for('home'))

# Manipulador de erro 404
@app.errorhandler(404)
def not_found_error(error):
    flash('Página não encontrada.')
    return redirect(url_for('home'))

# --- FUNÇÕES DE BANCO DE DADOS ---
def load_json(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def _to_upper(value):
    return (value or "").strip().upper()

def _highlight_nome_guerra(nome, nome_guerra):
    nome = (nome or "").strip()
    nome_guerra = (nome_guerra or "").strip()

    if not nome:
        return Markup("")
    if not nome_guerra:
        return escape(nome)

    # 1) Se a expressão completa existir no nome, destaca de uma vez.
    match_full = re.search(re.escape(nome_guerra), nome, flags=re.IGNORECASE)
    if match_full:
        ini, fim = match_full.span()
        return Markup(f"{escape(nome[:ini])}<b>{escape(nome[ini:fim])}</b>{escape(nome[fim:])}")

    # 2) Se não for contíguo (ex.: 'FÁBIO CRUZ' em 'FÁBIO REIS DA CRUZ'),
    # destaca cada token encontrado.
    tokens = re.findall(r"[A-ZÀ-Ý0-9]+", nome_guerra.upper())
    tokens = sorted({t for t in tokens if len(t) >= 2}, key=len, reverse=True)
    if not tokens:
        return escape(nome)

    spans = []
    for token in tokens:
        pattern = rf"(?<!\w){re.escape(token)}(?!\w)"
        for m in re.finditer(pattern, nome, flags=re.IGNORECASE):
            spans.append(m.span())

    if not spans:
        return escape(nome)

    spans.sort(key=lambda x: (x[0], -(x[1] - x[0])))
    merged = []
    for ini, fim in spans:
        if not merged or ini >= merged[-1][1]:
            merged.append([ini, fim])

    out = []
    last = 0
    for ini, fim in merged:
        out.append(escape(nome[last:ini]))
        out.append(Markup(f"<b>{escape(nome[ini:fim])}</b>"))
        last = fim
    out.append(escape(nome[last:]))
    return Markup("").join(out)
app.jinja_env.filters['highlight_nome_guerra'] = _highlight_nome_guerra

# --- ROTAS PRINCIPAIS ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['password'] == ADMIN_PASSWORD:
            session.permanent = True
            session['logged_in'] = True
            session['session_start'] = time.time()
            flash('Login realizado com sucesso!')
            return redirect(url_for('home'))
        else:
            error = 'Senha inválida. Tente novamente.'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Você foi desconectado.')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def home():
    # 1. Carrega os dois bancos de dados (Civil e Militar)
    # Se der erro aqui, verifique se definiu DB_CIVIL e DB_MILITAR lá em cima
    civis = load_json(DB_CIVIL)       
    militares = load_json(DB_MILITAR) 
    
    # 2. Configura os dados padrão (ISSO CORRIGE O ERRO 'padrao undefined')
    agora = datetime.now()
    ultimo_dia = calendar.monthrange(agora.year, agora.month)[1]
    
    dados_padrao = {
        "nota_num": "001",
        "dia_inicio": "01",
        "dia_fim": str(ultimo_dia), 
        "comandante": "EMANUEL LOBATO RODRIGUES – 2° TEN QOABM",
        "nome_guerra_comandante": "L RODRIGUES",
        "ano_atual": agora.year,
        "mes_atual": agora.month
    }
    
    # 3. Envia tudo para o HTML com os nomes corretos
    return render_template(
        'index.html', 
        civis=civis,          # O HTML novo espera 'civis' (não 'voluntarios')
        militares=militares,  # O HTML novo espera 'militares'
        padrao=dados_padrao   # <--- AQUI ESTÁ A CORREÇÃO PRINCIPAL
    )

# --- CRUD CIVIL (Mantido) ---
@app.route('/add_civil', methods=['POST'])
@login_required
def add_civil():
    data = load_json(DB_CIVIL)
    novo_id = max([v.get('id', 0) for v in data if isinstance(v, dict)] + [0]) + 1
    novo = {
        "id": novo_id,
        "nome": _to_upper(request.form.get('nome')),
        "nome_guerra": _to_upper(request.form.get('nome_guerra')),
        "funcao": (request.form.get('funcao') or "").strip(),
        "turno": (request.form.get('turno') or "").strip()
    }
    data.append(novo)
    save_json(DB_CIVIL, data)
    return redirect(url_for('home'))

@app.route('/del_civil/<int:id>')
@login_required
def del_civil(id):
    data = load_json(DB_CIVIL)
    data = [v for v in data if v.get('id') != id]
    save_json(DB_CIVIL, data)
    return redirect(url_for('home'))

# --- CRUD MILITAR (Novo) ---
@app.route('/add_militar', methods=['POST'])
@login_required
def add_militar():
    data = load_json(DB_MILITAR)
    novo_id = max([v.get('id', 0) for v in data if isinstance(v, dict)] + [0]) + 1
    novo = {
        "id": novo_id,
        "graduacao": _to_upper(request.form.get('graduacao')),
        "nome": _to_upper(request.form.get('nome')),
        "nome_guerra": _to_upper(request.form.get('nome_guerra'))
    }
    data.append(novo)
    save_json(DB_MILITAR, data)
    return redirect(url_for('home'))

@app.route('/del_militar/<int:id>')
@login_required
def del_militar(id):
    data = load_json(DB_MILITAR)
    data = [v for v in data if v.get('id') != id]
    save_json(DB_MILITAR, data)
    return redirect(url_for('home'))

# --- GERAÇÃO DE FOLHAS ---
def _generate_dias_data(year, month):
    agora = datetime(year, month, 1) # Use the provided year and month
    _, num_dias_mes = calendar.monthrange(year, month)

    dias = []
    for d in range(1, 32): # Table fixed to 31 rows generally
        if d > num_dias_mes:
            dias.append({"numero": d, "tipo": "nulo", "texto": ""})
            continue

        dt = datetime(year, month, d)
        weekday = dt.weekday()

        tipo = "dia_util"
        texto = ""

        if weekday == 5:
            tipo = "sabado"
            texto = "SÁBADO"
        elif weekday == 6:
            tipo = "domingo"
            texto = "DOMINGO"

        dias.append({"numero": f"{d:02d}", "tipo": tipo, "texto": texto})
    return dias

def _easter_sunday(year):
    """Computa a data do domingo de Páscoa (algoritmo de Meeus/Jones/Butcher)."""
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return date(year, month, day)

def _get_feriados_brasil(year):
    """Retorna conjunto de datas de feriados nacionais no Brasil."""
    pascoa = _easter_sunday(year)
    return {
        date(year, 1, 1),    # Confraternização Universal
        date(year, 4, 21),   # Tiradentes
        date(year, 5, 1),    # Dia do Trabalhador
        date(year, 9, 7),    # Independência do Brasil
        date(year, 10, 12),  # Nossa Senhora Aparecida
        date(year, 11, 2),   # Finados
        date(year, 11, 15),  # Proclamação da República
        date(year, 11, 20),  # Dia da Consciência Negra
        date(year, 12, 25),  # Natal
        pascoa - timedelta(days=47),  # Carnaval (terça)
        pascoa - timedelta(days=2),   # Sexta-feira Santa
        pascoa + timedelta(days=60),  # Corpus Christi
    }


@app.route('/gerar_civil')
@login_required
def gerar_civil():
    voluntarios = load_json(DB_CIVIL)
    comandante = request.args.get('comandante', 'EMANUEL L OBATO RODRIGUES – 2° TEN QOABM')
    nome_guerra_comandante = request.args.get('nome_guerra_comandante', 'L RODRIGUES')
    
    agora = datetime.now()
    try:
        mes_selecionado = int(request.args.get('mes', agora.month))
        ano_selecionado = int(request.args.get('ano', agora.year))
    except ValueError:
        mes_selecionado = agora.month
        ano_selecionado = agora.year
    mes_nome = calendar.month_name[mes_selecionado].upper()
    _, num_dias = calendar.monthrange(ano_selecionado, mes_selecionado)
    
    feriados = _get_feriados_brasil(ano_selecionado)
    dias = []
    for d in range(1, num_dias + 1):
        dt = datetime(ano_selecionado, mes_selecionado, d)
        data_atual = date(ano_selecionado, mes_selecionado, d)
        is_fim_de_semana = dt.weekday() >= 5
        is_feriado = data_atual in feriados

        texto = ""
        if is_feriado:
            texto = "FERIADO"
        elif dt.weekday() == 5:
            texto = "SÁBADO"
        elif dt.weekday() == 6:
            texto = "DOMINGO"

        dias.append({
            "numero": d,
            "is_fim_de_semana": is_fim_de_semana, # 5=Sáb, 6=Dom
            "is_feriado": is_feriado,
            "texto": texto
        })
        
    return render_template('folha_civil.html', 
                           voluntarios=voluntarios, 
                           mes=mes_nome, 
                           ano=ano_selecionado, 
                           dias=dias, 
                           comandante=comandante,
                           nome_guerra_comandante=nome_guerra_comandante)

@app.route('/gerar_militar')
@login_required
def gerar_militar():
    militares = load_json(DB_MILITAR)
    nota_num = request.args.get('nota_num', '001')
    
    # 1. Detecta Data Atual
    agora = datetime.now()
    
    # 2. Configura Mês e Último Dia Real (ex: Fev = 28)
    # locale já foi configurado no início do script, então month_name vem em PT ou Inglês dependendo do sistema
    # Vamos garantir UPPERCASE
    mes_nome = calendar.month_name[agora.month].upper()
    _, ultimo_dia = calendar.monthrange(agora.year, agora.month)
    
    # 3. Textos
    periodo_str = f"01 A {ultimo_dia:02d} DE {mes_nome} DE {agora.year}"
    nota_str = f"{nota_num}/{agora.year}"

    # 4. Gera dias DINÂMICOS (Só vai até o último dia do mês, igual ao Civil)
    dias = []
    for d in range(1, ultimo_dia + 1):
        dt = datetime(agora.year, agora.month, d)
        weekday = dt.weekday() # 0=Seg, 5=Sáb, 6=Dom
        
        tipo = "dia_util"
        texto = ""
        
        if weekday == 5:
            tipo = "sabado"
            texto = "SÁBADO"
        elif weekday == 6:
            tipo = "domingo"
            texto = "DOMINGO"
            
        dias.append({"numero": f"{d:02d}", "tipo": tipo, "texto": texto})

    return render_template('folha_militar.html',
                           militares=militares,
                           nota=nota_str,
                           periodo=periodo_str,
                           dias=dias)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)