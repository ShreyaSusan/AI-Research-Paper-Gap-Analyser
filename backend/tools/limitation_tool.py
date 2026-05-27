def extract_limitations(text: str):

    """
    Extract limitations from research text.
    """

    limitation_keywords = [
        "limitation",
        "limitations",
        "challenge",
        "drawback",
        "computational cost",
        "small dataset",
        "overfitting",
        "high latency",
        "poor generalization",
        "scalability issue"
    ]

    found_limitations = []

    for keyword in limitation_keywords:

        if keyword.lower() in text.lower():
            found_limitations.append(keyword)

    return {
        "limitations": found_limitations
    }