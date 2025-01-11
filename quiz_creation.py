from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
from pydantic import BaseModel

import streamlit as st
import os
from dotenv import load_dotenv

import urllib.error
from urllib.request import urlopen, Request
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


# Set the PWD environment variable to the current working directory
os.environ['PWD'] = os.getcwd()

# Load environment variables from .env file
load_dotenv()


# Initialize Google Generative AI
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])


system_template = """You are skilled at quiz creation. Check the text given by user as input and find out target customer persona from that text. 
Create a 10 question quiz with 4 options below each question by taking into consideration the problems faced by that target persona.

"""

## Prompt Template

prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), ("user", "{text}")]
)


## streamlit framework

st.title('Create your quiz')
input_text=st.text_input("Enter a valid link")

# url= urlopen(input_text)
# data=url.read()

# soup=BeautifulSoup(data,'html.parser')
# soup.find('title')

# text = soup.get_text()
# tokens = word_tokenize(text)

# swords = stopwords.words('english')
# quiz_creation_text = [token.lower() for token in tokens if token.lower() not in swords and (token.lower()).isalnum()]

# Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro")

# # Use the model to get the genre and key components
# parser = StrOutputParser()
# chain = prompt_template | llm | parser
# output = chain.invoke({"text": quiz_creation_text})

# # Display the result
# print(output)

if input_text:
    try:
        # Validate URL
        parsed_url = urlparse(input_text)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise ValueError("Invalid URL")

        # Add User-Agent header
        url = urlopen(input_text)
        headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'sec-ch-ua':'"Brave";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': url}

        request = Request(input_text, headers=headers)

        data = url.read()
        soup = BeautifulSoup(data, 'html.parser')
        soup.find('title')

        text = soup.get_text()
        tokens = word_tokenize(text)
        swords = stopwords.words('english')
        quiz_creation_text = [token.lower() for token in tokens if token.lower() not in swords and (token.lower()).isalnum()]

        # Use the model to get the genre and key components
        parser = StrOutputParser()
        chain = prompt_template | llm | parser
        output = chain.invoke({"text": quiz_creation_text})

        # Display the result
        st.write(output)
    except urllib.error.HTTPError as e:
        st.error(f"HTTP Error {e.code}: {e.reason}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
else:
    st.error("Please enter a valid URL")