from src.pipeline import *
import json

with open("questions.json", "r", encoding="utf-8") as f:
    dados = json.load(f)

print(dados)
