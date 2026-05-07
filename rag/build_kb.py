from pathlib import Path

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

DATA_DIR = Path("../data/laws")
INDEX_DIR = Path("vectorstore/legal_faiss")


def load_documents(data_dir: Path):
    docs = []

    if not data_dir.exists():
        raise FileNotFoundError(f"找不到目录：{data_dir}")

    for file_path in sorted(data_dir.rglob("*")):
        if not file_path.is_file():
            continue

        suffix = file_path.suffix.lower()

        try:
            if suffix == ".pdf":
                docs.extend(PyPDFLoader(str(file_path)).load())
            elif suffix == ".txt":
                docs.extend(TextLoader(str(file_path), encoding="utf-8").load())
            else:
                print(f"跳过不支持的文件：{file_path}")
        except Exception as e:
            print(f"加载失败，已跳过：{file_path}，原因：{e}")

    return docs


def main():
    print("开始加载文档...")
    documents = load_documents(DATA_DIR)
    print(f"共加载原始文档页/段数：{len(documents)}")

    if not documents:
        print("没有加载到任何文档，请先把 PDF 或 TXT 放进 data/laws/")
        return

    print("开始切分文本...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120,
        separators=["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""],
    )
    chunks = splitter.split_documents(documents)
    print(f"切分后总块数：{len(chunks)}")

    print("开始生成向量...")
    embeddings = DashScopeEmbeddings(model="text-embedding-v3")

    print("开始构建向量库...")
    vectorstore = FAISS.from_documents(chunks, embeddings)

    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(INDEX_DIR))

    print(f"知识库已保存到：{INDEX_DIR}")


if __name__ == "__main__":
    main()