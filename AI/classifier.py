##ici on rassemble tous les elements deja definie
##LLM 
##prompt definie via Chatpromptemplate
##schema via pydantic assure output format du llm

from AI.llm import get_llm
from AI.schema import EmailIntent
from AI.prompts import email_classification_prompt


def classify_email(email):

    #model LLM brain 
    llm = get_llm()

    ##the format output fixed via pydantic
    structured_llm = llm.with_structured_output(
        EmailIntent
    )

    #LCEL via the pipe "|" that ensure the notion of chain coordination execution !
    chain = (
        email_classification_prompt
        | structured_llm
    )

    ##the calling invoke with single input and single output clarifying the variable needed .

    result = chain.invoke(
        {
            "sender": email["from"],
            "subject": email["subject"],
            "body": email["body"]
            
        }
    )

    return result