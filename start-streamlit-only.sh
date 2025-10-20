#!/bin/bash

# CV2Profile - Nur Streamlit starten (minimale Version)

echo "🚀 Starte CV2Profile (Streamlit only)..."
echo ""

# Beende alte Prozesse
pkill -f "streamlit" 2>/dev/null
sleep 1

# Prüfe .env
if [ ! -f .env ]; then
    echo "⚠️  Tipp: Erstelle .env mit OPENAI_API_KEY für automatisches Laden"
    echo ""
fi

# Starte Streamlit
echo "📱 Starte Streamlit App auf http://localhost:8501"
echo ""
echo "Drücke Ctrl+C zum Beenden..."
echo ""

python3 run_streamlit.py

