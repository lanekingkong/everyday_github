@echo off
chcp 65001 >nul
cd /d D:\claudecodework\everyday_github

echo.
echo ╔══════════════════════════════════════════════╗
echo ║  🚀 Everyday GitHub — 一键推送              ║
echo ╚══════════════════════════════════════════════╝
echo.
echo 目标: https://github.com/lanekingkong/everyday_github
echo.

REM Check connectivity
git ls-remote https://github.com/lanekingkong/everyday_github.git >nul 2>&1
if %errorlevel% neq 0 (
    echo [✗] 无法连接 GitHub，请先开启VPN/代理后重试！
    echo.
    pause
    exit /b 1
)

echo [✓] GitHub 连接正常
echo.
echo [→] 正在推送...
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ╔══════════════════════════════════════════════╗
    echo ║  ✅ 推送成功！                              ║
    echo ╚══════════════════════════════════════════════╝
    echo.
    echo 下一步:
    echo   1. 打开 https://github.com/lanekingkong/everyday_github/settings/actions
    echo   2. 确保 Actions 已启用
    echo   3. 手动触发一次 workflow 测试流水线
    echo.
) else (
    echo.
    echo [✗] 推送失败，请检查：
    echo   1. 仓库是否已在 GitHub 上创建
    echo   2. 仓库地址是否正确
    echo   3. VPN/代理是否正常工作
    echo.
)

pause
