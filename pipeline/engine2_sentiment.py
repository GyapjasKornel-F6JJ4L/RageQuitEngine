from transformers import pipeline

sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="NYTK/sentiment-hts5-hubert-hungarian",
)

def sentiment(text: str) -> dict:
    result = sentiment_pipeline(text)[0]
    score = round(result["score"], 2)
    label = int(result["label"].split()[0])

    match label:
        case 0:
            mood = "Teljesen negatív"
        case 1:
            mood = "Inkább negatív"
        case 2:
            mood = "Neutrális"
        case 3:
            mood = "Inkább pozitív"
        case 4:
            mood = "Teljesen pozitív"
        case _:
            mood = "Unknown"

    print(mood)
    print(score)
    return {"mood": mood, "score": score}
