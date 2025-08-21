from pdf_wrapper import PDFSearchAPIWrapper
from web_wrapper import WebSearchAPIWrapper
from langchain_google_community.search import GoogleSearchAPIWrapper
from langchain.tools.base import StructuredTool

def google_tool():
    google_search = GoogleSearchAPIWrapper()
    google_tool = StructuredTool.from_function(
        name="google-search",
        description="Search Google for recent results.",
        func=google_search.run
    )
    return google_tool

def web_tool():
    web_search = WebSearchAPIWrapper()
    web_tool = StructuredTool.from_function(
        name="web-search",
        description="Searches in URL data to get the relavent chunk based on the  user-query.",
        func=web_search.run
    )
    return web_tool

def pdf_tool():
    pdf_search = PDFSearchAPIWrapper()
    pdf_tool = StructuredTool.from_function(
        name="pdf-search",
        description="Searches in pdf to get the relavent chunk based on the  user-query. ",
        func=pdf_search.run
    )
    return pdf_tool

