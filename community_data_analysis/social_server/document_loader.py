from langchain_core.documents import Document
from jd import result_pipiline
from typing import List, Optional
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter


class DocumentLoader:
    """
    This class uses the get_docs function to take a Keyword as input, and outputs a list of documents (including metadata).
    """

    async def create_vector_store(self, docs, store_path: Optional[str] = None) -> 'FAISS':
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=300)
        texts = text_splitter.split_documents(docs)
        embedding_model = OpenAIEmbeddings()
        store = FAISS.from_documents(texts, embedding_model)

        if store_path:
            store.save_local(store_path)
        return store

    async def get_retriever(self, keywords: List[str], page: int):
        print(f"开始实时查询API获取数据")
        docs = [Document(page_content=doc["real_data"]) for doc in result_pipiline(keywords=keywords)]
        print(f"接收到的数据为：{docs}")
        print("-------------------------")
        print(f"开始进行向量数据库存储")
        vector_store = await self.create_vector_store(docs)
        print(f"成功完成向量数据库的存储")
        print("-------------------------")
        print(f"开始进行文本检索")
        retriever = vector_store.as_retriever(search_kwargs={"k": 10})
        retriever_result = retriever.invoke(str(keywords))
        print(f"检索到的数据为：{retriever_result}")
        return retriever_result
