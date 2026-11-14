# RageQuitEngine
3-fázisú MI pipeline automatikus toxicitásszűrésre, hangulatelemzésre és LLM-alapú közösségi moderációra.

# 🤬 RageQuitEngine

Egy 3 motoros, teljesen nyílt forráskódú MI pipeline automatikus kommentmoderációra. 

Ezt a projektet egyetemi beadandóként, csapatban készítjük. A célunk az volt, hogy egy olyan működő rendszert építsünk, ami **nem igényel semmilyen fizetős API-kulcsot vagy felhős előfizetést**: minden modell teljesen ingyenes, lokálisan futtatható open-source technológia.

---

## 👥 A Csapat
* Dr. Fekete József (WXZS41)– 
* Jobbágy Bertalan (IQGE2B) – 
* Gyapjas Kornél (F6JJ4L) – 

---

## 💡 Mi ez és miért csináljuk?
A netes komment szekciók gyakran átcsapnak toxikus vitákba, és a moderátoroknak képtelenség mindent átnézniük. A **RageQuitEngine** ezt a folyamatot automatizálja: a beérkező hozzászólást végigküldi három különálló, ingyenes open-source modellen, amik egymásra épülve dolgoznak, a végén pedig egy átlátható moderációs jelentést adnak.

---

## 🛠️ Hogyan működik a 3 motoros pipeline?

Teljesen ingyenes, nyílt forráskódú modelleket láncoltunk össze:

1. **1. Motor (Toxicitás szűrés):** Hugging Face Transformer modell, ami kiszűri a trágárságot és a gyűlöletbeszédet. *Teljesen ingyenes, helyben fut.*
2. **2. Motor (Hangulatelemzés):** Egy nyílt forráskódú Sentiment Analysis modell, ami megvizsgálja a szöveg érzelmi töltetét és feszültségét. *Ingyenes, offline fut.*
3. **3. Motor (LLM Döntéshozó):** **Ollama** segítségével lokálisan futtatott kis nyelvi modell, ami az előző két motor eredményeit összeveti, és generál egy emberi nyelvű indoklást + döntési javaslatot. *Költségmentes, helyi futtatás.*

## 💻 Telepítés és Szükséges Csomagok

### 1. Előfeltételek
* **Python 3.10+**
* **Ollama** (letölthető az [ollama.com](https://ollama.com) oldalról)
  * Telepítés után futtasd terminálban a QWEN3 letöltéséhez:  
    `ollama pull qwen3:4b`
  * Modell ellenőrzéséhez:
    `ollama list`
  * Letöltés után futtasd a terminálban a QWEN3 elindításához
    `ollama start qwen3:4b`

### 2. Python csomagok telepítése
A projektben használt könyvtárak (`transformers`, `torch`, `streamlit`, `requests`, `sentencepiece`,`tiktoken`):

```bash
pip install -r requirements.txt
```
### 3. A Streamlit alkalmazás indítása
```bash
python -m streamlit  run main.py
```
