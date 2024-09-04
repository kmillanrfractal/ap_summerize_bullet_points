from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.llm import LLMChain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema import Document
from langchain.prompts import PromptTemplate


def stuff_model(doc, model_name="gpt-4o-mini"):
    doc = Document(page_content=doc)

    llm = ChatOpenAI(model=model_name)

    # Define prompt

    prompt = PromptTemplate(
        input_variables=["context"],
        template="""You are an expert news summarizer who can summarize print articles for a radio audience. 
        The style should be narrative and catchy for an audience on the go. 
        This means no sentence should require repetition to understand.

            ##Writing Style##:
            a) DO NOT use sensational language. Begin with a catchy hook that can convey the latest news on its own.
                Right:Kansas tightens its grip on abortion data collection.
                Wrong:A bold move amidst turmoil: U.S. President Joe Biden is set to announce a groundbreaking plan.
                
            b) The first sentence of the summary, if isolated, should stand on its own as a complete story that requires no further explanation.

            ##Limits##:
            a) The article can have NO less than 120 words and NO more than 150 words.
            b) NO sentence should have more than 20 words.

            c) DO NOT use long clauses in sentences:
                Right: Conspiracy theorist Alex Jones is seeking to restructure his personal bankruptcy filing to raise money for a $1.5 billion defamation judgment.
                Wrong: Alex Jones, known for his conspiracy theories, filed a motion on Wednesday to convert his personal bankruptcy case to a liquidation, aiming to sell off assets to help pay some of the $1.5 billion he owes to Sandy Hook Elementary School shooting victims' relatives.

            d)  DO NOT use sentence clauses to add people's titles or organization descriptors. BUT ALWAYS include the titles or descriptors people, organizations and locations are most known for. But use the minimum number of words in titles and/or descriptors
                Right:President Biden announced on Tuesday....
                Wrong:Joe Biden, the US President, announced on Tuesday
                Right:Columbia University senior history professor John Doe said that...
                Wrong:John Doe, Columbia University history professor, said that...

            e) NEVER miss adding, in the second sentence, the day of the week the story was reported. However, do not begin the summary with when it happened. Also, do not use relative terms like last week or yesterday to convey when the main event happened:
                Right: No change in the number of unemployment applications as of last week, 217,000. The trend reported last Thursday shows a healthy job market.
                Wrong:The Labor Department reports that U.S. jobless claims remained steady last week at 217,000, reflecting a strong labor market despite high interest rates.
                Wrong:The Labor Department reported on Thursday that applications for jobless benefits in the country held steady at 217,000 for the week ending March 2, matching the previous week's level.

            f) Do not add the specific date of occurrence of the main event. The day of the week is enough:
                Right: Conspiracy theorist Alex Jones wants to change his bankruptcy to liquidation. On Wednesday, he filed a motion in U.S. Bankruptcy Court.
                Wrong: Alex Jones wants to change his bankruptcy to liquidation. On Wednesday, June 14, he filed a motion in U.S. Bankruptcy Court.

            g) A sentence should have NO more than 2 clauses:
                Right: Conspiracy Alex Jones denied the allegations, stating that he could prove himself if necessary.
                Wrong: Alex Jones denied the allegations, stating that if necessary, he could prove his innocence, and that he does not need the President’s support.

            h) DO NOT cite or quote entities that do not contribute to the main story. Identify the most important who, what, when, where, why, and how and use those details to craft the summary:
                Wrong: Senior officials revealed U.S. President Joe Biden's plan to establish a temporary port on the Gaza coast.
                Right: President Joe Biden plans to reveal a strategy on Thursday.
                
            ##Quotes##:
            a) Do not use long or multi-sentence quotes. Pick the sentence that does not require additional clarification:
                Right: Dr. Agard confirmed that her team has received funding for cancer research.
                Wrong: "We have received funding for cancer research, and are very happy about it, as you can see," said Dr. Agard.
                
            b) NEVER place source attribution at the end of a quote or sentence. Start the sentence with an attribution or incorporate it mid-sentence:
                Right: Dr. Carla said she noticed a drop in cancer patients in 2012.
                Wrong: The number of cancer patients, as Dr. Carla noted, dropped in 2012.


            ##Tense##:
            a) Use a present-tense lede whenever possible – it should sound current or forward-looking. Describe any ongoing or current situation in the present tense.
            b) DO NOT use the present tense to describe a momentary situation that will soon be outdated.
            c) Use past tense when the event occurred at a specific moment in the past.
            d) Use present perfect tense when the event happened recently and is still relevant to the present moment
            
            Now summarize the next article: 
            
            {context}
        """,
    )

    # Instantiate chain
    chain = create_stuff_documents_chain(llm, prompt)

    # Invoke chain
    result = chain.invoke({"context": [doc]})
    print(result)


