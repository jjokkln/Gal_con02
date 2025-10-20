#!/bin/bash

# CV2Profile - Automatisches Startskript
# Startet Streamlit App und FastAPI Backend

echo "================================================="
echo "🚀 CV2Profile wird gestartet..."
echo "================================================="
echo ""

# Farben für Output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Prüfe ob .env existiert
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  Warnung: .env Datei nicht gefunden!${NC}"
    echo "   Bitte erstelle eine .env Datei mit deinem OpenAI API Key."
    echo "   Beispiel: OPENAI_API_KEY=sk-your-key-here"
    echo ""
fi

# Prüfe ob Python installiert ist
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 ist nicht installiert!"
    echo "   Bitte installiere Python 3.9 oder höher."
    exit 1
fi

# Prüfe ob Dependencies installiert sind
echo "📦 Prüfe Python Dependencies..."
if ! python3 -c "import streamlit" &> /dev/null; then
    echo -e "${YELLOW}⚠️  Dependencies fehlen. Installiere...${NC}"
    python3 -m pip install -r backend/requirements.txt
fi

echo ""
echo "================================================="
echo "🔧 Starte Services..."
echo "================================================="
echo ""

# Beende alte Prozesse
echo "🧹 Beende alte Prozesse..."
pkill -f "streamlit" 2>/dev/null
pkill -f "uvicorn" 2>/dev/null
sleep 1

# Starte Streamlit im Hintergrund
echo -e "${BLUE}📱 Starte Streamlit App...${NC}"
python3 run_streamlit.py > /dev/null 2>&1 &
STREAMLIT_PID=$!
echo "   PID: $STREAMLIT_PID"

# Warte kurz
sleep 3

# Starte FastAPI Backend im Hintergrund
echo -e "${BLUE}⚙️  Starte FastAPI Backend...${NC}"
python3 run_backend.py > /dev/null 2>&1 &
BACKEND_PID=$!
echo "   PID: $BACKEND_PID"

# Warte bis Services bereit sind
echo ""
echo "⏳ Warte auf Services..."
sleep 5

# Prüfe ob Services laufen
STREAMLIT_RUNNING=0
BACKEND_RUNNING=0

if curl -s http://localhost:8501 > /dev/null 2>&1; then
    STREAMLIT_RUNNING=1
fi

if curl -s http://localhost:8000 > /dev/null 2>&1; then
    BACKEND_RUNNING=1
fi

echo ""
echo "================================================="
echo "📊 Status"
echo "================================================="
echo ""

if [ $STREAMLIT_RUNNING -eq 1 ]; then
    echo -e "${GREEN}✅ Streamlit App:  http://localhost:8501${NC}"
else
    echo -e "❌ Streamlit App:  Fehler beim Start"
fi

if [ $BACKEND_RUNNING -eq 1 ]; then
    echo -e "${GREEN}✅ FastAPI Backend: http://localhost:8000${NC}"
else
    echo -e "${YELLOW}⚠️  FastAPI Backend: http://localhost:8000 (optional)${NC}"
fi

echo ""
echo "================================================="
echo "📝 Hinweise"
echo "================================================="
echo ""
echo "• Öffne: http://localhost:8501 im Browser"
echo "• API Key: Prüfe .env Datei oder gib in App ein"
echo "• Stoppen: Drücke Ctrl+C oder führe ./stop.sh aus"
echo ""
echo "================================================="
echo ""

# Funktion zum Beenden beim Exit
cleanup() {
    echo ""
    echo "🛑 Beende Services..."
    kill $STREAMLIT_PID 2>/dev/null
    kill $BACKEND_PID 2>/dev/null
    pkill -f "streamlit" 2>/dev/null
    pkill -f "uvicorn" 2>/dev/null
    echo "✅ Alle Services beendet."
    exit 0
}

# Trap für Ctrl+C
trap cleanup INT TERM

# Warte auf Benutzer-Input (Ctrl+C)
echo "Drücke Ctrl+C zum Beenden..."
echo ""

# Halte Skript am Laufen
while true; do
    sleep 1
done

