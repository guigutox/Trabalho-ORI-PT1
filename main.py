import fitz  # PyMuPDF
from nltk.tokenize import word_tokenize
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('rslp')

language = "portuguese"
stopwords_portuguese = set(stopwords.words(language))
new_stopwords = {'pra', 'troc', 'lá', 'tudo', 'entre', 'dos', 'ainda', 'então', 'pouco', 'cada', '...', '—', ',', ':', '?', '!', 'oh'}
stopwords_portuguese.update(new_stopwords)

#extrai o texto do PDF retorna o texto
def extrair_texto_pdf(arquivo_pdf):
    doc = fitz.open(arquivo_pdf)
    texto = ""
    
    for pagina_num in range(doc.page_count):
        pagina = doc[pagina_num]
        texto += pagina.get_text()

    return texto
#tokeniza o texto e extrai as stopwords
def tokenizar_texto_remove_stopwords(texto):
    palavras = word_tokenize(texto.lower())
    palavras = [re.sub(r'\W', '', palavra) for palavra in palavras if re.sub(r'\W', '', palavra)]

    palavras_filtradas = [palavra for palavra in palavras if palavra not in stopwords_portuguese]

    # Imprime as stopwords removidas
    stopwords_removidas = set(palavras) - set(palavras_filtradas)
    print("Stopwords Removidas:", stopwords_removidas)
    return palavras_filtradas

#metodo que lematiza as palavras
def lematizar_texto(palavras):
    stemmer = RSLPStemmer()
    palavras_lematizadas = [stemmer.stem(palavra) for palavra in palavras]
    return palavras_lematizadas

# Lista de arquivos PDF que vão ter suas palavras extraidas
arquivos_pdf = ["A_Canção_dos_tamanquinhos_Cecília_Meireles.pdf", "A_Centopeia_Marina_Colasanti.pdf", "A_porta_Vinicius_de_Moraes.pdf", "Ao_pé_de_sua_criança_Pablo_Neruda.pdf", "As_borboletas_Vinicius_de_Moraes.pdf", "Convite_José_Paulo_Paes.pdf","Pontinho_de_Vista_Pedro_Bandeira.pdf"]

# Dicionário para armazenar tokens e lematização por documento
tokens_lematizados_por_documento = {}

# Iterar sobre cada arquivo PDF
for arquivo_pdf in arquivos_pdf:

    # Envia para o metodo que extrai as palavras
    texto_pdf = extrair_texto_pdf(arquivo_pdf)
    
    # Envia para o metodo que Tokeniza o texto e extrai stopwords
    tokens_sem_stopwords = tokenizar_texto_remove_stopwords(texto_pdf)
    
    # Envia para o metodo que lematiza as palavras
    tokens_lematizados = lematizar_texto(tokens_sem_stopwords)

    # Armazenar tokens e lematização no dicionário
    tokens_lematizados_por_documento[arquivo_pdf] = {
        'tokens_sem_stopwords': tokens_sem_stopwords,
        'tokens_lematizados': tokens_lematizados
    }

# Exibindo os resultados
for arquivo_pdf, dados in tokens_lematizados_por_documento.items():
    print(f"{arquivo_pdf} -> Tokens Sem Stopwords: {dados['tokens_sem_stopwords']}")
    print(f"{' ' * len(arquivo_pdf)}   -> Tokens Lematizados: {dados['tokens_lematizados']}")
    print()
