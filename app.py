from memory.long_memory import (
    init_db,
    save_memory,
    get_memory,
    get_single_memory
)
import os
import json
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import FAISS

# =========================
# 基础配置
# =========================
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
INDEX_DIR = BASE_DIR / "vectorstore" / "legal_faiss"

api_key = os.getenv("DASHSCOPE_API_KEY")

llm = ChatOpenAI(
    model="qwen-plus",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=api_key,
    temperature=0.2
)

# =========================
# 加载向量库
# =========================
@st.cache_resource
def load_vectorstore():
    embeddings = DashScopeEmbeddings(model="text-embedding-v3")
    vectorstore = FAISS.load_local(
        './rag/vectorstore/legal_faiss',
        embeddings,
        allow_dangerous_deserialization=True
    )
    return vectorstore

vectorstore = load_vectorstore()

# =========================
# Prompt
# =========================
system_prompt = """
你是一名专业、严谨、克制的AI法律助手。

你需要：
1. 优先依据提供的法律知识库内容回答
2. 不要编造法律条文
3. 如果知识库中不存在相关内容，要明确说明
4. 不要假装自己是真实律师
5. 使用专业、清晰、结构化表达

以下是用户长期记忆：

{memory}

以下是检索到的法律资料：

{context}
"""
memory_extract_prompt = """
你是一个信息提取助手。

请从用户输入中提取“值得长期记忆的信息”。

只返回JSON格式。

如果没有可记忆内容，返回：

{{}}

可提取内容包括：

1. 用户姓名
2. 用户身份
3. 地区
4. 案件类型
5. 重要长期事实

JSON格式示例：

{{
    "username": "张三",
    "case_type": "劳动仲裁"
}}

用户输入：

{user_input}
"""


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder("history"),
        ("human", "{question}")
    ]
)

chain = prompt | llm

# =========================
# 页面
# =========================
st.title("⚖️ AI法律助手（RAG版）")

thread_id = st.sidebar.text_input(
    "用户ID",
    value="user_001"
)

# 初始化数据库
init_db()

if "messages" not in st.session_state:
    st.session_state.messages = []

if st.sidebar.button("清空对话"):
    st.session_state.messages = []
    st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_memory = get_memory(thread_id)
user_input = st.chat_input("请输入法律问题")

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.write(user_input)

    docs = vectorstore.similarity_search(user_input, k=4)
    context = "\n\n".join([doc.page_content for doc in docs])

    history = []
    for msg in st.session_state.messages[:-1]:
        if msg["role"] == "user":
            history.append(HumanMessage(content=msg["content"]))
        else:
            history.append(AIMessage(content=msg["content"]))

    response = chain.invoke(
        {
            "history": history,
            "question": user_input,
            "context": context,
            "memory": str(user_memory)
        }
    )

    ai_text = response.content

    # =========================
    # AI自动提取长期记忆
    # =========================

    try:

        memory_response = llm.invoke(

            memory_extract_prompt.format(
                user_input=user_input
            )

        )

        memory_text = memory_response.content.strip()

        # 去掉markdown
        memory_text = memory_text.replace("```json", "")
        memory_text = memory_text.replace("```", "")

        memory_json = json.loads(memory_text)

        if isinstance(memory_json, dict):

            for key, value in memory_json.items():
                save_memory(
                    thread_id,
                    key,
                    str(value)
                )

    except Exception as e:

        print("记忆提取失败：", e)

    st.session_state.messages.append(
        {"role": "assistant", "content": ai_text}
    )

    with st.chat_message("assistant"):
        st.write(ai_text)

    with st.expander("查看检索到的法律资料"):
        for i, doc in enumerate(docs, 1):
            st.markdown(f"### 资料 {i}")
            st.write(doc.page_content[:1000])