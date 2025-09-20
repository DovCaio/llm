from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.load_local("../data/indice_faiss", embeddings, allow_dangerous_deserialization=True)
#retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 4})

def retriever_agent(query: str):
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k":4})
    return retriever

def response_with_quotes(query: str, docs: list):
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
        retriever=docs,
        return_source_documents=True,  
        chain_type_kwargs={"prompt": prompt},
    )

    res = qa(query)
    result = res["result"]
    quotes = [f"- {doc.metadata.get('source')}" for doc in res["source_documents"]]
    #all_quotes = "\n".join(quotes)

    response = f"""
{result}
    """
    return (response, res["source_documents"])


def self_check(answer: str, docs: list):
    """Verifica se cada sentença da resposta está suportada pelos documentos."""
    llm_sc = OllamaLLM(model="phi3:mini")

    context_text = "\n\n".join(doc.page_content for doc in docs)

    prompt_sc = PromptTemplate(
        input_variables=["answer", "context"],
        template="""
Analise se cada sentença da RESPOSTA está suportada pelos trechos do CONTEXTO.
Caso não, dê um feedback de como melhorar, Do contrário diga somente que: ESTÁ TUDO CERTO

RESPOSTA:
{answer}

CONTEXTO:
{context}
"""
    )

    chain_sc = LLMChain(llm=llm_sc, prompt=prompt_sc)
    return chain_sc.run({"answer": answer, "context": context_text})

def safety_agent(answer: str):
    disclaimer = "O conteúdo apresentado aqui, incluindo informações, análises e discussões, tem finalidade estritamente informativa e educacional. Ele não constitui, e não deve ser interpretado como, aconselhamento jurídico, financeiro, político ou de qualquer outra natureza profissional."
    return f"{answer}\n\n{disclaimer}"


if __name__ == "__main__": #Só para fazer um teste rápido
    query = "Quais são os direitos fornecidos a pessoas idosas?"

    docs = retriever_agent(query)

    response = response_with_quotes(query, docs)
    print(response[0])

    print("-----------------Verficação-----------------")

    check = self_check(response, response[1])
    print(check)
