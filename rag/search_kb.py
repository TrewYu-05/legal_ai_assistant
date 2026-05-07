from dotenv import load_dotenv
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

INDEX_DIR = "vectorstore/legal_faiss"


def main():
    embeddings = DashScopeEmbeddings(model="text-embedding-v3")

    vectorstore = FAISS.load_local(
        INDEX_DIR,
        embeddings,
        allow_dangerous_deserialization=True,
    )

    query = "劳动合同试用期最长多久？"
    results = vectorstore.similarity_search(query, k=4)

    print(f"查询：{query}")
    print("=" * 60)

    for i, doc in enumerate(results, 1):
        print(f"【结果 {i}】")
        print("来源：", doc.metadata)
        print(doc.page_content[:500])
        print("-" * 60)


if __name__ == "__main__":
    main()