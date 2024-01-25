import fitz  # PyMuPDF
from nltk.tokenize import word_tokenize
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
import spacy
from collections import Counter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


nltk.download('stopwords')
nltk.download('punkt')
nltk.download('rslp')
nlp = spacy.load('pt_core_news_sm')

language = "portuguese"
stopwords_portuguese = set(stopwords.words(language))
new_stopwords = {'pra', 'troc', 'lá', 'tudo', 'entre', 'dos', 'ainda',
                 'então', 'pouco', 'cada', '...', '—', ',', ':', '?', '!', 'oh', 
                 'antes', 'cem', 'algum', 'então', 'outro', 'tanto', 'vamos', 'sempre', 'cada',
                'todo', 'ia', 'manca', 'vivo', 'tudo'}
stopwords_portuguese.update(new_stopwords)

# Extrai o texto do PDF e retorna o texto
def extrair_texto_pdf(arquivo_pdf):
    doc = fitz.open(arquivo_pdf)
    texto = ""

    for pagina_num in range(doc.page_count):
        pagina = doc[pagina_num]
        texto += pagina.get_text()

    return texto

# Tokeniza o texto e extrai as stopwords
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

# Método que lematiza e stemiza as palavras, com exceções
def steemizar_lematizar_texto(palavras, evitar_stemizacao, excecoes_stemming, excecoes_lematizacao):
    stemmer = RSLPStemmer()
    palavras_stemmizadas_lematizadas = []

    for palavra in palavras:
        # Lematização
        doc = nlp(palavra)
        lema = doc[0].lemma_ if doc[0].lemma_ != '-PRON-' else palavra

        if lema.lower() in evitar_stemizacao:
            stem = lema  # Mantém a palavra original
        elif lema.lower() in excecoes_stemming:
            stem = excecoes_stemming[lema.lower()]  # Usa a exceção de stemmização
        else:
            # Executa a stemização normalmente
            stem = stemmer.stem(palavra)

        if lema.lower() in excecoes_lematizacao:
            lema = excecoes_lematizacao[lema.lower()]  # Usa a exceção de lematização

        palavras_stemmizadas_lematizadas.append((palavra, lema, stem))

    return palavras_stemmizadas_lematizadas

# Lista de palavras a evitar a stemização
palavras_a_evitar_stemizacao = ['azul', 'morta']

# Lista de exceções para stemming
excecoes_stemming = {
    'tamanquinh': 'tamanc',
    'entã': 'entao',
    'pé': 'pe',
    'pés': 'pe',
    'piã': 'piao',
    'águ': 'agua',
    'maçã': 'maca',
    'amarelinha': 'amarel',
    'bonitinh': 'bonit',
    'escuridã': 'escur',
    'silênci': 'silenci',
    'bichinh': 'bich',
    'matér': 'mater',
    'devagarinh': 'devag',
    'menininh': 'menin',
    'céu': 'ceu',
    'chã': 'chao',
    'grandã': 'grand',
    'ligeirinh': 'ligeir',
    'man':'manei',
    'capitão':'capit',
    'ir':'ir',
    'vizinho':'vizi',
    'ter':'ter',
}

# Lista de exceções para lematização
excecoes_lematizacao = {
    'ligeirinho':'ligeiro',
    'tamanquinho':'tamanco',
    'madrugar':'madruga',
    'ideiar':'ideia',
    'centopeiar':'centopeia',
    'patar':'pato',
    'fazer':'feito',
    'abrar':'abrir',
    'davagarinho':'devagar',
    'menininho': 'menino',
    'namorar':'namorado',
    'aberta':'aberto',
    'frutar': 'fruta',
    'redondar':'redondo',
    'condenar':'condenado',
    'encerrar':'encerrado',
    'amararelinha':'amarelo',
    'bonitinha':'bonita',
    'bolo':'bola',
    'vir':'ver'
}

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
    tokens_lematizados = steemizar_lematizar_texto(tokens_sem_stopwords, palavras_a_evitar_stemizacao, excecoes_stemming, excecoes_lematizacao)

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
for doc_id, dados in tokens_info_por_documento.items():
    print(f"ID {doc_id} - {dados['arquivo_pdf']}")
    print("   -> Tokens Sem Stopwords:")
    print()

print("Frequência no Corpus:")
for palavra, freq in palavras_no_corpus.items():
    documentos_com_palavra = []

    # Soma total da frequência da palavra no corpus
    freq_total_corpus = sum(dados['frequencia_no_documento'][palavra] for dados in tokens_info_por_documento.values() if palavra in dados['frequencia_no_documento'])

    for doc_id, dados in tokens_info_por_documento.items():
        if palavra in dados['frequencia_no_documento']:
            freq_no_documento = dados['frequencia_no_documento'][palavra]
            documentos_com_palavra.append(f"{doc_id}/{freq_no_documento}")

    if documentos_com_palavra:
        documentos_str = ', '.join(documentos_com_palavra)
        print(f"   -> {palavra} -> {documentos_str} -> Total no Corpus: {freq_total_corpus}")





# Função para gerar o PDF com os resultados
def gerar_pdf(tokens_info_por_documento, palavras_no_corpus, output_file):
    # Inicializa o objeto canvas para gerar o PDF
    c = canvas.Canvas(output_file, pagesize=letter)
    width, height = letter

    # Define o tamanho da fonte
    c.setFont("Helvetica", 12)

    # Adiciona manualmente os IDs e nomes dos documentos na primeira página
    documentos = {
        1: "A_Cancao_dos_tamanquinhos_Cecilia_Meireles.pdf",
        2: "A_Centopeia_Marina_Colasanti.pdf",
        3: "A_porta_Vinicius_de_Moraes.pdf",
        4: "Ao_pe_de_sua_crianca_Pablo_Neruda.pdf",
        5: "As_borboletas_Vinicius_de_Moraes.pdf",
        6: "Convite_Jose_Paulo_Paes.pdf",
        7: "Pontinho_de_Vista_Pedro_Bandeira.pdf"
    }

    y_offset = height - 50  # Posição vertical inicial
    for doc_id, arquivo_pdf in documentos.items():
        c.drawString(100, y_offset, f"ID {doc_id} - {arquivo_pdf}")
        y_offset -= 15  # Move para a próxima linha

    # Pula para a próxima página
    c.showPage()

    # Adiciona a frequência no corpus na nova página
    c.drawString(100, height - 50, "Frequência no Corpus:")
    y_offset = height - 70  # Posição vertical inicial

    for palavra, freq in palavras_no_corpus.items():
        freq_total_corpus = sum(1 for dados in tokens_info_por_documento.values() if palavra in dados['frequencia_no_documento'])
        if freq_total_corpus > 0:
            documentos_str = ', '.join(f"{doc_id}/{dados['frequencia_no_documento'].get(palavra, 0)}" for doc_id, dados in tokens_info_por_documento.items() if palavra in dados['frequencia_no_documento'])
            c.drawString(100, y_offset, f"{palavra}/{freq_total_corpus} -> {documentos_str}")
            y_offset -= 15  # Move para a próxima linha
            if y_offset < 50:
                c.showPage()  # Nova página se não houver espaço suficiente
                c.drawString(100, height - 50, "Frequência no Corpus:")
                y_offset = height - 70  # Redefine a posição vertical

    # Salva o PDF
    c.save()

# Chama a função para gerar o PDF
gerar_pdf(tokens_info_por_documento, palavras_no_corpus, "resultados.pdf")
