from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vectorstore = FAISS.load_local("indice_faiss", embeddings, allow_dangerous_deserialization=True)

retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 4})

llm = OllamaLLM(model="mistral:latest")


template = """
Você é um assistente informativo.
Use **somente** os trechos fornecidos abaixo para responder.
Mostre sempre as citações (as urls dos pdf's).
Se não encontrar evidência suficiente, diga que não sabe.

Contexto:
{context}

Pergunta: {question}
"""

prompt = PromptTemplate(
    template=template,
    input_variables=["context", "question"]
)

qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True,  
    chain_type_kwargs={"prompt": prompt},
)

query = "Quais são os direitos básicos do cidadão segundo o guia?"
res = qa(query)

print("Resposta:")
print(res["result"])

print("\nCitações:")
for doc in res["source_documents"]:
    print(f"- {doc.metadata.get('source')}")