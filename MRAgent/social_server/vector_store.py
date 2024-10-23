
from typing import List, Optional
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from social_server.document_loader import DocumentLoader


def get_local_store(store_path: str) -> FAISS:
    """
    Loads a locally stored FAISS vector store.

    Args:
        store_path (str): The path where the FAISS vector store is stored locally.

    Returns:
        FAISS: The loaded FAISS vector store.
    """
    # 加载Embedding模型
    embedding_model =  GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    # 从本地直接加载Faiss数据库
    store = FAISS.load_local(store_path, embedding_model)

    return store


async def create_vector_store(docs, store_path: Optional[str] = None) -> FAISS:
    """
    Creates a FAISS vector store from a list of documents.

    Args:
        docs (List[Document]): A list of Document objects containing the content to be stored.
        store_path (Optional[str]): The path to store the vector store locally. If None, the vector store will not be stored.

    Returns:
        FAISS: The FAISS vector store containing the documents.
    """
    # 构建文本切分器
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=50,
    )

    print("docs: ", docs)
    texts = text_splitter.split_documents(docs)

    # Embedding object
    embedding_model =  GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    # Create the FAISS vector store
    store = FAISS.from_documents(texts, embedding_model)

    # Save the vector store locally if a path is provided
    if store_path:
        store.save_local(store_path)

    return store


async def get_retriever(keywords: List[str], page: int):
    loader = DocumentLoader()
    docs = await loader.get_docs(keywords=keywords, page=page)
    vector_store = await create_vector_store(docs)
    if hasattr(vector_store, 'as_retriever'):
        # retriever = vector_store.as_retriever()
        # print(retriever.invoke("总结一下ChatGLM3-6b热门视频的描述"))
        return vector_store.as_retriever()
    else:
        return vector_store


if __name__ == '__main__':
    import asyncio

    asyncio.run(get_retriever(["ChatGLM3-6b"], 1))
