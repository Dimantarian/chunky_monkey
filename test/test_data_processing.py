import pytest
from topic.processing import _calculate_topic_densities, combined_densities


@pytest.fixture
def setup_data():
    doc0 = "This is a sentence about sample text. This is a sample sentence about testing densities in text."
    doc1 = """
    Natural Language Processing (NLP), a subset of artificial intelligence, 
    focuses on the interaction between computers and human language. At its core, 
    NLP aims to enable computers to understand, interpret, and respond to human 
    language in a valuable way. To achieve this, vast amounts of sample text are 
    processed, enabling machines to learn language patterns and nuances. 
    This sample text, often derived from diverse sources, forms the bedrock of NLP 
    training models. Testing these models is a critical step in NLP development. 
    During testing, algorithms are exposed to new text samples to evaluate their 
    understanding and response accuracy. This iterative process of testing and 
    refining helps in enhancing the model's ability to process language effectively.

    Moreover, the concept of word densities in NLP holds significant importance. 
    It refers to the frequency of specific words or phrases in a given text sample. 
    By analyzing these densities, NLP algorithms can discern topic relevance, sentiment, 
    and even stylistic elements of the text. High-frequency words in a sample text often 
    indicate key themes or subjects, making the analysis of these densities crucial in tasks 
    like text summarization or keyword extraction. Repeated testing with various text 
    samples ensures that NLP models can accurately interpret varying densities and 
    adapt to different linguistic contexts. As NLP continues to evolve, the manipulation 
    and understanding of sample texts, coupled with rigorous testing and analysis of word 
    densities, remain pivotal in pushing the boundaries of how machines understand human 
    language.
    """

    doc2 = """
    Natural Language Processing (NLP) is a field of Artificial Intelligence (AI) that
    enables computers to analyze and understand human language. It combines computer
    science, information engineering, and AI to process human languages and convert
    them into actionable insights. NLP uses machine learning algorithms to analyze
    text and speech data. It also uses Natural Language Understanding (NLU) to
    understand the meaning behind the text. NLP is used in various applications
    such as machine translation, speech recognition, sentiment analysis, and
    text classification. NLP is also used in chatbots and virtual assistants
    to understand human language and respond accordingly. NLP is a rapidly
    growing field of AI. It is used in various industries such as healthcare,
    finance, and education. NLP is also used in various applications such as
    machine translation, speech recognition, sentiment analysis, and text
    classification. NLP is also used in chatbots and virtual assistants to
    understand human language and respond accordingly. NLP is a rapidly
    growing field of AI. It is used in various industries such as healthcare,
    finance, and education.
    """
    topics = {"topic1": ["sample", "text"], "topic2": ["testing", "densities"]}
    return doc0, doc1, doc2, topics


def test_calculate_topic_densities_type(setup_data):
    doc0, doc1, doc2, topics = setup_data
    result = _calculate_topic_densities(doc0, topics, 5, 10, 3, 2)
    assert isinstance(result, list)


def test_calculate_topic_densities_calculation(setup_data):
    doc0, doc1, doc2, topics = setup_data
    result = _calculate_topic_densities(doc0, topics, 5, 10, 3, 2)
    assert result[0]["substring_start"] == 0
    assert result[0]["substring_end"] == 7
    assert result[1]["substring_start"] == 4
    assert result[1]["substring_end"] == 9
    assert result[2]["substring_start"] == 6
    assert result[2]["substring_end"] == 13
    assert result[3]["substring_start"] == 10
    assert result[3]["substring_end"] == 17


def test_combined_densities_columns(setup_data):
    doc0, doc1, doc2, topics = setup_data
    docs = [doc0, doc1, doc2]
    result = combined_densities(docs, topics)
    assert result.columns.tolist() == [
        "doc_id",
        "chunk_id",
        "substring_start",
        "substring_end",
        "l2_norm",
        "topic1_topic_density",
        "topic2_topic_density",
    ]
