from langchain_core.prompts import ChatPromptTemplate

# Build prompt template
def prompt():
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system", """You are a helpful assistant.
                You have been equipped with tools to:
                1. Chat with the user about uploaded PDFs.
                2. Perform Google searches to retrieve information.
                3. Open a web URL and scrape information from it.
                
                Use the right tool depending on the user query/request, and then respond helpfully in natural language."""
            ),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )
    return prompt