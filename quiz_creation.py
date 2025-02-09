# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from langchain_google_genai import ChatGoogleGenerativeAI
# import google.generativeai as genai
# from pydantic import BaseModel

# import streamlit as st
# import os
# from dotenv import load_dotenv

# import urllib.error
# from urllib.request import urlopen, Request
# from urllib.parse import urlparse
# from bs4 import BeautifulSoup
# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords


# # os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


# # Set the PWD environment variable to the current working directory
# os.environ['PWD'] = os.getcwd()

# # Load environment variables from .env file
# load_dotenv()


# # Initialize Google Generative AI
# genai.configure(api_key=os.environ["GOOGLE_API_KEY"])


# system_template = """You are skilled at quiz creation. Check the text given by user as input and find out target customer persona from that text. 
# Create a 10 question quiz with 4 options below each question by taking into consideration the problems faced by that target persona.

# """

# ## Prompt Template

# prompt_template = ChatPromptTemplate.from_messages(
#     [("system", system_template), ("user", "{text}")]
# )


# ## streamlit framework

# st.title('Create your quiz')
# input_text=st.text_input("Enter a valid link")

# # url= urlopen(input_text)
# # data=url.read()

# # soup=BeautifulSoup(data,'html.parser')
# # soup.find('title')

# # text = soup.get_text()
# # tokens = word_tokenize(text)

# # swords = stopwords.words('english')
# # quiz_creation_text = [token.lower() for token in tokens if token.lower() not in swords and (token.lower()).isalnum()]

# # Gemini LLM
# llm = ChatGoogleGenerativeAI(
#     model="gemini-1.5-pro")

# # # Use the model to get the genre and key components
# # parser = StrOutputParser()
# # chain = prompt_template | llm | parser
# # output = chain.invoke({"text": quiz_creation_text})

# # # Display the result
# # print(output)

# if input_text:
#     try:
#         # Validate URL
#         parsed_url = urlparse(input_text)
#         if not parsed_url.scheme or not parsed_url.netloc:
#             raise ValueError("Invalid URL")

#         # Add User-Agent header
#         url = urlopen(input_text)
#         headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
#     'sec-ch-ua':'"Brave";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#     'Accept-Language': 'en-US,en;q=0.5',
#     'Referer': url}

#         request = Request(input_text, headers=headers)

#         data = url.read()
#         soup = BeautifulSoup(data, 'html.parser')
#         soup.find('title')

#         text = soup.get_text()
#         tokens = word_tokenize(text)
#         swords = stopwords.words('english')
#         quiz_creation_text = [token.lower() for token in tokens if token.lower() not in swords and (token.lower()).isalnum()]

#         # Use the model to get the genre and key components
#         parser = StrOutputParser()
#         chain = prompt_template | llm | parser
#         output = chain.invoke({"text": quiz_creation_text})

#         # Display the result
#         st.write(output)
#     except urllib.error.HTTPError as e:
#         st.error(f"HTTP Error {e.code}: {e.reason}")
#     except Exception as e:
#         st.error(f"An error occurred: {str(e)}")
# else:
#     st.error("Please enter a valid URL")

#################################################################################################


import asyncio
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
from crawl4ai import AsyncWebCrawler

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Check for API key
if not GOOGLE_API_KEY:
    raise ValueError("Missing Google API Key. Please check your .env file.")

# Configure Google Gemini API
genai.configure(api_key=GOOGLE_API_KEY)
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")

# Define the system prompt
system_prompt = """Please refer the attached file. It is summary of a website. 
Using the attached file, I want you to identify this website's target customer. 

If the target customer is a business (which means this website is operating as a B2B model), 
then create a quiz or assessment for the same. 

On the other hand, if the target customer is a consumer (which means this website is operating as a B2C model), 
then create a quiz or assessment for the potential partners of this website. 

The quiz or assessment should be designed in such a way that the target audience will get some insight 
about the problem being solved by this website and corresponding product or services that they are selling. 

The ideal purpose of the quiz or assessment will be to open the eyes of the target audience 
with some insights related to the problems they are facing and motivate them to enquire more about 
the product or services or solutions that the subject website or its owner is offering. 

The quiz or assessment should be simple and should not go beyond 10 to 15 questions, 
but feel free to make it more if it is really required. 

In the end, calculate their final score and create a personalized message for a specific range of scores. 
e.g., Low scorers will get a different message and medium scorers will get a different message.
"""

async def crawl_website(url):
    """ Uses crawl4ai to extract website content """
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url)
        return result.markdown  # Extracted content in Markdown format

def generate_quiz(website_content):
    """ Sends extracted website content to Gemini and returns the generated quiz """
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "{text}")
    ])
    
    parser = StrOutputParser()
    chain = prompt_template | llm | parser
    return chain.invoke({"text": website_content})

def main():
    """ Main function to crawl website and generate quiz """
    website_url = input("Enter website URL: ").strip()
    
    if not website_url:
        print("Error: Please enter a valid URL.")
        return

    try:
        # Run async web crawling
        print("\n🔍 Crawling website... Please wait.")
        website_content = asyncio.run(crawl_website(website_url))

        if not website_content.strip():
            print("❌ Error: Failed to retrieve content. Try another website.")
            return
        
        # Generate quiz based on website content
        print("\n🤖 Generating quiz based on extracted content...\n")
        quiz_output = generate_quiz(website_content)

        # Print the generated quiz
        print("🎯 Generated Quiz:\n")
        print(quiz_output)

    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
