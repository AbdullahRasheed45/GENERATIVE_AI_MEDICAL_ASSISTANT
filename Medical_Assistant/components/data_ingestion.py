from Medical_Assistant.components.data_preproceesing import load_pdf_file, text_split, download_embeddings
from pinecone import ServerlessSpec, Pinecone
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Check if Pinecone API key is available
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
if not PINECONE_API_KEY:
    raise ValueError("Pinecone API key not found in .env file")

# Set Pinecone API key in environment
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

# Load PDF files from directory
try:
    # Ensure the path is correct and absolute
    data_directory = os.path.abspath("../../Data/")
    extracted_data = load_pdf_file(data=data_directory)
except Exception as e:
    print(f"Error loading PDF files: {e}")
    raise

# Split text into chunks
try:
    text_chunks = text_split(extracted_data)
    print(f"Successfully split data into {len(text_chunks)} chunks")
except Exception as e:
    print(f"Error splitting text: {e}")
    raise

# Download embeddings
try:
    embeddings = download_embeddings()
    print("Embeddings successfully downloaded")
except Exception as e:
    print(f"Error downloading embeddings: {e}")
    raise

# Initialize Pinecone
try:
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index_name = "medbot-index"

    # Create or connect to a Pinecone index
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=384,  # Ensure this matches your embeddings dimension
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1",
            )
        )
        print(f"Index '{index_name}' created successfully")
    else:
        print(f"Index '{index_name}' already exists")

    # Connect to the index
    index = pc.Index(index_name)
except Exception as e:
    print(f"Error initializing Pinecone: {e}")
    raise

# Store documents in Pinecone
try:
    doc_ingestion = PineconeVectorStore.from_documents(
        documents=text_chunks,
        embedding=embeddings,
        index_name=index_name,
        text_key="text"
    )
    print("Documents successfully ingested into Pinecone")
except Exception as e:
    print(f"Error ingesting documents into Pinecone: {e}")
    raise