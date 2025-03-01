from typing import List
import google.generativeai as genai

from config import Settings

settings = Settings()

class LLMService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-2.0-flash")
    def generate_response(self, query: str, sorted_result: List[dict]):
        context_text = '\n\n'.join(
            [
                f"Source {i+1} {result['url']}:\n{result['content']}"
                for i, result in enumerate(sorted_result)
            ]
        )
        print(context_text)
        full_prompt = f"""
        Context from the web: {context_text}
        
        Query: {query}
        
        Please Provide a comprehensive, detailed, well-cited accurate response using the above context. Think and reason deeply. Ensure it answers the query the user has asked. Do not use your own knowledge until it is absolutely neccessary.
        """
        
        response = self.model.generate_content(full_prompt)
        
        return response.text