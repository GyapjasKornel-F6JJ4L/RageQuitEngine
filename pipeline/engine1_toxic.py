from transformers import pipeline

class ToxicityEngine:
    def __init__(self):
        # Betoltjuk a modellt a hugging face-rol
        self.pipe = pipeline("text-classification", model="unitary/toxic-bert", top_k=None)

    def evaluate(self, text):
        if not text:
            return {"score": 0.0, "level": "alacsony", "details": {}}

        # Futtatas
        eredmeny = self.pipe(text)[0]
        
        # Pontszamok osszegyujtese
        details = {}
        for elem in eredmeny:
            kategoria = elem["label"]
            pont = round(float(elem["score"]), 4)
            details[kategoria] = pont

        toxic_score = details.get("toxic", 0.0)

        # Besorolas a kuszobok alapjan
        if toxic_score < 0.3:
            level = "alacsony"
        elif toxic_score < 0.7:
            level = "közepes"
        else:
            level = "magas"

        return {
            "score": toxic_score,
            "level": level,
            "details": details
        }


if __name__ == "__main__":
    motor = ToxicityEngine()
    proba = motor.evaluate("You are completely useless and I hate you!")
    print(proba)