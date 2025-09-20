# Assistente RAG + Agentes (Assunto: Justiça social)

Resumo
-------
PoC open-source que indexa documentos públicos e responde com citações + self-check. Stack: Python, LangChain, LangGraph, FAISS/Chroma, Ollama (local), Streamlit.

Status
------
- Prova de conceito funcional — demo local
- Licença: MIT

Instalação requisitos
------------------
```bash
# python venv
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
Caso não tenha os dados processados
------------------------------------
```bash
cd ingest
make injest
```
Execução
---------
```bash
cd src
make run
```
