# from pydantic import BaseModel
# import requests
# from pydantic_models import QueryRequest

# class WebQuestionAnswering(BaseModel):
#     name: str = "Web Question Answering"
#     description: str = "Useful to Answer user based on query from webdata."

#     def run(self, query: str) -> str:
#         try:
#             print(query)
#             request_data=QueryRequest(input=query)
#             response = requests.post(f"http://127.0.0.1:8000/search_query_in_web", json=request_data.dict())
#             response.raise_for_status()
#             return response.json()
#         except requests.RequestException as e:
#             # Handle request errors
#             return {"error": f"Request failed: {str(e)}"}
#         except Exception as e:
#             # Handle other exceptions
#             return {"error": str(e)}

from typing import Any, Dict, Optional
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.pydantic_v1 import BaseModel, Extra
from langchain_core.tools import BaseTool

class WebSearchAPIWrapper(BaseModel):
    """Wrapper for Web Search API."""

    api_url:str= "http://127.0.0.1:8000"  # The API URL for searching the web
    k: int = 10  # Number of results to return

    class Config:
        """Configuration for this pydantic object."""
        extra = Extra.forbid

    def _web_search_results(self, search_term: str) -> str:
        # Implement the logic to call your web search API and return the response.
        import requests
        response = requests.post(f"{self.api_url}/search_query_in_web", json={"input": search_term})
        if response.status_code == 200:
            return response.json()
        else:
            return "Failed to fetch results"

    def run(self, query: str) -> str:
        """Run query through Web Search and parse result."""
        return self._web_search_results(query)


class WebSearchRun(BaseTool):
    """Tool that queries the Web search API."""

    name: str = "web_search"
    description: str = (
        "A wrapper around Web Search API. "
        "Useful for searching relevant information on the web. "
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
