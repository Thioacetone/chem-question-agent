@echo off
chcp 65001 >nul
echo ========================================
echo   高考有机化学命题Agent - 启动脚本
echo ========================================
echo.

REM 检查API Key
if "%DEEPSEEK_API_KEY%"=="" (
    echo [警告] 未设置 DEEPSEEK_API_KEY 环境变量
    echo.
    set /p API_KEY="请输入DeepSeek API Key: "
    set DEEPSEEK_API_KEY=!API_KEY!
    echo.
)

echo [启动] 后端服务 (端口 8000)...
start "命题Agent后端" cmd /c "cd /d "%~dp0backend" && python main.py"

echo [启动] 前端服务 (端口 3000)...
start "命题Agent前端" cmd /c "cd /d "%~dp0frontend" && npm run dev"

echo.
echo ========================================
echo   启动完成！
echo   后端: http://localhost:8000
echo   前端: http://localhost:3000
echo ========================================
echo.
pause