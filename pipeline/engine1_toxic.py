from transformers import pipeline


class ToxicityEngine:
    def __init__(self):
        # Betoltjuk a modellt a hugging face-rol
        self.pipe = pipeline("text-classification", model="unitary/multilingual-toxic-xlm-roberta", use_fast=False)

    def evaluate(self, text):
        if not text:
            return {"score": 0.0, "level": "alacsony", "details": {}}

       # Futtatas
        eredmeny = self.pipe(text)[0]
        
        # Pontszam kiolvasasa (mennyire toxic a komment)
        score = round(float(eredmeny["score"]), 4)
        details = {eredmeny["label"].lower(): score}

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
    proba = motor.evaluate("Te egy rohadt idióta faszkalap vagy, takarodj innen!")
    print(proba)