from stuff_model import model
from prompts import prompts
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from langchain.pydantic_v1 import BaseModel, Field


def summary_validation(
    doc, summary_prompt=prompts.summary_prompt, model_base_name="gpt-4o-mini"
):
    llm = ChatOpenAI(temperature=0, model_name=model_base_name)

    base_response_output_key = "base_response"
    base_response_chain = model.stuff_model(
        doc=doc, prompt=summary_prompt, model_name=model_base_name
    )

    query = (
        summary_prompt
        + f"""

        Now summarize the next article: 
        
        {doc}
    """
    )

    class PlanVerificationsOutput(BaseModel):
        query: str = Field(description="The user's query")
        base_response: str = Field(description="The response to the user's query")
        facts_and_verification_questions: dict[str, str] = Field(
            description="Facts (as the dictionary keys) extracted from the response and verification questions related to the query (as the dictionary values)"
        )

    plan_verifications_output_parser = PydanticOutputParser(
        pydantic_object=PlanVerificationsOutput
    )

    plan_verifications_template = """
    Given the below Question and answer, generate a series of verification questions that test the factual claims in the original baseline response.
    For example if part of a longform model response contains the statement “The Mexican–American War
    was an armed conflict between the United States and Mexico from 1846 to 1848”, then one possible
    verification question to check those dates could be “When did the Mexican American war start and
    end?”

    # Question: {query}
    # Answer: {base_response}

    # <fact in passage>, <verification question, generated by combining the query and the fact>

    # {format_instructions}
    # """

    plan_verifications_prompt_template = PromptTemplate(
        input_variables=[query] + [base_response_output_key],
        template=plan_verifications_template,
        partial_variables={
            "format_instructions": plan_verifications_output_parser.get_format_instructions()
        },
    )

    plan_verifications_chain = LLMChain(
        llm=llm,
        prompt=plan_verifications_prompt_template,
        output_key="output",
        output_parser=plan_verifications_output_parser,
    )

    plan = plan_verifications_chain.invoke(
        {"query": query, "base_response": base_response_chain[0]}
    )

    intermediate_result = plan["output"]

    claimed_facts = list(intermediate_result.facts_and_verification_questions.keys())
    verification_questions = list(
        intermediate_result.facts_and_verification_questions.values()
    )

    verify_input_variables = ["article", "question", "answer"]
    verify_output_key = "answer"

    verify_template = """

    Next I will give you a news article Article: 

    Article: {article}

    Now using only the information in the article, I will provide you with a question and its answer, and you must return True if the answer is correct or False if the answer is false or the article does not contain enough information to answer the question.


    Question: {question}


    Answer: {answer}

    """

    verify_prompt_template = PromptTemplate(
        input_variables=verify_input_variables, template=verify_template
    )

    verify_chain = LLMChain(
        llm=llm,
        prompt=verify_prompt_template,
        output_key=verify_output_key,
    )

    answer = []
    for i in range(len(verification_questions)):
        answer.append(
            verify_chain.invoke(
                {
                    "article": doc,
                    "question": verification_questions[i],
                    "answer": claimed_facts[i],
                }
            )["answer"]
        )

    return answer, verification_questions, claimed_facts


if __name__ == "__main__":
    summary_validation(
        doc="""MEXICO CITY (AP) — The smell of hairspray clouds Alexa Flores López as she gets the finishing touches of an intricate updo on her thick black hair. When Alexa found out she was going to have a quinceañera — the traditional celebration for a 15th birthday in Mexico — she could barely contain herself.\n\She got super excited, like her heart would come out!\" said her mother, Carmen López Díaz. \"She was just counting down the days.\"\nAt the Federico Gomez Children\\'s Hospital in Mexico City, volunteers clad in white and blue nurse uniforms scurry to attend to birthday girls and boys. They curl hair, do makeup, and adjust bow ties.\nIt\'s all for the hospital\'s annual \"Mis XV\" or \"My Fifteenth\" event. Whether the young patients are in treatment for a serious disease or have overcome cancer, the hospital celebrates the coming-of-age of these teenagers. After going through expensive treatments, some families can\'t afford to pay for a party — with the hospital providing them an alternative.\n\"We\'ve really just bought shoes because the hospital handles everything,\" said Díaz. \nThe hospital started throwing the event in 2017 after volunteer nurses caught wind that a beloved patient would turn 15 soon. They took it as an opportunity to organize a celebration for her and eventually turned it into an annual hospital event that\'s been going strong for seven years.\nIn Mexico, the \"quinceñera\" or \"fifteenth birthday\" is a huge rite of passage for adolescents, particularly girls. The occasion marks the transition of a teen into adulthood.\nThough Alexa\'s birthday was last month, the hospital allows patients to participate if their birthdays happen within the year of the celebration. \nShe has been a patient at the hospital the past three years receiving treatment for lupus. Her younger sister was just diagnosed with the same disease last year, making things more difficult for the family. However, the hospital\'s celebration has been something to look forward to. \n\"We never imagined so much — we thought this was going to be a regular hospital event,\" her mother said. \nFrancesca Solórzano, who has been a volunteer at the hospital for 17 years, assists Alexa on her big day and attends to her every need. Solórzano makes sure the teen has enough water and showers hairspray onto her dress to make sure its fabric remains crisp. \nShe also sports a silver and blue pin that matches Alexa\'s bouquet.\n\"I receive more than I give,\" Solórzano says about volunteering. \"I give my time here and I get a lot of blessings in return.\"\nSolórzano takes Alexa into a dressing area to change into her dress. When she comes out in a deep navy blue gown sprinkled with sequins, volunteers exclaim, \"How pretty!\" Another volunteer takes her cellphone out and snaps a picture. \"She looks like a princess!\" \nOn the other end of the room, Carlos Emilio Escalona García, 15, takes a seat with his mom after getting suited up. \nFor his mother, Marta Magdalena García Chávez, the day is filled with nothing but joy.\n\"It\'s really beautiful to see all of this happening,\" she said. \"He just had surgery so we wouldn\'t have had the possibility to have a party.\"\nCarlos has been a patient with the hospital for 13 years. He has dealt with heart problems since he was a child, and just underwent his fourth surgery. His mother said he gets tired often, but is still motivated to make the most out of every day.\n\"Like every other teenager, my favorite class is physical education,\" Carlos says. \"I also really enjoy doing math — I have so much fun doing different operations.\"\nThe preparations for the hospital\'s extravaganza have been a long time in the making. As early as January the hospital is already reaching out to make-up artists and other vendors to see if they want to participate. The entire event comes together free of charge.\nAfter getting fitted into their regal looks, it\'s time for the party to start.\nDownstairs in the banquet hall, family members crowd the dance floor, craning their necks to get a look at the teenagers. As they walk in with their partners, Carlos and Alexa end up lined up side by side.\n\"A round of applause for our fifteen-year-olds!\" says someone in the crowd.\nAs they kick off the first dance, Alexa takes the hand of her partner and her mom zooms in on her phone to get a video. After the chorus of the song settles, her mother takes a deep breath and puts her phone away — ready to capture the moment.\nShe stares in awe at her daughter as she twirls in her blue tulle skirt.\n""",
        summary_prompt=prompts.summary_prompt,
        model_base_name="gpt-4o-mini",
    )
