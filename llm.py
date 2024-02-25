
import os
from operator import itemgetter
import json
import data

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

    def analyze_data(self, header, rows):
        prompt_template = """
        You are a system which analyzes csv data. You will analyze a csv file with the following fields:
        ```{header}```.

        Here is some sample rows of data:
        ```{rows}```.

        Generate any insights that you can about the data. Include any patterns or anomalies that you find. 
        This data will later be used by a system which generates additional data, so include any insights that may help generate additional similar data.
        """
        filled_template = prompt_template.format_map({"header": header, "rows": "\n".join(rows)})
        print(filled_template)
        output = self.model.invoke(filled_template)
        print(output)
        return output


    def generate_data(self, header, rows):
        analysis = self.analyze_data(header, rows)
        prompt_template = """
        You are a system which generates csv data. You will generate a csv file with the following fields:
        ```{header}```.

        Here is some sample rows of data:
        ```{rows}```.

        Here is an analysis of the data in order to help you generate additional data:
        ```{analysis}```.

        Generate 20 additional rows of csv data. Your response should only contain the csv data with no additional text. Do not include headers.
        """
        filled_template = prompt_template.format_map({"header": header, "rows": "\n".join(rows), "analysis": analysis})
        print(filled_template)
        output = self.model.invoke(filled_template).content


        data.write("intermediateoutput.csv", header, output)
        filtered_data = self.filter_data(header, output.split("\n")[1:], rows, analysis)

        return filtered_data
    
    def filter_data(self, header, rows, originalrows, analysis):

        prompt_template = """
        You are a system which analyzes data and removes outliers. You are looking at a csv file with the following fields:
        ```{header}```.

        Here is the data from that csv which you will be operating on:
        ```{rows}```.

        Here is an analysis of the data in order to help you generate additional data:
        ```{analysis}```.

        And here is the original data, which you should use to remove any rows that are outliers:
        ```{originalrows}```.

        Look at the rows of data and return any which are not outliers. Any data row which would not fit in the original data is considered an outlier.
        Your response should only contain the csv data with no additional text. Do not include headers.
        """
        filled_template = prompt_template.format_map({"header": header, "rows": "\n".join(rows), "analysis": analysis, "originalrows": "\n".join(originalrows)})
        print(filled_template)
        output = self.model.invoke(filled_template).content
        return output
    

class SafeDict(dict):
    def __missing__(self, key):
        return '{' + key + '}'