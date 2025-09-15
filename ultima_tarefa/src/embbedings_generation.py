from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os

pdfs_urls = [
    "https://www.defensoriapublica.pr.def.br/sites/default/arquivos_restritos/files/migrados/File/Cartilha/CARTILHADIREITOSHUMANOSDIGITAL.pdf",
    "https://www.defensoria.df.gov.br/wp-content/uploads/2023/01/Cartilha-Os-Direitos-da-Crianca-e-do-Adolescente.pdf",
    "https://www.sda.ce.gov.br/wp-content/uploads/sites/60/2018/10/cartilha_cidadania_direito_ter_direitos.pdf",
    "https://www.anadep.org.br/wtksite/CARTILHA_2025(1).pdf",
    "https://www.anadep.org.br/wtksite/CARTILHA_CAMPANHA_24-DIGITAL.pdf",
    "https://www.anadep.org.br/wtksite/CARTILHA_2023(1).pdf",
    "https://www.anadep.org.br/wtksite/CARTILHA_DIGITAL_(2).pdf",
    "https://www.anadep.org.br/wtksite/CARTILHA-DIGITAL(1).pdf",
    "https://www.anadep.org.br/wtksite/CARTILHA_LGBT.pdf",
    "https://www.anadep.org.br/wtksite/CARTILHA_ANADEP_CONDEGE_ONLINE.pdf",
    "https://www.anadep.org.br/wtksite/CARTILHA_MULHERES-3(2).pdf",
    "https://www.anadep.org.br/wtksite/CARTILHA_ANADEP_CONDEGE.pdf",
    "https://direitoshumanos.dpu.def.br/wp-content/uploads/2024/06/Protocolo_GTCEC_2106.pdf",
    "https://direitoshumanos.dpu.def.br/wp-content/uploads/2025/05/Cartilha_Endividamento_Pessoa_Idosa_2025.pdf",
    "https://direitoshumanos.dpu.def.br/wp-content/uploads/2025/05/Guia_Pr_C3_A1tico_de_Rotinas_Administrativas_das_Defensorias_Regionais_v2.pdf",
    "https://direitoshumanos.dpu.def.br/wp-content/uploads/2025/04/guia_de_orientacao_comissoes_de_heteroidentificacao_etnico_racial_versaofinal_menor.pdf",
    "https://direitoshumanos.dpu.def.br/wp-content/uploads/2025/04/agenda_projeto_redd.pdf",
    "https://direitoshumanos.dpu.def.br/wp-content/uploads/2025/03/Cartilha-Pensao-especial-para-filhas-e-filhos-de-vitimas-de-feminicidio.pdf",
    "https://direitoshumanos.dpu.def.br/wp-content/uploads/2025/03/DPU-cartilha-Assedio-moral-e-sexual-v4-pgs-indiv.pdf"
]



def extract_text_from_file(path: str) -> str:
    texts = ""
    with open(path, "r") as file:
        texts += file.read()
    return texts

def transform_into_chunks():
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,      
        chunk_overlap=50   
    )
    
    all_chunks = []
    for filename in os.listdir("./data"):
        path = Path("./data") / filename

        if not path.is_file() or not filename.lower().endswith(".txt"):
            continue

        text = extract_text_from_file(str(path))

        pieces = splitter.split_text(text)
        
        url = next((value for value in pdfs_urls if filename.replace(".txt", "") in value), "")
        for piece in pieces:
            all_chunks.append({
                "content": piece,
                "source": url
            })

    return all_chunks

chunks = transform_into_chunks()
texts = [c["content"] for c in chunks]
metadatas = [{"source": c["source"]} for c in chunks]

print("Qtd de chunks:", len(chunks))
print("Qtd de texts:", len(texts))
print("Primeiro texto:", texts[0] if texts else "Nenhum texto")

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vectorstore = FAISS.from_texts(
    texts,
    embedding=embeddings,
    metadatas=metadatas
)

vectorstore.save_local("indice_faiss")

def test(query = "Quais são os direitos garantidos às pessoas idosas?"):
    docs = vectorstore.similarity_search(query, k=3)

    for i, doc in enumerate(docs, 1):
        print(doc.metadata)
        print(f"\nTrecho {i}:\n", doc.page_content)

test()  