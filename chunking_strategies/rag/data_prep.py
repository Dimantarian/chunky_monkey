import json
from multiprocessing import Pool
import pandas as pd
from helper.general import convert_to_dict
from helper.openai_utils import general_prompt, create_client


def generate_qa_prompt(article):
    prompt = f"""
    Given the following article, generate 5 Question/Answer pairs that could be used to test a student's understanding of the material:

    Article:\n
    {article}\n

    The output should be a list of dictionaries, with each question/answer pair structured as follows:
    {{
        "question": "What is the capital of France?",
        "answer": "Paris"
    }}

    Only provide the data in as describes, do not include any other information in the output.
    The questions should not be generic and should be specific to the content of the article.
    Ensure that the output is formatted as a list of dictionaries.
    Do not include markdown or any other formatting in the output e.g. no ```json.
    Do not generate questions that are too similar to each other.
    Do not generate questions that require external knowledge.
    """
    return prompt
