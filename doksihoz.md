# RageQuitEngine

## Automatikus kommentmoderációs rendszer

A RageQuitEngine egy három elemzőmotorból álló, mesterséges intelligencián alapuló kommentmoderációs rendszer. A projekt célja, hogy felhasználói hozzászólásokat elemezzen, felismerje a sértő, személyeskedő vagy gyűlöletkeltő megnyilvánulásokat, majd ezek alapján moderációs javaslatot adjon.

A rendszer helyben futtatható, nyílt forráskódú modelleket használ, így nincs szükség fizetős külső API-szolgáltatásokra.

## 1. A rendszer felépítése

A RageQuitEngine három különböző elemzőmotort alkalmaz:

- **Engine 1 – Toxicity Engine:** A kommentek toxicitását vizsgálja, és pontszámot, valamint súlyossági besorolást ad.
- **Engine 2 – Sentiment Engine:** Meghatározza a komment érzelmi töltetét, például negatív, semleges vagy pozitív hangulatát.
- **Engine 3 – LLM Moderáció:** Egy helyben futó nyelvi modell segítségével elemzi a komment tartalmát, és meghozza a végső moderációs döntést.

A rendszer működését a `decision.py` koordinálja. Ez összegyűjti az első két motor eredményeit, majd kiegészítő információként továbbítja azokat a harmadik motornak.

A végső döntést minden esetben az LLM hozza meg. A toxicitási pontszám és az érzelmi elemzés önmagukban nem eredményeznek automatikus törlést.

## 2. Alkalmazott technológiák és modellek

| Technológia | Felhasználás |
|---|---|
| Python | A rendszer programozási nyelve |
| Streamlit | Felhasználói felület |
| Hugging Face Transformers | Gépi tanulási modellek futtatása |
| PyTorch | Modellek futtatási háttere |
| Ollama | Helyi nyelvi modell futtatása |
| Qwen3:4b | LLM-alapú moderáció |

### Alkalmazott modellek

- Toxicity: `unitary/multilingual-toxic-xlm-roberta`
- Sentiment: `NYTK/sentiment-hts5-hubert-hungarian`
- LLM: `qwen3:4b`

## 3. Projektstruktúra

```text
RageQuitEngine/
│
├── main.py
│
├── pipeline/
│   ├── __init__.py
│   ├── engine1_toxic.py
│   ├── engine2_sentiment.py
│   ├── engine3_llm.py
│   └── decision.py
│
├── tests/
│   └── test_pipeline.py
│
├── requirements.txt
└── README.md
```

## 4. Telepítés

### Előfeltételek

- Python 3.10 vagy újabb
- Ollama telepítve a számítógépen
- Internetkapcsolat az első modellletöltésekhez

### Python-függőségek telepítése

A projekt gyökérkönyvtárában futtassuk:

```bash
pip install -r requirements.txt
```

### Ollama és a nyelvi modell telepítése

Az Ollama telepítése után töltsük le a használt modellt:

```bash
ollama pull qwen3:4b
```

Ellenőrizzük, hogy a modell elérhető:

```bash
ollama list
```

Az Ollama szolgáltatásnak futnia kell a program használata közben.

## 5. A program indítása

A projekt gyökérkönyvtárából futtassuk:

```bash
python -m streamlit run main.py
```

Ezután a Streamlit által megadott helyi címen, általában a `http://localhost:8501` oldalon érhető el a felhasználói felület.

## 6. A rendszer működése

1. A felhasználó megad egy kommentet a webes felületen.
2. A Toxicity Engine megvizsgálja a hozzászólás toxicitását.
3. A Sentiment Engine meghatározza a hozzászólás érzelmi töltetét.
4. A Decision modul összegyűjti az elemzési eredményeket.
5. Az LLM elemzi az eredeti kommentet és a kiegészítő információkat.
6. A rendszer megjeleníti a moderációs döntést és annak rövid indoklását.

A lehetséges végső döntések:

- **ALLOW:** A komment engedélyezhető.
- **DELETE:** A komment törlésre javasolt.

## 7. Fontos megjegyzés

