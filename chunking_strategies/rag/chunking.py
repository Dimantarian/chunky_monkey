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
