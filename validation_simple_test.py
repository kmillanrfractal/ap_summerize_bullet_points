from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain


def simple_varification(
    doc, summarization_prompt, summary_generated, model_base_name="gpt-4o-mini"
):
    llm = ChatOpenAI(temperature=0, model_name=model_base_name)

    prompt = """You are an expert AI system designed to detect hallucinations in text summarizations produced by language models. 
    Your task is to carefully analyze the given input text and its corresponding summary, identifying any information in the summary that is not supported by or contradicts the original input.

    ## Input Format:
    You will receive three pieces of information:
    1. The original input text
    2. The summarization prompt used
    3. The summary generated by the language model

    ## Your Task:
    1. Thoroughly read and understand the original input text.
    2. Review the summarization prompt to understand the task given to the language model.
    3. Carefully examine the generated summary, comparing it to the original input.
    4. Identify any statements or information in the summary that:
    a. Are not present in or directly implied by the original text
    b. Contradict information in the original text
    c. Exaggerate or misrepresent information from the original text
    5. For each identified issue, provide:
    a. The problematic statement from the summary
    b. An explanation of why it's considered a hallucination
    c. The relevant section from the original text (if applicable)

    ## Output Format:
    Provide your analysis in the following structure:

    1. Hallucination Detection:
    - [List each identified hallucination with explanations]

    2. Accuracy Score:
    - Assign a score from 1-10, where 10 represents a perfectly accurate summary with no hallucinations, and 1 represents a summary filled with hallucinations.

    3. Confidence Level:
    - State your confidence in your assessment (Low/Medium/High) and briefly explain why.

    4. Improvement Suggestions:
    - Provide brief suggestions on how the summary could be improved to eliminate hallucinations.

    Remember:
    - Be thorough and precise in your analysis.
    - Consider both explicit statements and implicit information.
    - Be aware of potential paraphrasing or synonymous expressions that maintain the original meaning.
    - If no hallucinations are detected, state this clearly and explain your reasoning.

    Your goal is to ensure the highest level of accuracy and faithfulness to the original text in summarizations. 
    Your analysis will be crucial in improving the reliability of AI-generated summaries.

    Below I attach the variables for the analysis:

    1. The original input text: {input_text}
    2. The summarization prompt used {summarization_prompt}
    3. The summary generated by the language model {summary_generated}


    """

    verifications_prompt_template = PromptTemplate(
        input_variables=["input_text", "summarization_prompt", "summary_generated"],
        template=prompt,
    )

    verifications_chain = LLMChain(
        llm=llm,
        prompt=verifications_prompt_template,
    )

    return verifications_chain.invoke(
        {
            "input_text": doc,
            "summarization_prompt": summarization_prompt,
            "summary_generated": summary_generated,
        }
    )
