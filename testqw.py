import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

# 你的 .env 里如果写的是 DASHSCOPE_API_KEY，这里就取这个值
api_key = os.getenv("DASHSCOPE_API_KEY")

llm = ChatOpenAI(
    model="qwen-plus",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=api_key
)

response = llm.invoke("你好，请介绍一下你自己")
print(response.content)