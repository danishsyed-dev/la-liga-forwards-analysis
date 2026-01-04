#!/bin/bash
# La Liga Forwards Analysis - Unix Launcher
# ==========================================

echo ""
echo "  ⚽ La Liga Forwards Analysis"
echo "  ============================"
echo ""
echo "  🚀 Starting web application..."
echo "  📊 Dashboard will open in your default browser"
echo "  🔗 URL: http://localhost:8501"
echo ""
echo "  Press Ctrl+C to stop the server"
echo ""

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "  ❌ Streamlit not found. Installing dependencies..."
    pip install -r requirements.txt
fi

# Run the app
streamlit run app.py
