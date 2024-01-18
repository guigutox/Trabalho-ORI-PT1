

import fitz  # PyMuPDF
from nltk.tokenize import word_tokenize
import re
import nltk
from nltk.corpus import stopwords
import nltk

nltk.download('stopwords')
nltk.download('punkt')

language = "portuguese"

    
def extrair_texto_pdf(arquivo_pdf):
    doc = fitz.open(arquivo_pdf)
    texto = ""
    
    for pagina_num in range(doc.page_count):
        pagina = doc[pagina_num]
        texto += pagina.get_text()

    return texto

def tokenizar_texto(texto):
    palavras = word_tokenize(texto.lower())
    palavras = [re.sub(r'\W', '', palavra) for palavra in palavras if re.sub(r'\W', '', palavra)]

    palavras_filtradas = [palavra for palavra in palavras if palavra not in stopwords.words(language)]
    return palavras_filtradas

# Lista de arquivos PDF
arquivos_pdf = ["A_Canção_dos_tamanquinhos_Cecília_Meireles.pdf", "A_Centopeia_Marina_Colasanti.pdf", "A_porta_Vinicius_de_Moraes.pdf", "Ao_pé_de_sua_criança_Pablo_Neruda.pdf", "As_borboletas_Vinicius_de_Moraes.pdf", "Convite_José_Paulo_Paes.pdf","Pontinho_de_Vista_Pedro_Bandeira.pdf"]

# Dicionário para armazenar tokens por documento
tokens_por_documento = {}

# Iterar sobre cada arquivo PDF
for arquivo_pdf in arquivos_pdf:
    # Extrair texto do PDF
    texto_pdf = extrair_texto_pdf(arquivo_pdf)
    
    # Tokenizar o texto
    tokens = tokenizar_texto(texto_pdf)
    
    # Armazenar tokens no dicionário
    tokens_por_documento[arquivo_pdf] = tokens

# Exibindo os tokens de cada documento
for arquivo_pdf, tokens in tokens_por_documento.items():
    print(f"{arquivo_pdf} -> {tokens}")
