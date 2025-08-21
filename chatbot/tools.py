from pdf_wrapper import PDFSearchAPIWrapper
from web_wrapper import WebSearchAPIWrapper
from langchain_google_community import GoogleSearchAPIWrapper
from langchain.tools import StructuredTool

# Configure Google Search tool
def google_tool():
    google_search = GoogleSearchAPIWrapper()
    google_tool = StructuredTool.from_function(
        func=google_search.run,
        name="google-search",
        description="Search Google for recent results."
    )
    return google_tool

# Configure Web URL Search tool
def web_tool():
    web_search = WebSearchAPIWrapper()
    web_tool = StructuredTool.from_function(
        func=web_search.run,
        name="web-search",
        description="Searches in URL data to get the relavent chunk based on the  user-query."
    )
    return web_tool

# Configure PDF Search tool
def pdf_tool():
    pdf_search = PDFSearchAPIWrapper()
    pdf_tool = StructuredTool.from_function(
        func=pdf_search.run,
        name="pdf-search",
        description="Searches in pdf to get the relavent chunk based on the  user-query. "
    )
    return pdf_tool