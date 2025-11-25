# 🎮 Tvůj Vlastní Robot na Rozpoznávání Číslic! 🤖

> **Pro děti od 10 let** - Nauč počítač rozpoznávat čísla jako superhrdina! 🦸

## 🌟 Co budeš dělat?

Představ si, že máš robota, který umí poznat, jaké číslo jsi nakreslil! 
Jako když Siri rozpozná tvůj hlas, ty naučíš počítač rozpoznávat čísla od 0 do 9.

---

## 🎯 Co budeš potřebovat?

- 💻 Počítač s Windows
- 🧠 Mozek (ten už máš!)
- ⏰ Asi 30 minut času
- 😊 Dobrou náladu

---

## 🚀 Krok 1: Stáhni si tajnou základnu (kód)

1. **Otevři si prohlížeč** (Chrome, Edge, Firefox...)

2. **Jdi na GitHub** - to je jako obří knihovna kódů:
   ```
   https://github.com/navidofek-cmyk/ai-compute-platform
   ```

3. **Stáhni si kód:**
   - Klikni na zelené tlačítko **"Code"** 💚
   - Vyber **"Download ZIP"**
   - Ulož si to na Plochu nebo do Dokumentů

4. **Rozbali ZIP soubor:**
   - Pravým tlačítkem na soubor → **"Rozbalit vše"**
   - Pamatuj si, kam jsi to rozbalil!

---

## 🛠️ Krok 2: Nainstaluj si kouzelné nástroje

### A) WSL - Linux ve Windows (jak mít dva počítače v jednom!)

1. **Otevři PowerShell jako správce:**
   - Stiskni `Windows` + `X`
   - Vyber **"Windows PowerShell (správce)"** nebo **"Terminál (správce)"**
   - Když se zeptá, zda může měnit věci → klikni **"Ano"**

2. **Napiš tenhle kouzelný příkaz:**
   ```powershell
   wsl --install
   ```
   ⏳ Počkej 5-10 minut... počítač stahuje Linux!

3. **Restartuj počítač** (důležité! ⚡)

4. **Po restartu:**
   - Otevře se okno, kde si vymyslíš:
     - **Uživatelské jméno** (např. `tvoje_jmeno`)
     - **Heslo** (nezapomeň si ho zapamatovat! 🔐)

### B) Python - jazyk, kterým mluvíme s počítačem

Ve WSL napiš (postupně, po každém řádku stiskni Enter):

```bash
sudo apt update
sudo apt install python3 python3-pip -y
```

Zadej heslo, když se zeptá.

### C) CMake a C++ - nástroje pro stavbu programu

```bash
sudo apt install build-essential cmake -y
```

---

## 🎨 Krok 3: Nauč robota rozpoznávat čísla!

### Příprava:

1. **Otevři WSL terminál**
2. **Přejdi do složky s kódem:**
   ```bash
   cd /mnt/c/Users/TVOJE_JMENO/Downloads/ai-compute-platform-main
   ```
   (Změň `TVOJE_JMENO` na své jméno ve Windows!)

### Trénování mozku robota:

```bash
cd ml_models
pip3 install torch torchvision pillow requests
python3 train_mnist.py
```

⏳ **Počkej asi 5 minut** - robot se učí rozpoznávat 60,000 obrázků číslic!

Uvidíš něco jako:
```
Epoch 1/5: █████████░ 95% | Accuracy: 92.34%
Epoch 2/5: █████████░ 95% | Accuracy: 95.12%
...
✅ Trénování dokončeno! Přesnost: 97.56%
```

🎉 **WOW!** Robot správně pozná čísla z 97.56%!

---

## 🏗️ Krok 4: Postav robotovu továrnu (C++ server)

```bash
cd ../services/compute
cmake -S . -B build
cmake --build build -j4
```

⏳ Počkej 2-3 minuty... staví se továrna!

---

## 🚦 Krok 5: Spusť robota!

### A) Vytvoř symlink (zkratka k modelům):

```bash
cd build
ln -sf ../models models
```

### B) Spusť všechny systémy:

```bash
cd ../../..
chmod +x start_all.sh
bash start_all.sh
```

Uvidíš:
```
✓ Compute service started (PID: 12345)
✓ Gateway started (PID: 67890)
```

🎊 **Funguje! Robot žije!**

---

## 🎮 Krok 6: Hraj si s robotem!

### Test 1: Nakresli čísla a nech robota hádat

```bash
cd ml_models
python3 test_classifier.py
```

Robot nakreslí čísla 0-9 a zkusí je poznat:

```
🔢 Testing digit: 0
   ✅ Top 3 predictions:
      1. Digit 0 - 55.33%  ← Robot myslí, že je to 0 (správně!)
      2. Digit 6 - 14.12%
      3. Digit 4 - 6.81%
   ⏱️  Inference time: 89.04 ms
   ✅ CORRECT! 🎉

🔢 Testing digit: 1
   ✅ Top 3 predictions:
      1. Digit 1 - 83.44%  ← Super jistý!
      2. Digit 8 - 6.97%
      3. Digit 7 - 3.82%
   ✅ CORRECT! 🎉
```

### Test 2: Jednoduchý test

```bash
python3 test_simple.py
```

Ukáže, jak rychle robot myslí!

---

## 🧪 Co se vlastně stalo? (Jak to funguje?)

