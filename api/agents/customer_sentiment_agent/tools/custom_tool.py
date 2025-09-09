import json
import requests
from crewai_tools import BaseTool
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()


from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field


# class MyCustomToolInput(BaseModel):
#     """Input schema for MyCustomTool."""
#     argument: str = Field(..., description="Description of the argument.")

# class MyCustomTool(BaseTool):
#     name: str = "Name of my tool"
#     description: str = (
#         "Clear description for what this tool is useful for, you agent will need this information to use it."
#     )
#     args_schema: Type[BaseModel] = MyCustomToolInput

#     def _run(self, argument: str) -> str:
#         # Implementation goes here
#         return "this is an example of a tool output, ignore it and move along."



# class BrowserlessScrapingTool(BaseTool):
#     """Custom Scraping Tool using Browserless API to fetch HTML content."""

#     # def __init__(self: str):
#     #     self.api_token = os.getenv('BROWSERLESS_API_KEY')

#     def _run(self, url: str) -> dict:
#         """
#         Scrapes a webpage using Browserless API to retrieve HTML content.

#         :param url: URL of the webpage to scrape
#         :return: Dictionary containing the HTML content or error details
#         """
#         print("Scraping URL:", url)
#         return url
#         response = requests.post("https://production-sfo.browserless.io/unblock",
#                             params={ "token": os.getenv('BROWSERLESS_API_KEY')},
#                             json={
#                                 "waitForTimeout": 5000,
#                                 "url": f"{url}"
#                             }
#         )
 
#         html_content = json.loads(response.text)['content']
        
#         return {"url": url, "html": html_content}

