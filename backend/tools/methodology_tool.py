def extract_methodologies(text: str):

    """
    Extract methodologies from research text.
    """

    methodologies = []

    methodology_keywords = [
        "Transformer",
        "CNN",
        "RNN",
        "LSTM",
        "GAN",
        "RAG",
        "Fine-tuning",
        "Reinforcement Learning",
        "Federated Learning",
        "BERT"
    ]

    for keyword in methodology_keywords:

        if keyword.lower() in text.lower():
            methodologies.append(keyword)

    return {
        "methodologies": methodologies
    }