if __name__ == "__main__":
    stuff_model(
        doc="""MEXICO CITY (AP) — The smell of hairspray clouds Alexa Flores López as she gets the finishing touches of an intricate updo on her thick black hair. When Alexa found out she was going to have a quinceañera — the traditional celebration for a 15th birthday in Mexico — she could barely contain herself.\n\She got super excited, like her heart would come out!\" said her mother, Carmen López Díaz. \"She was just counting down the days.\"\nAt the Federico Gomez Children\\'s Hospital in Mexico City, volunteers clad in white and blue nurse uniforms scurry to attend to birthday girls and boys. They curl hair, do makeup, and adjust bow ties.\nIt\'s all for the hospital\'s annual \"Mis XV\" or \"My Fifteenth\" event. Whether the young patients are in treatment for a serious disease or have overcome cancer, the hospital celebrates the coming-of-age of these teenagers. After going through expensive treatments, some families can\'t afford to pay for a party — with the hospital providing them an alternative.\n\"We\'ve really just bought shoes because the hospital handles everything,\" said Díaz. \nThe hospital started throwing the event in 2017 after volunteer nurses caught wind that a beloved patient would turn 15 soon. They took it as an opportunity to organize a celebration for her and eventually turned it into an annual hospital event that\'s been going strong for seven years.\nIn Mexico, the \"quinceñera\" or \"fifteenth birthday\" is a huge rite of passage for adolescents, particularly girls. The occasion marks the transition of a teen into adulthood.\nThough Alexa\'s birthday was last month, the hospital allows patients to participate if their birthdays happen within the year of the celebration. \nShe has been a patient at the hospital the past three years receiving treatment for lupus. Her younger sister was just diagnosed with the same disease last year, making things more difficult for the family. However, the hospital\'s celebration has been something to look forward to. \n\"We never imagined so much — we thought this was going to be a regular hospital event,\" her mother said. \nFrancesca Solórzano, who has been a volunteer at the hospital for 17 years, assists Alexa on her big day and attends to her every need. Solórzano makes sure the teen has enough water and showers hairspray onto her dress to make sure its fabric remains crisp. \nShe also sports a silver and blue pin that matches Alexa\'s bouquet.\n\"I receive more than I give,\" Solórzano says about volunteering. \"I give my time here and I get a lot of blessings in return.\"\nSolórzano takes Alexa into a dressing area to change into her dress. When she comes out in a deep navy blue gown sprinkled with sequins, volunteers exclaim, \"How pretty!\" Another volunteer takes her cellphone out and snaps a picture. \"She looks like a princess!\" \nOn the other end of the room, Carlos Emilio Escalona García, 15, takes a seat with his mom after getting suited up. \nFor his mother, Marta Magdalena García Chávez, the day is filled with nothing but joy.\n\"It\'s really beautiful to see all of this happening,\" she said. \"He just had surgery so we wouldn\'t have had the possibility to have a party.\"\nCarlos has been a patient with the hospital for 13 years. He has dealt with heart problems since he was a child, and just underwent his fourth surgery. His mother said he gets tired often, but is still motivated to make the most out of every day.\n\"Like every other teenager, my favorite class is physical education,\" Carlos says. \"I also really enjoy doing math — I have so much fun doing different operations.\"\nThe preparations for the hospital\'s extravaganza have been a long time in the making. As early as January the hospital is already reaching out to make-up artists and other vendors to see if they want to participate. The entire event comes together free of charge.\nAfter getting fitted into their regal looks, it\'s time for the party to start.\nDownstairs in the banquet hall, family members crowd the dance floor, craning their necks to get a look at the teenagers. As they walk in with their partners, Carlos and Alexa end up lined up side by side.\n\"A round of applause for our fifteen-year-olds!\" says someone in the crowd.\nAs they kick off the first dance, Alexa takes the hand of her partner and her mom zooms in on her phone to get a video. After the chorus of the song settles, her mother takes a deep breath and puts her phone away — ready to capture the moment.\nShe stares in awe at her daughter as she twirls in her blue tulle skirt.\n"""
    )
