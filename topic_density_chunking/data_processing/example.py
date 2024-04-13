import topic_utils.logging as log
from sklearn.datasets import fetch_20newsgroups
import random

logger = log.get_logger(__name__)


def create_example_input_docs(records=None, seed=None) -> list:
    """Creates a list of strings to demo the capabilities of the package.

    Args:
        records: The number of records to randomly select.

    Returns:
        dataset: A pandas dataframe.
    """
    logger.info("Creating example data")
    news = fetch_20newsgroups(subset="all", remove=("headers", "footers", "quotes"))[
        "data"
    ]

    if records is not None:
        if seed is not None:
            random.seed(seed)

        news = random.sample(news, records)

    logger.info(f"Created {len(news)} example records")

    return news
