import asyncio
from fastapi import FastAPI, WebSocket

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


@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    try:
        await asyncio.sleep(.1)
        data = await websocket.receive_json()
        query = data.get("query")
        search_results = search_service.web_search(query)
        await asyncio.sleep(.1)
        await websocket.send_json(
            {
                "type": "search_results",
                "data": search_results
            }
            )
        sorted_result = sort_source_service.sort_sources(query, search_results)
        print(sorted_result)
        for chunk in llm_service.generate_response(query, sorted_result):
            await asyncio.sleep(.1)
            await websocket.send_json(
                {
                    "type": "content",
                    "data": chunk.to_dict()  # Convert to dictionary
                }
            )
    except Exception as e:
        print(e)
    finally:
        await websocket.close()
    
# chat
@app.post("/chat")
def send_chat(body: ChatBody):
    # Search the web and find appropriate sources
    # sort the sources
    # generate the response using LLM
    search_results = search_service.web_search(body.query)
    sorted_result = sort_source_service.sort_sources(body.query, search_results)
    llm_response = llm_service.generate_response(body.query, sorted_result)
    return [chunk.to_dict() for chunk in llm_response]  # Convert each chunk to dictionary