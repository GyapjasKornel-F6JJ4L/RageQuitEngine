from transformers import pipeline


class ToxicityEngine:
    def __init__(self, model_name: str = "unitary/toxic-bert"):
        print(f"[{self.__class__.__name__}] Modell betöltése ({model_name})...")
        self.classifier = pipeline(
            "text-classification",
            model=model_name,
            top_k=None
        )

    def evaluate(self, text: str) -> dict:
        if not text or not text.strip():
            return {
                "score": 0.0,
                "level": "alacsony",
                "details": {}
            }

        raw_results = self.classifier(text)[0]
        scores = {item["label"]: round(float(item["score"]), 4) for item in raw_results}
        toxic_score = scores.get("toxic", 0.0)

        if toxic_score < 0.3:
            level = "alacsony"
        elif toxic_score < 0.7:
            level = "közepes"
        else:
            level = "magas"

        return {
            "score": toxic_score,
            "level": level,
            "details": scores
        }


if __name__ == "__main__":
    engine = ToxicityEngine()
    test_comment = "You are completely useless and I hate you!"
    result = engine.evaluate(test_comment)

    print("\n--- Teszt Eredmény ---")
    print(f"Szöveg: {test_comment}")
    print(f"Pontszám: {result['score']} ({result['level']})")
    print("Részletek:", result["details"])