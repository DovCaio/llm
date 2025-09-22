.PHONY: injest clean run eval

injest:
	@echo "Extraindo dados..."
	python3 -m ingest.data_extract.py
	@echo "Gerando embeddings..."
	python3 -m ingest.embbedings_generation.py

clean:
	@echo "Removendo índices e dados processados..."
	rm -rf ./data/indice_faiss
	rm -rf ./data/processed

run:
	cd ./src && streamlit run app.py

eval: 
	python3 -m eval.eval.py