A RageQuitEngine egy kísérleti, mesterséges intelligencián alapuló moderációs rendszer. Az automatikus elemzés eredménye nem tekinthető minden esetben tévedhetetlennek. A modellek nyelvi és kontextuális korlátai miatt előfordulhatnak téves besorolások, ezért éles környezetben emberi felülvizsgálat is javasolt.










# A harmadik elemzőmotor és a döntési modul működése

## 1. Engine 3 – LLM-alapú kommentmoderáció (`engine3_llm.py`)

A RageQuitEngine harmadik elemzőmotorja egy nagy nyelvi modellre (Large Language Model, LLM) épülő moderációs komponens. Feladata, hogy a felhasználók által beküldött hozzászólásokat szövegkörnyezetükben értelmezze, felismerje a nem megfelelő megnyilvánulásokat, majd ezek alapján meghozza a végső moderációs döntést.

A rendszer a Qwen3:4b modellt használja, amely az Ollama segítségével, helyi környezetben futtatható. Ennek köszönhetően a kommentek elemzése nem igényel fizetős külső API-szolgáltatást. A modell a `requests` Python-könyvtáron keresztül kommunikál az Ollama helyi HTTP API-jával.

A kommunikáció a következő végponton történik:

`http://localhost:11434/api/chat`

A modul központi függvénye a `moderate_comment(text: str)`, amely bemenetként egy szöveget kap. A függvény összeállítja az Ollama számára szükséges kérést, majd elküldi azt a helyi modellnek.

### 1.1. A moderációs utasításrendszer

A modell működését egy előre meghatározott rendszerutasítás, azaz `SYSTEM_PROMPT` szabályozza. Ez tartalmazza a moderációs szempontokat és azokat a szabályokat, amelyek alapján a modellnek értékelnie kell a hozzászólásokat.

A moderáció során három fő kategóriát vizsgál:

- **Personal attack (személyes támadás):** A komment a másik személy intelligenciáját, hozzáértését, gondolkodási képességét vagy emberi értékét támadja.
- **Insult (sértés):** A hozzászólás sértő, megalázó, trágár vagy lealacsonyító kifejezéseket tartalmaz.
- **Hate speech (gyűlöletbeszéd):** A komment valamely védett tulajdonság alapján egy személyt vagy csoportot támad, diszkriminál vagy kirekesztésre buzdít.

A rendszer fontos szempontja, hogy különbséget tegyen a kulturált kritika és a személyeskedő megnyilvánulások között. Egy negatív vélemény vagy szakmai kritika önmagában nem indokolja a hozzászólás törlését. Például egy videó minőségének vagy egy állítás helyességének bírálata engedélyezhető, amennyiben nem válik sértővé vagy személyeskedővé.

A rendszerutasítás kitér az olyan közvetett személyeskedő megfogalmazásokra is, amelyek nem feltétlenül tartalmaznak trágár kifejezéseket, mégis a másik személy képességeit vagy intelligenciáját minősítik lealacsonyító módon.

### 1.2. A modell válaszának feldolgozása

A modell válaszát a program kötött JSON-formátumban kéri le. Ez lehetővé teszi, hogy az eredményt a Python-program további részei egyszerűen feldolgozzák.

A válasz az alábbi adatokat tartalmazza:

- `personal_attack`: történt-e személyes támadás;
- `insult`: tartalmaz-e a komment sértést;
- `hate_speech`: felismerhető-e gyűlöletbeszéd;
- `decision`: a végső moderációs döntés (`ALLOW` vagy `DELETE`);
- `reason`: a döntés rövid, magyar nyelvű indoklása.

A JSON-választ a Python `json` moduljának segítségével alakítja a program feldolgozható adattá.

A modell a megadott moderációs szabályok alapján `ALLOW` döntést ad, ha a komment nem sérti a meghatározott feltételeket. Amennyiben személyes támadást, sértést vagy gyűlöletbeszédet azonosít, a döntés `DELETE` lesz.

A függvény végül egy szótárat ad vissza, amely tartalmazza a moderációs kategóriákat, a döntést és az indoklást.

---

## 2. Decision modul – Az elemzőmotorok koordinálása (`decision.py`)

A `decision.py` modul feladata a RageQuitEngine három elemzőmotorjának összehangolása és a teljes elemzési folyamat vezérlése. Ez a komponens biztosítja, hogy a különálló motorok eredményei egységes folyamatban kerüljenek feldolgozásra.

