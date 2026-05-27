def extract_future_work(text: str):

    """
    Extract future work suggestions
    from research text.
    """

    future_keywords = [
        "future work",
        "future research",
        "can be extended",
        "in future",
        "further research",
        "future directions",
        "scope for improvement",
        "next steps"
    ]

    found_future_work = []

    for keyword in future_keywords:

        if keyword.lower() in text.lower():
            found_future_work.append(keyword)

    return {
        "future_work": found_future_work
    }