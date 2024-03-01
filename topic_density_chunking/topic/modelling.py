from bertopic import BERTopic
from bertopic.representation import KeyBERTInspired
from numpy import ndarray
import utils.logging as log

logger = log.get_logger(__name__)


# TODO: Separate out model creation and parametrise it with the core options
# for BERTopic components (embeddings, dimension reduction, clustering,
# Vectorisation, Word weighting, and fine tuning)


def create_and_fit_topic_model(docs: list) -> (BERTopic, list, ndarray | None):
    """Creates a topic model from a list of documents.

    Args:
        docs: A list of documents.

    Returns:
        topics: A list of topics.
    """
    logger.info("Creating topic model")
    rep_model = KeyBERTInspired()

    kb_topic_model = BERTopic(representation_model=rep_model, verbose=True)

    logger.info("Fitting topic model")
    topics, probs = kb_topic_model.fit_transform(docs)

    return (kb_topic_model, topics, probs)
