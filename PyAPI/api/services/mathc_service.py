from db.mongodb import mongodb
from core.logging import app_logger
from api.services.embedding_service import get_embeddings
from collections import defaultdict
from bson import ObjectId

async def match_cv(
        doc_id: str,
        top_k: int = 3,
        score_threshold: float = 0.75,
        min_matches: int = 4,
        ):
    try:
        # Retrieve the embeddings for the given document ID
        chunk_embeddings = await get_embeddings(mongodb.db['job_description_embeddings'], doc_id)

        all_results = []

        for chunk_vector in chunk_embeddings:
            pipeline = [
                {
                    "$vectorSearch": {
                        "index": "vector_index",
                        "path": "embedding",
                        "queryVector": chunk_vector.embedding,
                        "numCandidates": 100,
                        "limit": 3,
                        "similarity": "cosine"
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "doc_id": 1,
                        "text": 1,
                        "score": {"$meta": "vectorSearchScore"}
                    }
                }
            ]

            chunk_results = await mongodb.db['cv_embeddings'].aggregate(pipeline).to_list(length=3)
            all_results.extend(chunk_results)

        grouped = defaultdict(list)
        for r in all_results:
            grouped[r["doc_id"]].append(r)

        filtered_matches = []
        for doc_id, chunks in grouped.items():
            high_score_chunks = [c for c in chunks if c["score"] >= score_threshold]

            if len(high_score_chunks) >= min_matches:
                avg_score = sum(c["score"] for c in high_score_chunks) / len(high_score_chunks)
                filtered_matches.append({
                    "doc_id": doc_id,
                    "score": avg_score,
                    "text": [c["text"] for c in high_score_chunks],
                    "match_count": len(high_score_chunks),
                })

        filtered_matches.sort(key=lambda x: x["score"], reverse=True) 
        result = []
        for doc in filtered_matches[:top_k]:
            mongo_doc = await mongodb.db['cvs'].find_one({"_id": ObjectId(doc["doc_id"])}, {"candidate_name": 1})
            doc["candidate_name"] = mongo_doc.get("candidate_name") if mongo_doc else None
            result.append(doc)
            
        return result

    except Exception as e:
        app_logger.error(f"Error retrieving job description embeddings: {e}")
        raise e
    