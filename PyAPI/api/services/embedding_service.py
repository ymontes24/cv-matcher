from core.config import settings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from typing import List
from motor.motor_asyncio import AsyncIOMotorCollection
from api.models.embedding import Embedding

async def create_embeddings(text: str):    
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

async def insert_embeddings(collection: AsyncIOMotorCollection, doc_id: str, chunks: List[dict]):
    try:
        # Prepare the data for insertion
        documents:List[Embedding] = [
            {
                "doc_id": doc_id,
                "chunk_index": i,
                "text": chunk["text"],
                "embedding": chunk["embedding"]
            }
            for i, chunk in enumerate(chunks)
        ]

        # Insert the documents into the collection
        if documents:
            await collection.insert_many(documents)
    except Exception as e:
        print(f"An error occurred: {e}")

async def get_embeddings(collection: AsyncIOMotorCollection, doc_id: str):
    try:
        # Retrieve the embeddings for the given document ID
        cursor = collection.find({"doc_id": doc_id})
        embeddings = await cursor.to_list(length=None)
        
        # Convert the MongoDB documents to Embedding objects
        embeddings = [Embedding(**embedding) for embedding in embeddings]
        
        return embeddings
    except Exception as e:
        print(f"An error occurred: {e}")