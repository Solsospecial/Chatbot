from typing import Optional
from langchain_core.callbacks.manager import CallbackManagerForToolRun
from langchain_core.pydantic_v1 import BaseModel, Extra
from langchain_core.tools import BaseTool

class PDFSearchAPIWrapper(BaseModel):
    """Wrapper for PDF Search API."""
    api_url:str= "http://127.0.0.1:8000"  # The API URL for searching in PDFs
    k: int = 10  # The number of results to return

    class Config:
        """Configuration for this pydantic object."""
        extra = Extra.forbid

    def _pdf_search_results(self, search_term: str) -> str:
        import requests
        response = requests.post(f"{self.api_url}/search_query_in_pdf", json={"input": search_term})
        if response.status_code == 200:
            return response.json()
        else:
            return "❌ Failed to fetch results!"

    def run(self, query: str) -> str:
        """Run query through PDF Search and parse the result."""
        return self._pdf_search_results(query)

class PDFSearchRun(BaseTool):
    """Tool that queries the PDF search API."""
    name: str = "pdf_search"
    description: str = (
        "A wrapper around PDF Search API."
        "Useful for searching relevant information within PDF documents."
        "Input should be a search query."
    )
    api_wrapper: PDFSearchAPIWrapper

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        return self.api_wrapper.run(query)