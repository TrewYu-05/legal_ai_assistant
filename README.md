# AI 法律助手 (AI Legal Assistant)

这是一个基于 [Streamlit](https://streamlit.io/)、[LangChain](https://www.langchain.com/) 和阿里云 DashScope（通义千问）的 AI 法律助手项目。该项目使用了检索增强生成（RAG）技术，通过内建的法律知识库（FAISS 向量数据库）为用户提供专业、严谨的法律咨询服务，同时具备提取用户长期记忆的功能。

## 🌟 功能特点
- **法律知识库 RAG**：在回答前优先从内建的法律数据库检索相关条文，减少 AI 幻觉，提供更可靠的法律依据。
- **自动记忆提取**：AI 自动从用户对话中提取有价值的长线信息（如用户身份、案件类型等），保存在本地 SQLite 数据库中。
- **上下文感知**：利用 LangChain 将聊天历史和记忆作为上下文，提供具有连贯性的连续对话。
- **交互式 UI**：基于 Streamlit 构建的轻量、直观的 Web 界面。

## 🚀 快速开始

### 1. 克隆项目
```bash
git clone <your-repository-url>
cd <your-repository-directory>
```

### 2. 安装依赖
确保你安装了 Python 3.8+ 环境，然后运行：
```bash
pip install -r requirements.txt
```

### 3. 配置环境变量
在项目根目录创建一个 `.env` 文件，或者复制 `.env.example` 为 `.env`：
```bash
cp .env.example .env
```
然后在 `.env` 中填入你的阿里云 DashScope API 密钥：
```ini
DASHSCOPE_API_KEY=your_actual_api_key_here
```

### 4. 运行应用
```bash
streamlit run app.py
```
运行后，浏览器会自动打开 `http://localhost:8501`。

## ☁️ 部署到 Streamlit Community Cloud

你可以将该项目免费部署到 [Streamlit Community Cloud](https://streamlit.io/cloud)：
1. 将本项目推送到你的 GitHub 仓库。
2. 登录 Streamlit Cloud，点击 **New app**。
3. 选择你的 GitHub 仓库、分支以及主干文件 `app.py`。
4. 点击 **Advanced settings**，在 **Secrets** 区域添加你的环境变量：
   ```toml
   DASHSCOPE_API_KEY = "your_actual_api_key_here"
   ```
5. 点击 **Deploy**，等待部署完成后即可通过在线地址访问。

## 📁 目录结构
- `app.py`：主 Streamlit 应用。
- `memory/`：处理用户长期和短期记忆的模块（SQLite）。
- `rag/`：处理 RAG（检索增强生成）、向量知识库建立和加载的模块。
- `requirements.txt`：项目运行所需的 Python 依赖。
- `.env.example`：环境变量示例文件。
