from transformers import pipeline


class ToxicityEngine:
    def __init__(self):
        # Betoltjuk a modellt a hugging face-rol
        self.pipe = pipeline(
            "text-classification",
            model="unitary/multilingual-toxic-xlm-roberta",
            use_fast=False
            )
    def evaluate(self, text:str) -> dict:
        if not text or not text.strip():
            return {
                "score": 0.0,
                "level": "alacsony",
                "details": {}
                }
       # Futtatas
        eredmeny = self.pipe(text.strip())[0]
        # Pontszam kiolvasasa (mennyire toxic a komment)
        score = round(float(eredmeny["score"]), 4)
        details = {
            eredmeny["label"].lower(): score
            }
        # Besorolas sulyossag alapjan
        if score < 0.3:
            level = "alacsony"
        elif score < 0.35:
            level = "közepes"
        else:
            level = "magas"
        return {
            "score": score,
            "level": level,
            "details": details
        }


if __name__ == "__main__":
    motor = ToxicityEngine()
    tesztek = [
    "This is a very good video!",
    "This video was terrible.",
    "You are a stupid idiot!",
    "I disagree with your opinion.",
    "You are completely worthless!"
]

    for komment in tesztek:

        eredmeny = motor.evaluate(komment)

        print("\nKomment:", komment)
        print("Toxicity:", eredmeny["score"])
        print("Besorolás:", eredmeny["level"])