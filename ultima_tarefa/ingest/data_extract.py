import requests
from bs4 import BeautifulSoup
import os
import re

save_in = "./data/data_for_rag"
processing_put_on = "./data/processed"

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

def exist_directory(dir):
    os.makedirs(dir, exist_ok=True)


def exist_file(path):
    return os.path.isfile(path)

from pathlib import Path
import pdfplumber

def extract_text_from_pdf(path: Path) -> str:
    texts = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            texts.append(text)
    return " ".join(texts)


def save_text_to_file(text, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text)

REPROCESSING = True

def process_pdf():
  for filename in os.listdir(save_in):
      save_path = f"{save_in}/{filename}"
      path_txt = f"{processing_put_on}/{filename.split('.')[0]}.txt"
      if not exist_file(path_txt) or REPROCESSING:
        text = extract_text_from_pdf(save_path)
        save_text_to_file(text, path_txt)

process_pdf()