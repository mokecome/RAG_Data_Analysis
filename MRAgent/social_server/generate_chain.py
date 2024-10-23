import os
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def create_generate_chain(llm):
    """
    Creates a generate chain for answering bilibili-related questions.

    Args:
        llm (LLM): The language model to use for generating responses.

    Returns:
        A callable function that takes a context and a question as input and returns a string response.
    """
    generate_template = """
    You are an AI personal assistant named FuFan. Users will pose questions related to BiliBili website data, which are presented in the parts enclosed by <context></context> tags.
    
    Use this information to formulate your answers.
    
    When a user's question requires fetching data using the BiliBili API, you may proceed accordingly.
    If you cannot find an answer, please respond honestly that you do not know. Do not attempt to fabricate an answer.  
    If the question is unrelated to the context, politely respond that you can only answer questions related to the context provided.
    
    For questions involving data analysis, please write the code in Python and provide a detailed analysis of the results to offer as comprehensive an answer as possible.
    
    <context>
    {context}
    </context>
    
    <question>
    {input}
    </question>
    """
    # 找不到答案時，請回應真實地表示你不知道
    # 如果問題與上下文無關，請友善地回應你只能回答與上下文相關的問題
    # 涉及數據分析的問題，請寫出Python代碼並提供詳細的分析結果，以提供最完整的回答
    generate_prompt = PromptTemplate(template=generate_template, input_variables=["context", "input"])


    generate_chain = generate_prompt | llm | StrOutputParser()

    return generate_chain



