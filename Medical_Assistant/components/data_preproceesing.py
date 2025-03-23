from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.embeddings import HuggingFaceEmbeddings


def load_pdf_file(data):
    loader = DirectoryLoader(data,
                             glob="*.pdf",
                             loader_cls=PyPDFLoader)
    documents = loader.load()

    return documents



def text_split(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size= 500, chunk_overlap=20)
    text_chunks = text_splitter.split_documents(extracted_data)
    return text_chunks

def download_embeddings():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return embeddings

#doc_1 = PyPDFLoader("./Data/Gale Encyclopedia of Medicine. Vol. 5. 2nd ed.pdf").load()##
#doc_2 = PyPDFLoader("./Data/Gale Encyclopedia of Medicine Vol. 3 (G-M).pdf").load()
#doc_3 = PyPDFLoader("./Data/Gale Encyclopedia of Medicine Vol. 4 (N-S).pdf").load()
#doc_4 = PyPDFLoader("./Data/The_GALE_ENCYCLOPEDIA_of_MEDICINE_SECOND.pdf").load()
#doc_5 = PyPDFLoader("./Data/The_GALE_ENCYCLOPEDIA_of_MEDICINE_SECOND (1).pdf").load()

#text_chunks_1 = text_split(doc_1)
#text_chunks_2 = text_split(doc_2)
#text_chunks_3 = text_split(doc_3)
#text_chunks_4 = text_split(doc_4)
#text_chunks_5 = text_split(doc_5)