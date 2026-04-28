@echo off
REM Script para fazer push das mudanças para Netlify
REM Executar em PowerShell ou CMD

cd /d "%~dp0"

echo ===== Git Push para Netlify =====
echo.

REM Adicionar arquivos
git add .
if errorlevel 1 (
    echo Erro: Git não encontrado. Instale Git em: https://git-scm.com/download/win
    pause
    exit /b 1
)

REM Fazer commit
git commit -m "Fix: Corrigir estrutura de arquivos para Netlify (404 resolvido)"

REM Push
git push origin main
if errorlevel 1 (
    echo Erro ao fazer push. Verifique sua conexão ou credenciais Git.
    pause
    exit /b 1
)

echo.
echo ===== Push concluído! =====
echo Netlify vai fazer deploy automaticamente em alguns minutos.
echo Monitore em: https://app.netlify.com
echo.
pause
