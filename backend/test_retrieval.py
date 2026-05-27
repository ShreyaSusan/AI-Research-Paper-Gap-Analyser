from tools.retrieval_tool import retrieve_chunks


results = retrieve_chunks(
    query="What methodologies are discussed?"
)

print("\nRETRIEVED CHUNKS:\n")

for result in results:
    print(result)
    print("\n-----------------\n")