.PHONY: injest clean run

injest:
	@echo "Extraindo dados..."
	@echo "Gerando embeddings..."
	python3 -m ingest.embbedings_generation.py

clean:
	@echo "Removendo índices e dados processados..."
	rm -rf ./data/indice_faiss
	rm -rf ./data/processed

run:
	cd ./src && streamlit run app.py