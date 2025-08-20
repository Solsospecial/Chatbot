import requests
from typing import Optional
from langchain_core.callbacks.manager import CallbackManagerForToolRun
from pydantic import BaseModel, ConfigDict
from langchain_core.tools.base import BaseTool

class WebSearchAPIWrapper(BaseModel):
    """Wrapper for Web Search API."""
    api_url:str= "http://127.0.0.1:8000"  # The API URL for searching the web
    k: int = 10  # The number of results to return
    model_config = ConfigDict(extra="forbid")
    
    def _web_search_results(self, search_term: str) -> str:
        response = requests.post(f"{self.api_url}/search_query_in_web", json={"input": search_term})
        if response.status_code == 200:
            return response.json()
        else:
            return "❌ Failed to fetch results!"

    def run(self, query: str) -> str:
        """Run query through Web Search and parse the result."""
        return self._web_search_results(query)

class WebSearchRun(BaseTool):
    """This tool queries the Web search API."""
    name: str = "web_search"
    description: str = (
        "A wrapper around Web Search API."
        "Useful for searching relevant information on the web."
        "Input should be a search query."
    )
    api_wrapper: WebSearchAPIWrapper

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        return self.api_wrapper.run(query)