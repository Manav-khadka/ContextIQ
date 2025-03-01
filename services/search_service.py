from config import Settings
from tavily import TavilyClient
import trafilatura

settings = Settings()
tavily_client = TavilyClient(api_key=settings.TAVILY_API_KEY)
class SearchService:
    def web_search(self, query: str):
        results = []
        response = tavily_client.search(query, max_results=5)
        search_results = response.get("results", [])
        print(search_results)
        for result in search_results:
            url = result.get("url")
            if url:
                downloaded = trafilatura.fetch_url(url)
                content = trafilatura.extract(downloaded, include_comments=False)
                results.append(
                    {
                        "title": result.get("title"),
                        "url": url,
                        "content": content  
                    }
                )
            
        return results  