def extract_datasets(text: str):

    """
    Extract datasets mentioned
    in research text.
    """

    dataset_keywords = [
        "ImageNet",
        "COCO",
        "MNIST",
        "CIFAR-10",
        "Wikipedia",
        "Common Crawl",
        "SQuAD",
        "LibriSpeech",
        "PubMed",
        "MMLU"
    ]

    found_datasets = []

    for dataset in dataset_keywords:

        if dataset.lower() in text.lower():
            found_datasets.append(dataset)

    return {
        "datasets": found_datasets
    }