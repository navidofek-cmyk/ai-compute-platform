# 🚀 Jak spustit super rychlou počítačku

Tento návod vysvětluje, jak spustit speciální program, který umí rychle počítat složité věci.

---

## 🎯 Co to vlastně je?

Program se skládá ze dvou částí:

1. **Python část** 🐍 - Komunikuje s uživatelem a má webové rozhraní. Je přívětivá a snadno ovladatelná.

2. **C++ část** ⚡ - Je SUPER rychlá v počítání! Umí násobit obrovské tabulky čísel v několika milisekundách.

Když uživatel něco zadá, Python část to přeloží do jazyka, kterému rozumí C++ část, a ta to bleskově spočítá!

---

## 📦 Co náš program umí?

### 1. **Násobení matic** 🔢
Velká tabulka čísel (jako šachovnice s čísly). Program dokáže dvě takové tabulky vynásobit dohromady!

### 2. **Statistika** 📊
Vezme spoustu náhodných čísel a vypočítá:
- Jaký je průměr (prostředek)
- Které číslo je největší a nejmenší
- Jak moc se čísla liší

### 3. **Monte Carlo simulace** 🎲
To je jako házet tisíckrát kostkou a sledovat, co se stane. Používá se třeba na předpověď počasí!

### 4. **Vektorové operace** ➕
Sčítá nebo násobí dlouhé řady čísel najednou.

---

## 🎮 Jak to spustit?

### Krok 1: Spuštění C++ služby (Výpočetní část)

V PowerShell terminálu se spustí příkaz:

```powershell
.\start_compute.ps1
```

Výstup by měl vypadat takto:
```
[INFO] Server listening on 0.0.0.0:50051
```

✅ To znamená: **C++ služba je připravená!**

---

### Krok 2: Spuštění Python služby (Webová brána)

Ve druhém PowerShell okně se spustí příkaz:

```powershell
.\start_gateway.ps1
```

Výstup by měl vypadat takto:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ To znamená: **Python služba je taky připravená!**

---

### Krok 3: Otevření webového rozhraní

V prohlížeči se otevře adresa:

```
http://localhost:8000/docs
```

Zobrazí se **interaktivní dokumentace API** s tlačítky! 🎛️

---

## 🕹️ Jak používat ovládací desku (Swagger UI)

### Test 1: Zkontroluj, jestli to funguje ❤️

1. Najdi **`GET /health`**
2. Klikni na něj
3. Klikni **"Try it out"**
4. Klikni **"Execute"**

✅ Odpověď by měla obsahovat: `"status": "healthy"` - To znamená, že všechno běží!

---

### Test 2: Vynásob matice! 🔢

1. Najdi **`POST /api/v1/compute/matrix/multiply`**
2. Kliknutí na endpoint
3. Kliknutí na **"Try it out"**
4. Zobrazí se okénko s výchozími hodnotami:
```json
{
  "rows_a": 3,
  "cols_a": 3,
  "rows_b": 3,
  "cols_b": 3
}
```
5. Klikni **"Execute"**

🎉 Program vrátí výsledek včetně času výpočtu (mělo by to být MEGA rychlé - míň než 1 milisekundu!)

---

### Test 3: Statistika náhodných čísel 📊

1. Najde se **`POST /api/v1/compute/stats/analyze`**
2. Zadá se například:
```json
{
  "size": 1000
}
```
To znamená: "Udělej statistiku z tisíce náhodných čísel"

3. Klikni **"Execute"**

Program vrátí:
- `mean` - průměr
- `std_dev` - jak moc se čísla liší
- `min` - nejmenší číslo
- `max` - největší číslo

---

### Test 4: Monte Carlo - házej "kostkou"! 🎲

1. Najde se **`POST /api/v1/compute/montecarlo/run`**
2. Zadá se:
```json
{
  "num_simulations": 10000
}
```
To znamená: "Hoď kostkou 10 000krát"

3. Klikni **"Execute"**

Program vrátí výsledek simulace!

---

## 🎨 Formát odpovědi

Každá odpověď obsahuje:

```json
{
  "result": "nějaký výsledek",
  "computation_time_ms": 0.5,
  "backend_time_ms": 0.3
}
```

