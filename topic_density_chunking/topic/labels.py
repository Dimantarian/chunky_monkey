import os
from topic_utils.logging import get_logger
from topic_utils.openai_utils import create_client, general_prompt
from dotenv import load_dotenv, find_dotenv
from tqdm.notebook import tqdm

load_dotenv(find_dotenv())

logger = get_logger(__name__)
client = create_client()

labelling_model = os.getenv("LABELLING_MODEL")


def _extract_topic_values(topic_tuple: tuple) -> list:
    """
    Extracts the topic values from a tuple of topic values and probabilities

    Args:
        topic_tuple: A tuple of topic values and probabilities

    Returns:
        topic_values: A list of topic terms

    """
    # logger.info(f"Extracting topic values from {topic_tuple}")
    topic_values = [t[0] for t in topic_tuple]
    return topic_values


def extract_all_topics(topic_dict: dict) -> map:
    """
    Extracts all topics from a dictionary of topic values and probabilities

    Args:
        topic_dict: A dictionary of topic values and probabilities
        (from BERTopic)

    Returns:
        all_topics: A map of topic terms where each item maps to a topic list

    """
    topic_values = topic_dict.values()

    logger.info("Extracting all topics")
    all_topics = map(_extract_topic_values, topic_values)

    return all_topics


def _construct_prompt(topics: list) -> list:
    """
    Constructs a prompt from a dictionary of topic terms where each item maps
    to a topic list

    Args:
        topics: A dictionary of topic terms where each item maps to a topic
        list

    Returns:
        prompt: A list of prompts

    """

    logger.info(f"Constructing prompts from {len(topics)} topics")
    prompt_template = """The following words represent a topic: {}.
                    Please come up with a two-word label for the topic based on
                    the inputs, separated by an underscore."""

    prompts = []
    for topic_terms in topics:
        prompt = prompt_template.format(", ".join(topic_terms))
        prompts.append(prompt)

    logger.info(f"Constructed {len(prompts)} prompts")
    return prompts


def label_topics(
    topics: map, client=client, model=labelling_model, topic_embeddings=None
) -> dict:
    """
    Labels topics using the OpenAI API.

    Args:
        topics: A map of topic terms where each item maps to a topic
        list.
        client: An AzureOpenAI client.
        model: The OpenAI model to use.

    Returns:
        topic_labels: A dictionary with topic labels as keys and their
        corresponding topic lists as values.

    """

    topics_list = list(topics)
    prompts = _construct_prompt(topics_list)

    topic_labels = []
    for index, prompt in enumerate(tqdm(prompts, desc="Labelling topics...")):
        topic_label = general_prompt(client, prompt, model)

        if topic_label == "" or topic_label is None:
            topic_label = topics_list[index][0] + "_" + topics_list[index][1]

        if len(topic_label.split()) > 1:
            topic_label = topic_label.replace(" ", "_")

        topic_labels.append(topic_label)

    if topic_embeddings:
        topic_dict = dict(
            zip(
                topic_labels,
                [
                    {"topic_terms": t, "topic_vector": v}
                    for t, v in zip(topics_list, topic_embeddings)
                ],
            )
        )
    else:
        topic_dict = dict(zip(topic_labels, topics_list))

    logger.info("Topic labelling complete")

    return topic_dict
