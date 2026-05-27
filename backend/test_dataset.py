from tools.dataset_tool import extract_datasets


sample_text = """
The model was evaluated on ImageNet,
COCO, and MMLU benchmarks for performance analysis.
"""


result = extract_datasets(sample_text)

print(result)