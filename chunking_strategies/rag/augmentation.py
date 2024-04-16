def get_context(question, index, top_k=5):
    results = index.query(query_texts=[question], n_results=top_k)["documents"]
    return results


def contruct_prompt(context, question):
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
    return generation_prompt
