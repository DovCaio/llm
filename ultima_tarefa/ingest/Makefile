.PHONY: injest clean

injest:
	@echo "Extraindo dados..."
	python3 data_extract.py
	@echo "Gerando embeddings..."
	python3 embbedings_generation.py

clean:
	@echo "Removendo índices e dados processados..."
	rm -f ../data/indices_faiss
	rm -f ../data/processed