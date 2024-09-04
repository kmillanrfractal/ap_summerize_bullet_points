from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import re
from langchain_community.callbacks import get_openai_callback
import time


def simple(article, model_name="gpt-4-turbo-2024-04-09"):
    print("start")
    chat_model = ChatOpenAI(model=model_name)

    # Definir prompts para cada tipo de titular
    prompt = PromptTemplate(
        input_variables=["article"],
        template="""You will be provided with an article.
        Your task is to identify and summarize the key points presented in the article.
        Focus on capturing the main ideas, arguments, and any critical information that contributes to the overall message of the article.
        The summary should be concise and highlight the most important aspects without unnecessary details.

        Output Format:

        Please present the summarized key points in the following format:

        1. first_point
        2. second_point
        (continue numbering as needed, based on the number of key points identified)

        Additional Instructions:

        Exclude minor details or examples unless they are crucial to understanding the main points.
        Ensure each key point is concise, ideally one sentence per point.
        The output should strictly follow the format provided above, with each point listed in a new line.
        If there are fewer than three key points, list only those that are relevant.
        If more than three key points are necessary, continue listing them beyond the third point.
        Ensure that the summary is neutral and objective, avoiding personal opinions or interpretations.

    
        Above the article : 

        {article}
""",
    )

    chain = prompt | chat_model

    with get_openai_callback() as cb:
        start_time = time.time()  # Start timing
        translate = chain.invoke(
            {
                "article": article,
            }
        ).content
        end_time = time.time()  # End timing
        execution_time = end_time - start_time  # Calculate total execution time

    return translate, execution_time, cb.total_cost
