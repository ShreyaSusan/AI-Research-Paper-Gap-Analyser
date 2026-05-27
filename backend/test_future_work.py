from tools.future_work_tool import extract_future_work


sample_text = """
Future work can focus on improving scalability
and extending the framework to multilingual datasets.
Further research is needed for real-world deployment.
"""


result = extract_future_work(sample_text)

print(result)