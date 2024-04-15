import pandas as pd
import random
import re
from helper.openai_utils import general_prompt


def load_and_sample_data(input_datapath, sample_size, seed):
    """
    Load a CSV file and randomly sample a subset of rows.

    This function reads a CSV file, randomly selects a subset of rows,
    and returns a DataFrame containing the selected rows. The random
    seed can be set for reproducibility.

    Parameters
    ----------
    input_datapath : str
        The path to the input CSV file.
    sample_size : int
        The number of rows to randomly select from the CSV file.
    seed : int
        The random seed for reproducibility.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the randomly selected rows.

    Examples
    --------
    >>> df = load_and_sample_data("data/Reviews.csv", 1000, 42)
    """
    # Set the random seed for reproducibility
    random.seed(seed)

    # Get the number of lines in the file
    num_lines = sum(1 for l in open(input_datapath))

    # Calculate the number of lines to skip
    skip = num_lines - sample_size

    # The row indices to skip - make sure 0 is not included to keep the header!
    skip_idx = random.sample(range(1, num_lines), skip)

    # Load the data
    df = pd.read_csv(input_datapath, skiprows=skip_idx, index_col=0)
    df = df[["Time", "ProductId", "UserId", "Score", "Summary", "Text"]]
    df = df.dropna()
    df["combined"] = (
        "Title: " + df.Summary.str.strip() + "; Content: " + df.Text.str.strip()
    )

    return df


def remove_over_percentile(df, column, percentile):
    """
    Remove records from a DataFrame where a given column's value is over a given percentile.
    Also returns a DataFrame containing the outlier records.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to remove records from.
    column : str
        The column to consider when removing records.
    percentile : float
        The percentile to use as the cutoff. Records with a value in the specified column
        over this percentile will be removed.

    Returns
    -------
    pandas.DataFrame
        The DataFrame with the specified records removed.
    pandas.DataFrame
        The DataFrame containing the outlier records.
    """

    # Check if df is a DataFrame
    if not isinstance(df, pd.DataFrame):
        raise ValueError("df must be a pandas DataFrame")

    # Check if column exists in df
    if column not in df.columns:
        raise ValueError(f"{column} does not exist in the DataFrame")

    # Check if percentile is between 0 and 1
    if not 0 <= percentile <= 1:
        raise ValueError("percentile must be between 0 and 1")

    # Calculate the cutoff value
    cutoff = df[column].quantile(percentile)

    # Remove records where the column's value is over the cutoff
    df_clean = df[df[column] <= cutoff]

    # Create a DataFrame containing the outlier records
    df_outliers = df[df[column] > cutoff]

    return df_clean, df_outliers


def chunk_string_with_overlap(input_text: str, chunk_length: int, overlap: int):
    """
    Chunk a string into substrings of length n words with an overlap of k words.

    Parameters
    ----------
    input_text : str
        The string to chunk.
    chunk_length : int
        The length of each chunk in words.
    overlap : int
        The number of words each chunk should overlap with the next.

    Returns
    -------
    list of str
        The list of chunked substrings.
    """
    if chunk_length < 1:
        raise ValueError("chunk_length must be at least one")
    if overlap >= chunk_length:
        raise ValueError("k must be less than n")

    words = input_text.split()
    return [
        " ".join(words[i : i + chunk_length])
        for i in range(0, len(words) - overlap, chunk_length - overlap)
    ]


def convert_to_dict(results):
    converted_results = [eval(result) for result in results]
    return [item for sublist in converted_results for item in sublist]


def remove_latex_packages(text):
    # Regular expression pattern for LaTeX package inclusions
    pattern = r"\\usepackage\{.*?\}"

    # Remove LaTeX package inclusions
    cleaned_text = re.sub(pattern, "", text)

    return cleaned_text


def ask_rag(question, client, model, collection):
    results = collection.query(query_texts=[question], n_results=5)

    context = "\n".join(results["documents"][0])
    generation_prompt = f"""
    You provide answers to questions based on information available. You give precise answers to the question asked.
    You do not answer more than what is needed. You are always exact to the point. You Answer the question using the provided context.
    If the answer is not contained within the given context, say 'I dont know.'. 
    The below context is an excerpt from a report or data.
    Answer the user question using only the data provided in the sources below.

    CONTEXT:
    {context}
    

    QUESTION:
    {question}

    ANSWER:
    """

    return general_prompt(client, generation_prompt, model=model)
