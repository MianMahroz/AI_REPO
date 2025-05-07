import sqlite3
import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict

class IssueDatabase:
    def __init__(self):
        self.conn = sqlite3.connect("issues.db")
        self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
        self.embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        self.collection = self.chroma_client.get_or_create_collection(
            name="issues",
            embedding_function=self.embedding_func
        )

    def init_db(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS issues (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT,
                error_message TEXT,
                resolution TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def insert_emails(self, emails: List[Dict]):
        cursor = self.conn.cursor()
        for email in emails:
            cursor.execute(
                "INSERT INTO issues (subject, error_message, resolution) VALUES (?, ?, ?)",
                (email["subject"], email["error_message"], email.get("resolution", ""))
            self.collection.add(
                documents=email["error_message"],
                metadatas={"subject": email["subject"], "resolution": email.get("resolution", "")},
                ids=str(cursor.lastrowid)
            )
        self.conn.commit()

    def semantic_search(self, query: str, k=3) -> List[Dict]:
        results = self.collection.query(
            query_texts=[query],
            n_results=k
        )
        issues = []
        for i in range(len(results["ids"][0])):
            issues.append({
                "subject": results["metadatas"][0][i]["subject"],
                "error_message": results["documents"][0][i],
                "resolution": results["metadatas"][0][i]["resolution"]
            })
        return issues

    def get_recent_issues(self, limit=10):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM issues ORDER BY created_at DESC LIMIT ?", (limit,))
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]