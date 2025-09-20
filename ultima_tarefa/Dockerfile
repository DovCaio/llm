FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://ollama.com/install.sh | sh

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

WORKDIR /app/src

CMD ollama serve & \
    sleep 3 && \
    ollama pull mistral:latest && \
    ollama pull phi3:mini && \
    streamlit run app.py --server.port=8501 --server.address=0.0.0.0