import requests
import json


MODEL = "qwen3:4b"

OLLAMA_URL = "http://localhost:11434/api/chat"


SYSTEM_PROMPT = """
Te egy magyar nyelvű kommentmoderációs rendszer vagy.

A feladatod a felhasználó által megadott komment elemzése.

Vizsgáld meg a következő kategóriákat:

1. personal_attack:
   A komment személyesen támad egy másik embert.

2. insult:
   A komment sértő, megalázó vagy lealacsonyító kifejezést tartalmaz.

3. hate_speech:
   A komment gyűlöletet vagy diszkriminációt fejez ki
   egy védett csoporttal szemben.

DÖNTÉSI SZABÁLYOK:

- DELETE: ha personal_attack, insult vagy hate_speech igaz.
- ALLOW: ha egyik kategória sem igaz.
- A negatív vélemény önmagában nem törlendő.
- A videó, termék vagy tartalom kritizálása önmagában nem személyes támadás.
- A kommentet magyar nyelven elemezd.

KIZÁRÓLAG JSON formátumban válaszolj.

Ne írj bevezetést.
Ne írj magyarázatot a JSON elé vagy mögé.
Ne jeleníts meg gondolatmenetet.

A reason mező egy rövid magyar indoklás legyen.

A JSON struktúrája:

{
    "personal_attack": false,
    "insult": false,
    "hate_speech": false,
    "decision": "ALLOW",
    "reason": "Rövid magyar indoklás."
}
"""


def moderate_comment(text: str) -> dict:

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": text
            }
        ],
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0
        }
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=120
    )

    response.raise_for_status()

    result = response.json()

    model_output = result["message"]["content"]

    moderation_result = json.loads(model_output)

    return moderation_result
