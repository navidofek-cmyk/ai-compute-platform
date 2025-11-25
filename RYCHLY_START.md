# 🎮 Rychlý Start - Robot na Čísla! ⚡

> **5minutový start pro zkušenější děti!**

## 🚀 Super Rychlý Postup

### 1. Stáhni a Rozbali
```
https://github.com/navidofek-cmyk/ai-compute-platform
→ Code → Download ZIP → Rozbalit
```

### 2. Nainstaluj WSL
```powershell
# PowerShell jako správce:
wsl --install
# Restartuj počítač!
```

### 3. Nainstaluj Nástroje
```bash
# V WSL:
sudo apt update
sudo apt install python3 python3-pip build-essential cmake -y
```

### 4. Jdi do Složky
```bash
cd /mnt/c/Users/TVOJE_JMENO/Downloads/ai-compute-platform-main
```

### 5. Natrénuj Robot
```bash
cd ml_models
pip3 install torch torchvision pillow requests
python3 train_mnist.py
```
⏳ **5 minut** - učení z 60,000 obrázků

### 6. Postav Server
```bash
cd ../services/compute
cmake -S . -B build && cmake --build build -j4
cd build && ln -sf ../models models
```
⏳ **2 minuty** - stavění programu

### 7. Spusť!
```bash
cd ../../..
chmod +x start_all.sh && bash start_all.sh
```

### 8. Testuj!
```bash
cd ml_models
python3 test_classifier.py
```

## 🎉 Hotovo!

Uvidíš:
```
🔢 Testing digit: 0
   ✅ Top 3 predictions:
      1. Digit 0 - 55.33%
      2. Digit 6 - 14.12%
      3. Digit 4 - 6.81%
   ✅ CORRECT! 🎉
```

## 🛑 Zastav
```bash
bash stop_all.sh
```

## 🐛 Problém?
```bash
# Zastav vše a zkus znovu:
pkill -f uvicorn; pkill -f compute_service
bash start_all.sh
```

---

**👀 Chceš víc detailů?** → Přečti si **NAVOD_PRO_DETI.md**! 📖
