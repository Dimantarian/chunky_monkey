import pandas as pd
import random


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
