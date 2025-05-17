from core.config import settings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

async def create_embeddings(text: str):    
    # Split the text into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP
    )

    chunks = text_splitter.split_text(text)
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectors = embedding_model.embed_documents(chunks)
    
    documents = []
    for chunk, vector in zip(chunks, vectors):
        doc = {
            "text": chunk,
            "embedding": vector
        }
        documents.append(doc)
    
    return documents