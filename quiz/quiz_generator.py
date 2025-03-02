"""
quiz_generator.py - Core module for generating quizzes from website content.
Uses Google Gemini AI (via LangChain) to produce quizzes.
"""

import time
from common.config import GOOGLE_API_KEY, SYSTEM_PROMPT
from common.logger import logger
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai

# Configure the Google Gemini API
genai.configure(api_key=GOOGLE_API_KEY)
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")

def generate_quiz(website_content: str) -> str:
    """
    Generate a quiz based on the provided website content.
    
    Parameters:
        website_content (str): The text content extracted from a website.
    
    Returns:
        str: The generated quiz text.
    
    Raises:
        Exception: If quiz generation fails or returns empty output.
    """
    logger.info("Starting quiz generation.")
    overall_start = time.time()
    try:
        start_time = time.time()
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("user", "{text}")
        ])
        parser = StrOutputParser()
        chain = prompt_template | llm | parser
        quiz_output = chain.invoke({"text": website_content})
        elapsed = time.time() - start_time
        logger.info("Quiz generation core process took %.2f seconds.", elapsed)

        total_elapsed = time.time() - overall_start
        logger.info("Total quiz generation time: %.2f seconds", total_elapsed)

        if not quiz_output:
            logger.error("Quiz generation returned empty output.")
            raise Exception("Quiz generation failed.")
        return quiz_output
    except Exception as e:
        logger.exception("Error during quiz generation: %s", e)
        raise
