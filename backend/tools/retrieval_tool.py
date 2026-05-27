from knowledge.knowledge_base import knowledge_base


def retrieve_chunks(query: str):

    """
    Retrieve semantically relevant chunks
    from the knowledge base.
    """

    results = knowledge_base.search(
        query=query
    )

    return results