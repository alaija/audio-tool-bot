from llama_index.llms.openai import OpenAI
from logger import logger
import os
import prompt_templates as prompts
from dotenv import load_dotenv

load_dotenv()

LLM_MODEL = "gpt-4o-mini"

llm = OpenAI(
    model=LLM_MODEL,
    api_key=os.getenv("OPENAI_API_KEY"), 
    temperature=0.1
)

def clean_up(text) -> str:
    logger.info(f"Cleaning up text")
    response = llm.complete(prompts.CLEAN_UP_TEMPLATE.format(text=text)) 
    return response.text.strip()

def structure(text) -> str:
    logger.info(f"Structuring text")
    response = llm.complete(prompts.STRUCTURE_TEMPLATE.format(text=text)) 
    return response.text.strip()

def email(lang, text) -> str:
    logger.info(f"Generating email in {lang}")
    response = llm.complete(prompts.EMAIL_TEMPLATE.format(target_language=lang, text=text)) 
    return response.text.strip()

def translate(lang, text) -> str:
    logger.info(f"Translating text to {lang}")
    response = llm.complete(prompts.TRANSLATION_TEMPLATE.format(target_language=lang, text=text)) 
    return response.text.strip()