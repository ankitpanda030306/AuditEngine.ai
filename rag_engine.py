from typing import List, Dict, Any, Optional
import chromadb
from sentence_transformers import SentenceTransformer

class VectorRAGEngine:
    def __init__(self):
        # 1. Initialize local Hugging Face Sentence Transformer model
        self.encoder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        
        # 2. Setup in-memory ChromaDB vector client
        self.chroma_client = chromadb.Client()
        self.collection = self.chroma_client.get_or_create_collection(
            name="audit_guidelines",
            metadata={"hnsw:space": "cosine"}
        )
        
        # 3. Seed technical governance knowledge base
        self._seed_knowledge_base()

    def _seed_knowledge_base(self):
        documents = [
            "Rule SEC-01: High login failure anomalies indicate brute force attacks. Remediate by enabling IP rate-limiting, WAF rules, and enforcing MFA.",
            "Rule NET-02: Public ingress topologies must terminate TLS at the load balancer and restrict open ports 22/3389 using security groups.",
            "Rule DB-03: Distributed database clusters require encrypted at-rest EBS volumes, multi-AZ failover, and strict VPC peering isolation.",
            "Rule RES-04: CPU and memory spikes beyond 85% with abnormal request bursts require auto-scaling policies and DDoS protection via Cloudflare/CloudFront.",
            "Rule IAM-05: Root access credentials detected in deployment templates. Enforce least-privilege IAM roles and rotate access tokens immediately."
        ]
        doc_ids = ["SEC-01", "NET-02", "DB-03", "RES-04", "IAM-05"]
        
        embeddings = self.encoder.encode(documents).tolist()
        self.collection.add(
            ids=doc_ids,
            documents=documents,
            embeddings=embeddings
        )

    def add_custom_document(self, doc_id: str, document_text: str):
        """Allows users to dynamically upload new security policies."""
        embedding = self.encoder.encode([document_text]).tolist()
        self.collection.add(ids=[doc_id], documents=[document_text], embeddings=embedding)

    def retrieve_guidelines(self, query: str, top_k: int = 2) -> List[Dict[str, Any]]:
        """Encodes query and returns documents with cosine similarity scores."""
        query_vector = self.encoder.encode([query]).tolist()
        results = self.collection.query(
            query_embeddings=query_vector,
            n_results=top_k,
            include=["documents", "distances"]
        )
        
        matched_items: List[Dict[str, Any]] = []
        docs = results.get("documents")
        dists = results.get("distances")
        
        if docs is not None and dists is not None and len(docs) > 0 and len(dists) > 0:
            for doc, dist in zip(docs[0], dists[0]):
                similarity = round((1.0 - float(dist)) * 100, 2)
                matched_items.append({"rule": str(doc), "similarity_pct": similarity})
                
        return matched_items

if __name__ == "__main__":
    rag = VectorRAGEngine()
    res = rag.retrieve_guidelines("Unauthorized login access and high traffic")
    print("Advanced RAG Matches with Similarity Scores:")
    for r in res:
        print(f"[{r['similarity_pct']}% Match] -> {r['rule']}")