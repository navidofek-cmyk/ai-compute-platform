# 🚀 High-Performance Microservices Platform with AI

Pokročilá mikroservisní architektura kombinující **Python FastAPI** (webové rozhraní) s **C++ gRPC** výpočetním backendem a **OpenAI** asistentskými schopnostmi.

## 🏗️ Architektura

```
User 👤
  ↓ HTTP REST API
🤖 AI Assistant (OpenAI GPT-4)
  ↓
🐍 Python Gateway (FastAPI - Port 8000)
  ↓ gRPC
⚡ C++ Compute Service (Port 50051)
```

## ✨ Funkce

### 🧮 Výpočetní Operace
- **Matrix Multiplication** - Optimalizované násobení matic
- **Statistical Analysis** - Průměr, směrodatná odchylka, min/max
- **Monte Carlo Simulation** - Paralelní simulace
- **Vector Operations** - Sčítání, odčítání, skalární a vektorový součin

### 🤖 AI Asistent
- **Natural Language Queries** - Dotazy v češtině: "Vynásob dvě matice 3x3"
- **Result Analysis** - AI vysvětlení výsledků
- **Parameter Optimization** - Doporučení optimálních parametrů

## 🚀 Rychlý Start

### Předpoklady
- WSL2 / Linux (Ubuntu 22.04+)
- Python 3.10+
- C++ (g++ 11+)
- OpenAI API Key

### Instalace

```bash
# 1. Python závislosti
cd services/gateway
pip install -r requirements.txt

# 2. Build C++ služby
cd ../compute/build
cmake .. && make -j4
```

### Konfigurace

```bash
# Zkopírování template
cp .env.example .env

# Přidání API klíče do .env
# OPENAI_API_KEY=sk-proj-your-key-here
```

### Spuštění

```powershell
# Terminál 1: C++ Service
.\start_compute.ps1

# Terminál 2: Python Gateway  
.\start_gateway.ps1
```

### Test

Otevřete v prohlížeči:
```
http://localhost:8000/docs
```

## 📚 API Příklady

### AI Natural Language Query

```bash
curl -X POST "http://localhost:8000/api/v1/ai/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Vynásob dvě matice 3x3",
    "auto_execute": true
  }'
```

### Klasické API

```bash
curl -X POST "http://localhost:8000/api/v1/compute/matrix/multiply" \
  -H "Content-Type: application/json" \
  -d '{
    "matrix_a": [[1, 2], [3, 4]],
    "matrix_b": [[5, 6], [7, 8]]
  }'
```

## 🔧 Struktura Projektu

```
cppplay/
├── .env                     # API klíče (GITIGNORED!)
├── .env.example             # Template
├── .gitignore              
├── README.md               
├── start_compute.ps1        # Start C++ service
├── start_gateway.ps1        # Start Python gateway
├── proto/
│   └── compute.proto        
└── services/
    ├── compute/             # C++ gRPC Service
    │   ├── CMakeLists.txt
    │   ├── include/
    │   └── src/
    └── gateway/             # Python FastAPI Gateway
        ├── requirements.txt
        └── app/
            ├── main.py
            ├── routers/
            │   └── ai.py    # AI endpoints
            └── services/
                └── ai_assistant.py
```

## 🔒 Bezpečnost

⚠️ **KRITICKÉ:**
- ✅ `.env` je v `.gitignore`
- ✅ Nikdy necommitovat API klíče
- ✅ Používat `.env.example` jako template

## 🐛 Troubleshooting

### `OPENAI_API_KEY není nastavený`
```bash
# Zkontrolujte .env
cat .env | grep OPENAI_API_KEY
```

### `compute_service_unavailable`
```bash
# Restart C++ služby
.\start_compute.ps1
```

## 📊 Performance

| Operace | Velikost | Čas (ms) |
|---------|----------|----------|
| Matrix Multiply | 100x100 | ~2.5 |
| Statistics | 1M samples | ~15 |
| Monte Carlo | 100K iter | ~50 |

## 📄 Licence

MIT License

---

**Pro více info:** Viz `JEDNODUCHY_NAVOD.md`