### 1. **Trénování = Učení**
   - Robot viděl 60,000 obrázků číslic
   - Učil se, jak vypadá 0, 1, 2, 3...
   - Jako když se učíš abecedu!

### 2. **Neural Network = Umělý mozek**
   - Má 784 "očí" (každé vidí jeden pixel)
   - 128 "myšlenek" v hlavě
   - 10 "odpovědí" (0-9)

### 3. **Inference = Hádání**
   - Robot dostane nový obrázek
   - Projde mozkem za 0.1 sekundy
   - Řekne: "Myslím, že je to 7!"

---

## 🎨 Bonus: Udělej si vlastní testy!

### Nakresli si své číslo v Paintu:

1. **Otevři Paint** (Windows → hledej "Paint")
2. **Změň velikost:** 28×28 pixelů (Obrázek → Změnit velikost)
3. **Nakresli číslo:** Černým fixem na bílém pozadí
4. **Ulož jako:** `moje_cislo.png`
5. **Přesuň do:** `ml_models/`

### Otestuj vlastní obrázek:

```python
# Vytvoř soubor test_vlastni.py
from PIL import Image
import numpy as np
import requests

# Načti obrázek
img = Image.open('moje_cislo.png').convert('L')
img = img.resize((28, 28))

# Převeď na data
arr = np.array(img, dtype=np.float32)
data = (1.0 - arr / 255.0).flatten().tolist()

# Pošli robotovi
response = requests.post('http://localhost:8000/api/v1/ml/inference', json={
    "model_name": "mnist",
    "input_data": data,
    "input_shape": [1, 1, 28, 28],
    "apply_softmax": True,
    "top_k": 5
})

# Ukaž výsledek
result = response.json()
print(f"🤖 Robot myslí, že je to: {result['top_classes'][0]}")
print(f"📊 Jistota: {result['top_probabilities'][0]*100:.1f}%")
```

---

## 🛑 Jak robota zastavit?

```bash
bash stop_all.sh
```

---

## 🐛 Co když něco nefunguje?

### ❌ "Command not found"
```bash
# Ujisti se, že jsi ve správné složce:
pwd
# Mělo by to být něco jako: /mnt/c/Users/.../ai-compute-platform-main
```

### ❌ "Permission denied"
```bash
chmod +x start_all.sh stop_all.sh
```

### ❌ "Port 8000 already in use"
```bash
# Zastav starého robota:
pkill -f uvicorn
pkill -f compute_service
# Pak spusť znovu
```

### ❌ Robot špatně hádá
- To je normální! Není dokonalý.
- Zkus jednodušší čísla (0, 1, 8)
- Některá čísla jsou těžší (2, 3, 5, 9)

---

## 🎓 Co ses naučil?

✅ **Umělá inteligence** - Robot se učí sám!  
✅ **Machine Learning** - Učení z příkladů  
✅ **Neural Networks** - Umělý mozek  
✅ **Python** - Programovací jazyk  
✅ **C++** - Rychlý programovací jazyk  
✅ **Linux** - Jiný operační systém  
✅ **Git** - Ukládání kódu  
✅ **APIs** - Jak programy spolu mluví

---

## 🚀 Co dál?

### Experimenty:

1. **Nakresli 100 číslic** a sleduj, kolik jich robot pozná správně
2. **Zkus písmena** (budou to potřebovat jiný model)
3. **Změň počet epoch** v `train_mnist.py` (řádek 83) na 10 - robot bude chytřejší!
4. **Přidej barvy** - zkus barevné číslice

### Sdílej výsledky:

- Ukaž kamarádům!
- Nauč mladší sourozence!
- Vyfot si statistiky a pochluď se rodičům! 📸

---

## 📚 Slovníček pojmů (jako ve hře!)

| Slovo | Co to znamená | Příklad |
|-------|---------------|---------|
| **AI** | Artificial Intelligence - Umělá inteligence | Robot myslí sám! |
| **MNIST** | Databáze 70,000 číslic | Učebnice pro roboty |
| **Epoch** | Jedno celé učení všech dat | Jako jedna školní hodina |
| **Accuracy** | Přesnost - kolik % správně | 97.56% = skoro vše správně! |
| **Inference** | Hádání/Předpovídání | Robot háda, co vidí |
| **Model** | Naučený mozek robota | Soubor `mnist_model.onnx` |
| **API** | Způsob, jak mluvit s robotem | Jako telefon mezi programy |
| **Training** | Učení/Trénování | Robot se učí z 60,000 příkladů |

---

## 🏆 Gratulujeme! 

**Právě jsi vytvořil svého prvního AI robota!** 🎉

Teď jsi:
- 🧙 **AI Kouzelník** - Ovládáš umělou inteligenci
- 🤖 **Robot Trenér** - Naučil jsi robota číst
- 💻 **Programátor** - Spustil jsi složitý systém
- 🏗️ **Stavitel** - Postavil jsi ML pipeline

**Sdílej tento projekt s kamarády a pokračuj v učení!** 🌟

---

## 🆘 Potřebuješ pomoc?

- **GitHub Issues:** https://github.com/navidofek-cmyk/ai-compute-platform/issues
- **Zeptej se rodičů/učitelů** - ukaž jim tento návod!

---

**Made with ❤️ by AI Enthusiasts**  
*Keep learning, keep building, keep having fun!* 🚀
