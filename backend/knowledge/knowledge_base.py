from agno.knowledge import Knowledge
from agno.vectordb.pgvector import PgVector

from knowledge.local_embedder import LocalEmbedder

DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/researchdb"

vector_db = PgVector(
    table_name="research_knowledge",

    db_url=DATABASE_URL,

    embedder=LocalEmbedder(),
)

knowledge_base = Knowledge(
    vector_db=vector_db
)