from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class GraderUtils:
    def __init__(self, model):
        self.model = model

    def create_retrieval_grader(self):
        """
        Creates a retrieval grader that assesses the relevance of a retrieved document to a user question.

        Returns:
            A callable function that takes a document and a question as input and returns a JSON object with a binary score indicating whether the document is relevant to the question.
        """
        # 您是一名评分员，负责评估检索到的文档与用户问题的相关性。如果文档包含与用户问题相关的关键词，请将其评为相关。这不需要非常严格的测试。目标是过滤掉错误的检索结果。
        grade_prompt = PromptTemplate(
            template="""
            <|begin_of_text|><|start_header_id|>system<|end_header_id|>
            You are a grader assessing relevance of a retrieved document to a user question. If the document contains keywords related to the user question, grade it as relevant. It does not need to be a stringent test. The goal is to filter out erroneous retrievals.
            Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question.
            Provide the binary score as a JSON with a single key 'score' and no preamble or explanation.
            <|eot_id|>
            <|start_header_id|>user<|end_header_id|>

            Here is the retrieved document: \n\n {document} \n\n
            Here is the user question: {input} \n
            <|eot_id|>
            <|start_header_id|>assistant<|end_header_id|>
            """,
            input_variables=["document", "input"],
        )
        retriever_grader = grade_prompt | self.model | JsonOutputParser()

        return retriever_grader

    # 您是一名评分员，负责评估答案是否基于/得到一组事实的支持。请给出“是”或“否”的二元评分，以表明答案是否基于/得到事实的支持。提供一个只有一个键“score”的JSON，不需要前言或解释。
    def create_hallucination_grader(self):
        """
        Creates a hallucination grader that assesses whether an answer is grounded in/supported by a set of facts.

        Returns:
            A callable function that takes a generation (answer) and a list of documents (facts) as input and returns a JSON object with a binary score indicating whether the answer is grounded in/supported by the facts.
        """
        hallucination_prompt = PromptTemplate(
            template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
            You are a grader assessing whether an answer is grounded in / supported by a set of facts. Give a binary score 'yes' or 'no' score to indicate whether the answer is grounded in / supported by a set of facts. Provide the binary score as a JSON with a single key 'score' and no preamble or explanation.
            <|eot_id|>
            <|start_header_id|>user<|end_header_id|>
            Here are the facts:
            \n ------- \n
            {documents}
            \n ------- \n
            Here is the answer: {generation}
            <|eot_id|>
            <|start_header_id|>assistant<|end_header_id|>""",
            input_variables=["generation", "documents"],
        )

        hallucination_grader = hallucination_prompt | self.model | JsonOutputParser()

        return hallucination_grader

    def create_code_evaluator(self):
        """
        Creates a code evaluator that assesses whether the generated code is correct and relevant to the given question.

        Returns:
            A callable function that takes a generation (code), a question, and a list of documents as input and returns a JSON object with a binary score and feedback.
        """
        eval_template = PromptTemplate(
            template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> You are a code evaluator assessing whether the generated code is correct and relevant to the given question.
            Provide a JSON response with the following keys:

            'score': A binary score 'yes' or 'no' indicating whether the code is correct and relevant.
            'feedback': A brief explanation of your evaluation, including any issues or improvements needed.

            <|eot_id|><|start_header_id|>user<|end_header_id|>
            Here is the generated code:
            \n ------- \n
            {generation}
            \n ------- \n
            Here is the question: {input}
            \n ------- \n
            Here are the relevant documents: {documents}
            <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
            input_variables=["generation", "input", "documents"],
        )

        code_evaluator = eval_template | self.model | JsonOutputParser()

        return code_evaluator

    # 您是一个问题重写器，将输入的问题转换成更好的版本，优化以适应向量存储检索。请查看输入并尝试理解其潜在的语义意图/含义。
    def create_question_rewriter(self):
        """
        Creates a question rewriter chain that rewrites a given question to improve its clarity and relevance.

        Returns:
            A callable function that takes a question as input and returns the rewritten question as a string.
        """
        re_write_prompt = PromptTemplate(
            template="""
            You a question re-writer that converts an input question to a better version that is optimized for vectorstore retrieval. Look at the input and try to reason about the underlying sematic intent / meaning.

            Here is the initial question: {input}

            Formulate an improved question.""",

            input_variables=["input"],
        )

        question_rewriter = re_write_prompt | self.model | StrOutputParser()

        return question_rewriter

