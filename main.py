import fitz  # PyMuPDF
from nltk.tokenize import word_tokenize
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
import spacy
from collections import Counter

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('rslp')
nlp = spacy.load('pt_core_news_sm')

language = "portuguese"
stopwords_portuguese = set(stopwords.words(language))
new_stopwords = {'pra', 'troc', 'lá', 'tudo', 'entre', 'dos', 'ainda',
                 'então', 'pouco', 'cada', '...', '—', ',', ':', '?', '!', 'oh'}
stopwords_portuguese.update(new_stopwords)

# extrai o texto do PDF retorna o texto


def extrair_texto_pdf(arquivo_pdf):
    doc = fitz.open(arquivo_pdf)
    texto = ""

    for pagina_num in range(doc.page_count):
        pagina = doc[pagina_num]
        texto += pagina.get_text()

    return texto

# tokeniza o texto e extrai as stopwords


def tokenizar_texto_remove_stopwords(texto):
    palavras = word_tokenize(texto.lower())
    palavras = [re.sub(r'\W', '', palavra)
                for palavra in palavras if re.sub(r'\W', '', palavra)]

    palavras_filtradas = [
        palavra for palavra in palavras if palavra not in stopwords_portuguese]

    # Imprime as stopwords removidas
    stopwords_removidas = set(palavras) - set(palavras_filtradas)
    print("Stopwords Removidas:", stopwords_removidas)
    return palavras_filtradas

# metodo que lematiza e steemiza as palavras


def steemizar_lematizar_texto(palavras):
    stemmer = RSLPStemmer()
    palavras_stemmizadas_lematizadas = []

    for palavra in palavras:
        # Stemming
        stem = stemmer.stem(palavra)

        # Lematização
        doc = nlp(palavra)
        lema = doc[0].lemma_ if doc[0].lemma_ != '-PRON-' else palavra
        palavras_stemmizadas_lematizadas.append((palavra, lema, stem))

    return palavras_stemmizadas_lematizadas


# Lista de arquivos PDF que vão ter suas palavras extraídas
arquivos_pdf = ["A_Canção_dos_tamanquinhos_Cecília_Meireles.pdf", "A_Centopeia_Marina_Colasanti.pdf", "A_porta_Vinicius_de_Moraes.pdf",
                "Ao_pé_de_sua_criança_Pablo_Neruda.pdf", "As_borboletas_Vinicius_de_Moraes.pdf", "Convite_José_Paulo_Paes.pdf", "Pontinho_de_Vista_Pedro_Bandeira.pdf"]

# Dicionário para armazenar tokens, lematização e frequência por documento e no corpus
tokens_info_por_documento = {}

# Lista de todas as palavras únicas e suas contagens no corpus
palavras_no_corpus = Counter()

# ID para documentos
doc_id_counter = 1

# Iterar sobre cada arquivo PDF
for arquivo_pdf in arquivos_pdf:

    # Envia para o método que extrai as palavras
    texto_pdf = extrair_texto_pdf(arquivo_pdf)

    # Envia para o método que Tokeniza o texto e extrai stopwords
    tokens_sem_stopwords = tokenizar_texto_remove_stopwords(texto_pdf)

    # Envia para o método que lematiza as palavras
    tokens_lematizados = steemizar_lematizar_texto(tokens_sem_stopwords)

    # Atualizar contagem no corpus
    palavras_no_corpus.update(tokens_lematizados)

    # Armazenar tokens, lematização e frequência no documento no dicionário
    tokens_info_por_documento[doc_id_counter] = {
        'arquivo_pdf': arquivo_pdf,
        'tokens_sem_stopwords': tokens_sem_stopwords,
        'tokens_lematizados': tokens_lematizados,
        'frequencia_no_documento': Counter(tokens_lematizados)
    }

    # Incrementar o ID do documento
    doc_id_counter += 1

# Exibindo os resultados
# ...

# Exibindo os resultados
for doc_id, dados in tokens_info_por_documento.items():
    print(f"ID {doc_id} - {dados['arquivo_pdf']}")
    print("   -> Tokens Sem Stopwords:")
    # ...

    print()

# Exibindo a frequência no corpus
print("Frequência no Corpus:")
for palavra, freq in palavras_no_corpus.items():
    documentos_com_palavra = []

    for doc_id, dados in tokens_info_por_documento.items():
        if palavra in dados['frequencia_no_documento']:
            freq_no_documento = dados['frequencia_no_documento'][palavra]
            documentos_com_palavra.append(f"{doc_id}/{freq_no_documento}")

    if documentos_com_palavra:
        documentos_str = ', '.join(documentos_com_palavra)
        print(f"   -> {palavra} -> {documentos_str}")


# Exibindo a frequência no corpus
# print("Frequência no Corpus:")
# for palavra, freq in palavras_no_corpus.items():
 #   print(f"   -> {palavra} -> {', '.join([f'{doc_id}/{freq}' for doc_id, freq in dados['frequencia_no_documento'].ite()])}")
        


# Nome do arquivo PDF de saída
output_pdf = "output_resultados.pdf"

# Criação do documento PDF
pdf_doc = fitz.open()

# Exibindo a frequência no corpus
page = pdf_doc.new_page(width=500, height=700)  # Adiciona uma nova página

# Definindo a posição inicial y
y_position = 50

page.insert_text((50, y_position), "Frequência no Corpus:\n")
y_position += 20  # Ajuste conforme necessário

for palavra, freq in palavras_no_corpus.items():
    documentos_com_palavra = []

    for doc_id, dados in tokens_info_por_documento.items():
        if palavra in dados['frequencia_no_documento']:
            freq_no_documento = dados['frequencia_no_documento'][palavra]
            documentos_com_palavra.append(f"{doc_id}/{freq_no_documento}")

    if documentos_com_palavra:
        documentos_str = ', '.join(documentos_com_palavra)

        # Verifica se é necessário adicionar uma nova página
        if y_position > 650:
            page = pdf_doc.new_page(width=500, height=700)
            y_position = 50

        page.insert_text((50, y_position), f"   -> {palavra} -> {documentos_str}\n")
        y_position += 20  # Ajuste conforme necessário

# Salvar o documento PDF
pdf_doc.save(output_pdf)