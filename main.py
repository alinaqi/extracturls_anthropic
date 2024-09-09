from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import anthropic
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Initialize the Anthropic client with the API key from the environment
client = anthropic.Anthropic()

class URLRequest(BaseModel):
    url: str

@app.post("/extract-urls/")
async def extract_urls(request: URLRequest):
    try:

        # first get the sitemap from a url
        message = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1024,
            system="Given the attached sitemap website, check the sitemap file where entire sitemap is contains. Return the sitemap link then. Return only sitemap link and no additional data as json.",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"sitemap: {request.url}"
                        }
                    ]
                }
            ]
        )

        sitemap_url = message.content
        print("sitemap url: ", sitemap_url)
        
        # Check if the response is a list and contains an element with a 'text' field
        if isinstance(sitemap_url, list) and len(sitemap_url) > 0:
            # Extract the 'text' field which contains a JSON string
            text_block = sitemap_url[0].text
            
            # Parse the JSON string to extract the URL
            try:
                parsed_json = json.loads(text_block)
                sitemap_url = parsed_json.get('sitemap', None)

                if sitemap_url:
                    print("clear sitemap url:", sitemap_url)
                else:
                    print("No sitemap URL found in the response.")
                    return
            except json.JSONDecodeError:
                print("Failed to parse JSON from the response.")
        else:
            print("Invalid response format from the API.")

        # Generate a message to send to the Anthropic API
        print("Extracting URLs from the sitemap...", sitemap_url)
        message = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1024,
            temperature=0,
            system="Given the  sitemap url, extract all urls with the page title and summary. Return as JSON with no additional comments.",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"sitemap: {sitemap_url}"
                        }
                    ]
                }
            ]
        )

        # Extract the content from the response
        content = message.content
        print("sitemap content: ", content)


        if content:
            return {"urls": content}
        else:
            raise HTTPException(status_code=500, detail="Failed to extract URLs from the sitemap.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the application with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
