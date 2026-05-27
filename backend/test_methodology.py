from tools.methodology_tool import extract_methodologies


sample_text = """
This paper uses Transformer architecture with
Retrieval-Augmented Generation (RAG)
and Fine-tuning techniques.
"""


result = extract_methodologies(sample_text)

print(result)