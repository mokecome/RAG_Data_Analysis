- **AI Agent 框架**: LangGraph
  
- **模型調用**: 基於LangChain gpt-4o or gemini-1.5-flash-latest 模型 
  
- **前端技术**: Streamlit
  
- **後端技术**: LangServe + FastAPI
  
- **嵌入模型**: OpenAI Embedding
  


## 安装指南
```bash
# 克隆仓库
git clone https://github.com/mokecome/RAG_Data_Analysis.git

# 安装依赖
cd community_data_analysis
pip install -r requirements.txt

# 在.env文件中填写OpenAI API Key

# 运行服务端
python app/client

# 运行客户端
streamlit run app/client.py
```
