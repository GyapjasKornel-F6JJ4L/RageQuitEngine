# teszt program a helyes json kimenetet és a döntési logikát teszteltem ezzel

from pipeline.engine3_llm import moderate_comment


comment = "Ez a videó borzalmas volt, teljesen feleslegesen néztem végig."


result = moderate_comment(comment)


print(result)

print("Döntés:", result["decision"])
print("Indoklás:", result["reason"])
