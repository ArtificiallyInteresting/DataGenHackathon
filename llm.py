
import os
from operator import itemgetter
import json

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import ConversationChain
from langchain_core.runnables import RunnableLambda, RunnablePassthrough


from langchain.memory import ConversationBufferMemory

class llm:
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY', 'YourAPIKey')
        self.model = ChatOpenAI(model="gpt-3.5-turbo")

    def generate_data(self):
        headers = "Name, Age"
        prompt_template = """
        You are a system which generates csv data. You will generate a csv file with the following fields:
        ```{headers}```.
        Here is some sample rows of data:
        ```Henry, 32
        John, 45
        Alice, 28
        ```
        Generate 20 additional rows of csv data. Your response should only contain the csv data with no additional text.
        """
        filled_template = prompt_template.format_map({"headers": headers})
        prompt = ChatPromptTemplate.from_template(filled_template)


        output = self.model.invoke(filled_template)
        print (output)
        return output

class SafeDict(dict):
    def __missing__(self, key):
        return '{' + key + '}'