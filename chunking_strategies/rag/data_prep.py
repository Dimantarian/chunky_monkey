def generate_qa_prompt(article):
    prompt = f"""
    Your task is to create three (3) question and answer pairs from provided document. You must follow specific rules while generating 3 questions.

    Rules for Crafting Questions:
    1. The questions should be understandable and meaningful on its own, without needing the document chunks for context.
    2. Avoid including direct references or links to the text within your questions.
    3. Ensure the questions are complex and demonstrates a deep understanding of the document.
    4. Do not use phrases that refer back to this task or its instructions, such as "in the provided document".
    5. Make the questions as complex as you can, don't resort to simple questions.

    Rules for Crafting Answers:
    1. The answers should stand alone without referring back to the document or containing document-specific citations, like "Table 2.1".
    2. The answers must directly address the questions, fully encapsulated within the provided document.

    <Example 1>:
    User:
        Context: 
        Discusses the population growth in City A due to its expanding technology sector, noting an increase to 1.5 million residents as per the 2020 census.
        Contrasts with City B, where the population has remained stable at 1 million, attributed to its consistent but unexpanding manufacturing base.

    Assistant:
        {{"question": "How are City A's technological sector growth and City B's consistent manufacturing base differently influencing their urban planning strategies in light of their divergent population trends?", "answer": "City A's significant population increase, driven by the booming tech industry, necessitates urban planning strategies that focus on expanding residential and technological infrastructure to accommodate the growing workforce. In contrast, City B, with its stable population anchored by a longstanding manufacturing sector, might prioritize urban planning efforts towards sustaining and modestly enhancing existing industrial and residential areas to support its steady economic base."}}
    </Example 1>

    <Example 2>:
    User:
        Context:
        Details how the increasing adoption of remote work is leading to a significant decrease in demand for office spaces within city centers, with a noted 20% decline in office rentals over the past year.
        Highlights the shift in consumer behavior towards online shopping, resulting in a 30% increase in e-commerce sales and prompting the repurposing of traditional retail spaces into distribution hubs and experiential centers.

    Assistant:
        {{"question": "With a 20% decrease in office space rentals and a 30% increase in e-commerce sales over the past year, how are cities adapting urban development strategies to repurpose commercial and retail spaces?", "answer": "In response to the significant shifts in workplace and shopping behaviors, cities are reevaluating their urban development strategies to accommodate the new landscape. The marked decrease in office space demand has prompted a reimagining of city centers, with a focus on converting underutilized office buildings into residential units, co-working spaces, or community centers. Simultaneously, the surge in e-commerce has transformed traditional retail locations into distribution hubs or experiential centers, catering to the new consumer preferences. These adaptations reflect a broader move towards flexible, mixed-use urban environments that can respond dynamically to changing economic and social trends."}}
    </Example 2>

    <Example 3>:
    User:
        Context:
        Describes the innovative approaches to waste management in City X, focusing on recycling programs and the conversion of waste to energy.
        Highlights the advancements in public transportation in City Y, including the introduction of electric buses and expanded bike-sharing systems.
        Discusses the challenges faced by City Z's educational system, particularly the lack of resources and overcrowded classrooms.
        Details the implementation of smart city technologies in City W, such as IoT sensors for monitoring traffic and air quality.
        Explores the revival of local agriculture in City V, emphasizing community gardens and urban farms' role in enhancing food security.

    Assistant:
        {{"question": "Considering City X's waste-to-energy programs, City Y's adoption of electric buses, and City W's IoT-based traffic and air quality monitoring, how are these specific initiatives redefining standards for urban living quality?", "answer": "The integration of City X's waste-to-energy programs and City Y's electric buses represents a significant step towards reducing urban pollution and carbon footprint, thereby enhancing environmental sustainability. Coupled with City W's implementation of IoT technologies for real-time traffic and air quality management, these initiatives collectively contribute to a substantial improvement in urban living standards. They not only ensure a cleaner and more efficient urban environment but also demonstrate the potential of combining green technologies and smart city solutions to create more livable, sustainable cities for future generations."}}
    </Example 3>

    The following example shows how to modify the question in case it doesn't comply with the rules.
    <Example 4>:
    User:
        Context:
        Analyzes a recent study which found that in urban areas with populations over 500,000, the introduction of bike-sharing programs led to a 15% decrease in car usage during peak traffic hours.
        Reviews data from a national health survey indicating that cities with extensive bike-sharing programs saw a 10% increase in reported physical activity levels among residents.
        Discusses a policy initiative in several large cities aiming to expand green spaces and cycling infrastructure by 30% over the next five years, in response to the positive outcomes of bike-sharing programs.

    Assistant:
        {{"question": "Given the 15% decrease in car usage during peak hours in cities with bike-sharing and a 10% increase in physical activity levels, what specific urban planning strategies are being formulated to capitalize on these trends, particularly the 30% expansion in green spaces and cycling infrastructure?", "answer": "The observed 15% reduction in car usage and the corresponding 10% increase in physical activity in cities with bike-sharing programs underscore the programs' effectiveness in promoting sustainable transportation and healthier lifestyles. In response, urban planners are formulating strategies to further encourage these trends, including a significant 30% expansion in green spaces and cycling infrastructure over the next five years. These initiatives aim not only to enhance the urban environment and resident well-being but also to sustain the momentum towards more eco-friendly and active urban lifestyles."}}
    </Example 4>
    Article:\n
    {article}\n

       The output should be a list of dictionaries, with each question/answer pair structured as follows::
    {{
        [
            {{"question": <question>, "answer": <answer>}},
            {{"question": <question>, "answer": <answer>}},
            {{"question": <question>, "answer": <answer>}}
        ]
      }}

    Only provide the data in as describes, do not include any other information in the output.
    The questions should not be generic and should be specific to the content of the article.
    Ensure that the output is formatted as a list of dictionaries.
    Do not include markdown or any other formatting in the output e.g. no ```json.
    """
    return prompt
