from pipeline.engine1_toxic import ToxicityEngine
from pipeline.engine2_sentiment import sentiment
from pipeline.engine3_llm import moderate_comment

# A Toxicity pédányát csak egyszer hozuk létre
# Így nem töltjük be újra a modellt minden kommentnél 

toxicity_engine = None

def get_toxicity_engine():
    global toxicity_engine

    if toxicity_engine is None:
        toxicity_engine = ToxicityEngine()
    return toxicity_engine

def analyze_comment(text:str) -> dict:
    """
    lefuttatja a három ellenörző motort. 
    Az LLM hozza meg a végső döntést
    """

    if not text or not text.strip():
        raise ValueError("A komment nem lehet üres.")

    comment= text.strip()

    # 1.Toxicity Engine
    toxicity_result = get_toxicity_engine().evaluate(comment)
    # 2. Sentiment Engine
    sentiment_result = sentiment(comment)
    # 3. Kiegészítő infók az LLM-nek
    llm_input=f"""
Az alábbi kommentet kell moderálnod.

EREDETI KOMMENT:
{comment}

KIEGÉSZÍTŐ ELEMZÉSI EREDMÉNYEK:

Toxicity Engine:
- Pontszám: {toxicity_result["score"]}
- Besorolás: {toxicity_result["level"]}

Sentiment Engine:
- Hangulat: {sentiment_result["mood"]}
- Pontszám: {sentiment_result["score"]}

FONTOS:
A két elemzőmotor eredménye kizárólag kiegészítő információ.
A végső moderációs döntést önállóan, az eredeti komment tartalma
alapján hozd meg.
A negatív hangulat vagy magas toxicitási pontszám önmagában
nem indokolja a komment törlését.
""" 

    # 4. LLM - Döntéshozó
    llm_result = moderate_comment(llm_input)

    #5. Eredmények összegyűjtése
    return {
        "comment": comment,
        "toxicity": toxicity_result,
        "sentiment": sentiment_result,
        "moderation": llm_result,
        "decision": llm_result["decision"],
        "reason": llm_result["reason"]
    }

if __name__ == "__main__":

    teszt_kommentek = [
    "Nem tudom, hogyan sikerült ennyi butaságot összehordanod.",
    "Gratulálok, bebizonyítottad, hogy nem értesz hozzá.",
    "A harmadik állításod tényszerűen hibás.",
    "Szerintem nem megfelelően mutattad be a témát."
]

    for komment in teszt_kommentek:
        eredmeny = analyze_comment(komment)

        print("\n" + "=" * 60)
        print("Komment:", komment)
        print("Toxicity:", eredmeny["toxicity"]["score"])
        print("Sentiment:", eredmeny["sentiment"]["mood"])
        print("LLM döntés:", eredmeny["decision"])
        print("Indoklás:", eredmeny["reason"])

