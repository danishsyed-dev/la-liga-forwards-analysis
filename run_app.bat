@echo off
REM La Liga Forwards Analysis - Windows Launcher
REM ==============================================

echo.
echo  ⚽ La Liga Forwards Analysis
echo  ============================
echo.
echo  🚀 Starting web application...
echo  📊 Dashboard will open in your default browser
echo  🔗 URL: http://localhost:8501
echo.
echo  Press Ctrl+C to stop the server
echo.

REM Check if streamlit is installed
where streamlit >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo  ❌ Streamlit not found. Installing dependencies...
    pip install -r requirements.txt
)

REM Run the app
streamlit run app.py
