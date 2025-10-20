#!/bin/bash

# CV2Profile - Stop Skript
# Beendet alle laufenden Services

echo "🛑 Beende CV2Profile Services..."
echo ""

# Beende Streamlit
if pgrep -f "streamlit" > /dev/null; then
    echo "⏹️  Beende Streamlit..."
    pkill -f "streamlit"
fi

# Beende FastAPI/Uvicorn
if pgrep -f "uvicorn" > /dev/null; then
    echo "⏹️  Beende FastAPI Backend..."
    pkill -f "uvicorn"
fi

# Beende Python Run-Skripte
if pgrep -f "run_streamlit.py" > /dev/null; then
    pkill -f "run_streamlit.py"
fi

if pgrep -f "run_backend.py" > /dev/null; then
    pkill -f "run_backend.py"
fi

sleep 1

echo ""
echo "✅ Alle Services beendet!"
echo ""

