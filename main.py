from fastapi import FastAPI

from pydantic_models.chat_body import ChatBody
from services.llm_service import LLMService
from services.search_service import SearchService
from services.sort_source_service import SortSourceService


app = FastAPI()

search_service = SearchService()
sort_source_service = SortSourceService()
llm_service = LLMService()

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
    sorted_result = sort_source_service.sort_sources(body.query, search_results)
    llm_response = llm_service.generate_response(body.query, sorted_result)
    return llm_response