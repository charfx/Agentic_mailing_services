##ici on rassemble tous les elements deja definie
##LLM 
##prompt definie via Chatpromptemplate
##schema via pydantic assure output format du llm
from AI.llm import get_llm
from AI.schema import EmailAnalysis
from AI.prompts import email_analysis_prompt


def analyze_email(email):

    llm = get_llm()

    structured_llm = llm.with_structured_output(
        EmailAnalysis
    )

    chain = (
        email_analysis_prompt
        | structured_llm
    )

    result = chain.invoke(
        {
            "sender": email["from"],
            "email_date": email["date"],
            "subject": email["subject"],
            "body": email["body"]
        }
    )

    return result