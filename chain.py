import os
from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


class Chain:
    def __init__(self):
        self.llm = ChatGroq(
                            temperature=0,
                            groq_api_key=os.getenv("groq_api_key"),
                            model_name='llama-3.1-70b-versatile'
                            )
    def extract_job(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### Scraped text from website:
            {page_data}
            ### Instruction:
            these scrapped text from careers page of a website.
            your job is to extract the job posting and return them in JSON format containing                    following keys:
            'role', 'experience, 'skills', and 'description'.
            only return valid json
            ### valid json and no preamble:
            """
        )
        
        
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={'page_data' : cleaned_text})
        
        try:
            json_parser = JsonOutputParser()
            json_res = json_parser.parse(res.content)
        except:OutputParserException("Contexttoo big. Unable to parse jobs")
        
        return res if isinstance(res, list) else [res]
        
        
    def write_mail(self, job, links):
        prompt_email = PromptTemplate.from_template(
            """
            ### Job DSCRIPION:
            {job description}
        
            ###INSTRUCTION:
            you are Thilanka, hr consultent in Big Dick Technologies. the company is working in software, machine learning
            , atomation fields. Over our experience, we have empowered numerous enterprises with tailored solution, fostering scalability,
            process optimization, cost reduction, and heightened overall efficiency.
            your job is to write a cold email to the client regarding the job mentioned above describing the capabilities of big dick in fullfilling their needs.
        
            also add most relevant ones from the following links to showcase big dick technologies porfolios:{link list}
        
            remember you are thilanka, hr consultant in big dick technologies.
            do not provide a peamble.
            ### EMAIL (NO PREAMBLE):
            """
        )

        chain_extract = prompt_email | self.llm
        res = chain_extract.invoke(input={'job description' : str(job), 'link list': links})
        return res.content
        