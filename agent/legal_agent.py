from typing import TypedDict

from langgraph.graph import StateGraph
from langgraph.graph import END

from langchain_core.messages import (
    HumanMessage,
    AIMessage
)

from langgraph.checkpoint.memory import InMemorySaver

# =========================
# Memory
# =========================

memory = InMemorySaver()

# =========================
# Agent State
# =========================

class AgentState(TypedDict):

    question: str

    context: str

    answer: str

    history: list

# =========================
# Agent Node
# =========================

def chat_node(state, llm, vectorstore):

    question = state["question"]

    # =========================
    # RAG 检索
    # =========================

    docs = vectorstore.similarity_search(
        question,
        k=4
    )

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    # =========================
    # 构建消息
    # =========================

    messages = [

        (
            "system",
            f"""
你是一名专业法律AI助手。

请严格基于以下法律资料回答：

{context}

要求：
1. 不要编造法律条文
2. 如果资料不足，请明确说明
3. 回答结构化
4. 保持专业严谨
"""
        )
    ]

    # 加入历史记录
    messages.extend(state["history"])

    # 加入当前问题
    messages.append(
        HumanMessage(content=question)
    )

    # =========================
    # 调用模型
    # =========================

    response = llm.invoke(messages)

    answer = response.content

    # 更新历史记录
    new_history = state["history"] + [
        HumanMessage(content=question),
        AIMessage(content=answer)
    ]

    return {
        "question": question,
        "context": context,
        "answer": answer,
        "history": new_history
    }

# =========================
# 创建Agent
# =========================

def create_legal_agent(llm, vectorstore):

    graph = StateGraph(AgentState)

    graph.add_node(
        "chat",
        lambda state: chat_node(
            state,
            llm,
            vectorstore
        )
    )

    graph.set_entry_point("chat")

    graph.add_edge(
        "chat",
        END
    )

    agent = graph.compile(
        checkpointer=memory
    )

    return agent