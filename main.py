from fastapi import FastAPI

from pydantic_models.chat_body import ChatBody
from services.search_service import SearchService


app = FastAPI()

search_service = SearchService()

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
    print(body.query)
    return {"chat_response": {"query": body.query, "search_results": search_results}}