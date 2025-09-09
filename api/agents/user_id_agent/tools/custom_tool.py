from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import base64
from openai import OpenAI
import os
import json

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class OCRToolInput(BaseModel):
    """Input schema for OCRTool."""
    image_path: str = Field(..., description="Path to the ID image file.")


class OCRTool(BaseTool):
    """
    A custom tool that performs OCR using OpenAI's GPT-4o model with base64-encoded images.
    """
    name: str = "ocr_tool"
    description: str = "Extracts key fields from an image using OpenAI's GPT-4o model."
    args_schema: Type[BaseModel] = OCRToolInput

    def _run(self, image_path: str) -> str:
        """
        Perform OCR on the given image using OpenAI's GPT-4o API.
        """
        try:
            # Convert the local image to a base64 string
            if not os.path.exists(image_path):
                return f"Error: File not found at {image_path}. Ensure the file exists."

            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode("utf-8")
                print("Image successfully converted to base64 string.")

            # Construct the base64 image string
            base64_img = f"data:image/png;base64,{base64_image}"

            # Make the API call using OpenAI
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Return JSON document with data. Only return JSON not other text."},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"{base64_img}"}
                            }
                        ],
                    }
                ],
                max_tokens=500,
                temperature=1,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )

            print("API call successful.")
            return response.choices[0].message.content

        except FileNotFoundError:
            return f"Error: File not found at {image_path}. Ensure the file exists."
        except json.JSONDecodeError:
            return "Error: Unable to decode JSON from the response. Check the API output."
        except Exception as e:
            return f"Error during OCR: {str(e)}"