A modul központi függvénye az `analyze_comment(text: str)`, amely a felhasználótól kapott kommentet bemenetként fogadja.

A függvény először ellenőrzi, hogy a megadott szöveg nem üres-e. Amennyiben a bemenet üres vagy csak szóközöket tartalmaz, `ValueError` kivételt dob.

### 2.1. A Toxicity Engine futtatása

Az első lépésben a modul meghívja a Toxicity Engine-t, amely megvizsgálja a hozzászólás toxicitását.

Az elemzés eredményeként a motor egy pontszámot, egy súlyossági besorolást és további részleteket ad vissza.

A modell példányosítása a `get_toxicity_engine()` függvényen keresztül történik. A modul egy globális változóban tárolja a létrehozott példányt, így a modellt nem kell minden egyes komment elemzésekor újra betölteni. Ez csökkenti a felesleges inicializálásból adódó időveszteséget.

### 2.2. A Sentiment Engine futtatása

A következő lépésben a rendszer meghívja a Sentiment Engine `sentiment()` függvényét.

Ez a motor a komment érzelmi töltetét vizsgálja, és meghatározza annak hangulati kategóriáját, valamint a modell által visszaadott pontszámot.

Az eredmény például lehet teljesen negatív, inkább negatív, neutrális, inkább pozitív vagy teljesen pozitív.

A sentiment eredmény szintén kiegészítő információként szolgál a további feldolgozáshoz.

### 2.3. Az eredmények továbbítása az LLM számára

Miután az első két elemzőmotor lefutott, a `decision.py` összeállít egy szöveges bemenetet a harmadik motor számára.

Ez a bemenet három fő részből áll:

1. Az eredeti felhasználói komment.
2. A Toxicity Engine által meghatározott pontszám és súlyossági besorolás.
3. A Sentiment Engine által meghatározott hangulati kategória és pontszám.

A modul külön utasításban jelzi a nyelvi modell számára, hogy a két előző motor eredménye kizárólag kiegészítő információként használható fel.

Ez a projekt egyik legfontosabb tervezési döntése: **a végső moderációs döntést kizárólag az LLM hozza meg.**

A toxicitási pontszám vagy a negatív érzelmi töltet önmagában nem elegendő egy komment törléséhez. Így például egy negatív, de kulturált vélemény továbbra is engedélyezhető.

### 2.4. A végső eredmény összeállítása

Az utolsó lépésben a `decision.py` meghívja az Engine 3 `moderate_comment()` függvényét, amely visszaadja a nyelvi modell moderációs eredményét.

A modul ezután egy egységes Python-szótárba rendezi az összes elemzési eredményt:

- az eredeti kommentet;
- a toxicitási elemzés eredményét;
- az érzelmi elemzés eredményét;
- az LLM által visszaadott moderációs kategóriákat;
- a végső döntést;
- a döntés rövid indoklását.

Az `analyze_comment()` függvény ezt az egységes eredményt adja vissza a program többi része számára.

A Streamlit-alapú felhasználói felület ezt az adatstruktúrát használja fel az elemzési eredmények megjelenítéséhez.

---

## 3. A két modul kapcsolata a rendszer egészében

Az `engine3_llm.py` és a `decision.py` egymásra épülő, de eltérő feladatot ellátó komponensek.

A `decision.py` felelős az elemzési folyamat koordinálásáért, az első két motor eredményeinek összegyűjtéséért és a harmadik motor bemenetének előállításáért.

Az `engine3_llm.py` ezzel szemben kizárólag a nyelvi modellel történő kommunikációt és a moderációs válasz feldolgozását végzi.

A két modul szétválasztása átláthatóbbá és könnyebben karbantarthatóvá teszi a projektet. Az elemzőmotorok feladatai elkülönülnek, miközben a döntési folyamat egyetlen központi modulból vezérelhető.

Ennek eredményeként a RageQuitEngine egy olyan hárommotoros moderációs pipeline-t valósít meg, amelyben a gépi tanulási modellek különböző szempontok alapján vizsgálják a hozzászólásokat, a végső moderációs döntésért pedig a helyben futó nagy nyelvi modell felel.