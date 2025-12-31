from langchain.prompts import PromptTemplate

research_prompt = PromptTemplate(
    input_variables=["query"],
    template="""
You are an AI research assistant.

Research Query:
{query}

Tasks:
1. Explain the topic clearly
2. Provide key insights
3. Mention real-world use cases
4. Give a short conclusion

Return the response in bullet points.
"""
)
