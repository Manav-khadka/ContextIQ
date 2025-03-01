from fastapi import FastAPI

from pydantic_models.chat_body import ChatBody
from services.search_service import SearchService
from services.sort_source_service import SortSourceService


app = FastAPI()

search_service = SearchService()
sort_source_service = SortSourceService()

@app.get("/read_root")
def read_root():
    return {"Hello": "World"}

# chat
@app.post("/chat")
def send_chat(body: ChatBody):
    # Search the web and find appropriate sources
    # sort the sources
    # generate the response using LLM
    search_results = search_service.web_search(body.query)
    sorted_query = sort_source_service.sort_sources(body.query, search_results)
    return {"chat_response": {"query": body.query, "length":len(search_results), "search_results": search_results, "sorted_query": sorted_query}}