- **computation_time_ms** = Jak dlouho to celkem trvalo (v milisekundách)
- **backend_time_ms** = Jak dlouho počítal C++ kamarád

💡 **1 milisekunda = 1/1000 sekundy** - to je MEGA rychlé!

---

## 🛑 Jak to vypnout?

Stiskne se **`Ctrl + C`** v obou PowerShell oknech.

To ukončí běh obou služeb. 👋

---

## 🤔 Co když něco nefunguje?

### Chyba: "ERR_CONNECTION_REFUSED"

❌ **Problém:** Python služba není spuštěná.

✅ **Řešení:** Je třeba znovu spustit `.\.start_gateway.ps1`

---

### Chyba: "Method Not Allowed"

❌ **Problém:** Adresa byla zadána přímo do prohlížeče (to posílá GET místo POST).

✅ **Řešení:** Je třeba použít rozhraní na `http://localhost:8000/docs`

---

### Chyba: "Failed to connect to backend"

❌ **Problém:** C++ služba není spuštěná.

✅ **Řešení:** Je třeba znovu spustit `.\.start_compute.ps1`

---

## 🏗️ Jak to uvnitř funguje?

```
Uživatel 👤
    ↓
    💻 Požadavek v prohlížeči
    ↓
🐍 Python Gateway (port 8000)
    ↓ 
    📡 Překlad požadavku do gRPC
    ↓
⚡ C++ Compute Service (port 50051)
    ↓
    🧮 Rychlé počítání!
    ↓
    📡 Vrácení výsledku
    ↓
🐍 Python Gateway
    ↓
    💻 Formátování do JSON
    ↓
😊 Uživatel (obdrží výsledek)
```

---

## 🎓 Slovníček pojmů

- **Port** = Jako číslo dveří u domu. Python má dveře číslo 8000, C++ má číslo 50051.
- **API** = Způsob, jak se programy spolu baví.
- **gRPC** = Speciální jazyk, kterým spolu mluví Python a C++.
- **HTTP** = Jazyk, kterým mluví webové stránky.
- **JSON** = Způsob, jak zapisovat data (vypadá jako `{"jmeno": "Karel", "vek": 10}`).
- **Milisekunda** = Tisícina sekundy (ms).
- **Thread Pool** = Jako když máš 8 pomocníků, kteří dělají věci najednou.

---

## 🏆 Proč to děláme takhle?

**Python** 🐍 je:
- ✅ Snadný na psaní
- ✅ Hodně lidí ho umí
- ✅ Má hezké knihovny pro web
- ❌ Ale trochu pomalý na počítání

**C++** ⚡ je:
- ✅ MEGA rychlý na počítání
- ✅ Umí pracovat s více procesory najednou
- ❌ Ale těžší na psaní

**Spolu** tvoří výkonný systém 🦇 - každá část má svoje speciality!

---

## 📚 Možnosti experimentování

1. **Změna vstupních hodnot** - například místo 3x3 matice použít 10x10
2. **Porovnání časů** - zjistit, zda jsou větší matice pomalejší
3. **Více simulací** - vyzkoušet třeba 100 000 simulací Monte Carlo
4. **Sledování terminálu** - v terminálu jsou vidět logy (záznamy) o probíhajících operacích

---

## 🎉 Shrnutí

Tento systém představuje sofistikovanou mikroservisní architekturu s:
- ✅ Python webovým rozhraním
- ✅ C++ výpočetním enginem
- ✅ gRPC komunikací
- ✅ Paralelním zpracováním

Jde o profesionální technologii, kterou používají velké firmy jako Google nebo Netflix! 👏

---

## 🆘 Řešení problémů

Kontrolní seznam:
1. ✅ Běží oba programy? (Kontrola v terminálu)
2. ✅ Je použita správná adresa? (`http://localhost:8000/docs`)
3. ✅ Je použito tlačítko "Try it out" ve Swaggeru?

Pokud problémy přetrvávají, doporučuje se restart:
1. Stisknout `Ctrl+C` v obou terminálech
2. Znovu spustit `.\.start_compute.ps1`
3. Znovu spustit `.\.start_gateway.ps1`
4. Opakovat test

---

**Vytvořeno: 23. listopadu 2025**  
**Verze: Pro děti a začátečníky** 🎈
