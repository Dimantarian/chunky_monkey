from openai import AzureOpenAI
import os
from dotenv import load_dotenv, find_dotenv
from topic_utils.logging import get_logger

logger = get_logger(__name__)


def create_client():
    """ """

    load_dotenv(find_dotenv())

    use_azure_active_directory = (
        False  # Set this flag to True if you are using Azure Active Directory
    )

    if not use_azure_active_directory:
        endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
        api_key = os.environ["AZURE_OPENAI_API_KEY"]
    try:
        client = AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=api_key,
            api_version=os.getenv("OPENAI_API_VERSION"),
        )

        return client

    except Exception as e:
        print(e)


def general_prompt(client, prompt, model, temperature=0.9):
    try:
        result = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": f"{prompt}",
                },
            ],
            temperature=temperature,
        )
        if result.choices[0].finish_reason == "content_filter":
            logger.warning(f"Content filter triggered. Review the prompt: {prompt}.")
            output = None

        elif (
            result.choices[0].message is None
            or result.choices[0].message.content is None
        ):
            logger.warning(f"No content was returned. Review the prompt: {prompt}.")
            output = None
        else:
            output = result.choices[0].message.content

        return output
    except Exception as e:
        print(e)
