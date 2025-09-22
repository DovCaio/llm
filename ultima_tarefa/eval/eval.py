from langchain_huggingface import HuggingFaceEmbeddings
import src.pipeline as pipeline
from src.app import *
import json
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
answer_save_path = "./eval/answers.json"
OUTPUT_MD = "./eval/report.md"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        result = json.load(f)
    return result

def save_json(path, new_data):
    data = load_json(path)
    data.append(new_data)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

questions = load_json("./eval/questions.json")

def get_response(answer):
    state = optimizer_workflow.invoke({"query": answer})
    return state["final_response"]

def get_response():
    for question in questions:
        current_question = question["question"]
        llm_response = get_response(current_question)
        id = question["id"]
        golden_answer = question["answer"]

        answer_json = {
            "id" : id,
            "question" : question["question"],
            "llm_response" : llm_response,
            "golden_answer" : golden_answer
        }

        save_json(answer_save_path, answer_json)

#get_response() #para gerar todas descomente isso

#Calculo de coeficientes

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

responses = load_json("./eval/answers.json")

faithfulness_scores = []
relevancy_scores = []


report_rows = []

for r in responses:
    # Faithfulness: LLM response vs Golden answer
    emb_llm = model.encode(r["llm_response"])
    emb_gold = model.encode(r["golden_answer"])
    faithfulness = cosine_similarity([emb_llm], [emb_gold])[0][0]
    faithfulness_scores.append(faithfulness)
    
    # Answer relevancy: (pergunta + LLM response) vs (pergunta + golden answer)
    emb_llm_rel = model.encode(r["question"] + " " + r["llm_response"])
    emb_gold_rel = model.encode(r["question"] + " " + r["golden_answer"])
    relevancy = cosine_similarity([emb_llm_rel], [emb_gold_rel])[0][0]
    relevancy_scores.append(relevancy)

    report_rows.append({
        "id": r["id"],
        "question": r["question"],
        "llm_response": r["llm_response"].replace("\n", " ")[:200] + "...",
        "faithfulness": faithfulness,
        "relevancy": relevancy
    })


faithfulness_medio = sum(faithfulness_scores) / len(faithfulness_scores)
relevancy_medio = sum(relevancy_scores) / len(relevancy_scores)

#print(f"Faithfulness médio: {faithfulness_medio:.3f}")
#print(f"Answer Relevancy médio: {relevancy_medio:.3f}")

with open(OUTPUT_MD, "w", encoding="utf-8") as f:
    f.write("# Relatório de Avaliação do RAG\n\n")
    f.write("Este relatório apresenta a avaliação automática das respostas geradas pelo modelo RAG.\n\n")
    f.write(f"**Média Faithfulness:** {faithfulness_medio:.3f}\n\n")
    f.write(f"**Média Answer Relevancy:** {relevancy_medio:.3f}\n\n")

    f.write("## Tabela de Resultados por Pergunta\n\n")
    f.write("| ID | Pergunta | Resposta (resumida) | Faithfulness | Relevancy |\n")
    f.write("|----|----------|--------------------|--------------|-----------|\n")

    for row in report_rows:
        f.write(f"| {row['id']} | {row['question'][:50]}... | {row['llm_response']} | {row['faithfulness']:.2f} | {row['relevancy']:.2f} |\n")

    f.write("\n> Observação: Faithfulness indica o quanto a resposta está correta e sustentada pelas evidências.\n")
    f.write("> Relevancy indica se a resposta atende corretamente à pergunta.\n")

print(f"Relatório gerado com sucesso: {OUTPUT_MD}")