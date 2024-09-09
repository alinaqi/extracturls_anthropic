from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import anthropic
import os
import json
import requests
from bs4 import BeautifulSoup
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize the Anthropic client with the API key from the environment
client = anthropic.Anthropic()

class URLRequest(BaseModel):
    url: str

def fetch_sitemap_urls_recursively(sitemap_url):
    """
    Recursively fetch URLs from a sitemap using requests and BeautifulSoup.

    Args:
    - sitemap_url (str): The URL of the sitemap to extract URLs from.

    Returns:
    - List of extracted URLs.
    """
    try:
        print(f"Fetching URLs from sitemap: {sitemap_url}")
        response = requests.get(sitemap_url)
        print("response: ", response)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "lxml")

        # Initialize list to store all URLs
        all_urls = []

        # Find all <sitemap> tags for nested sitemaps
        sitemaps = soup.find_all("sitemap")
        for sitemap in sitemaps:
            loc = sitemap.find("loc").text
            print(f"Found nested sitemap: {loc}")
            all_urls.extend(fetch_sitemap_urls_recursively(loc))

        # Find all <url> tags for actual URLs
        urls = soup.find_all("url")
        for url in urls:
            loc = url.find("loc").text
            print(f"Found URL: {loc}")
            all_urls.append(loc)

        return all_urls
    except Exception as e:
        print(f"Error fetching URLs from sitemap: {e}")
        return []  # Return an empty list on any exception


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

        # Fetch URLs from the sitemap recursively
        print("Extracting URLs from the sitemap...", sitemap_url)
        urls = fetch_sitemap_urls_recursively(sitemap_url)

        # Experimental extraction using gpt-3.5-turbo
        
        url_results = []
        for url in urls:
          completion = openai.chat.completions.create(
              model="gpt-3.5-turbo",
              response_format={"type": "json_object"},
              messages=[
                  {"role": "system", "content": "Get page title the given URL. Return as JSON"},
                  {"role": "user", "content": f"url: {url}"}
              ]
          )
      
          results = completion.choices[0].message.content
          url_results.append(results)

        return url_results

        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


prompt_for_data_extraction = """
Given an HTML page, convert it to JSON, separating out all the key entities from the page e.g. main content, images, reviews, etc. Return as json. The example json is given below. Analyze the page and add any additional entities that may be needed:

{
  "url": "https://www.example.com",  // The URL of the webpage
  "metadata": {
    "title": "Page Title",  // The title of the page
    "description": "A brief description of the page content",  // Meta description for SEO
    "keywords": ["keyword1", "keyword2", "keyword3"],  // Keywords related to the page
    "author": "Author Name",  // Author of the content
    "language": "en",  // Language of the content
    "publish_date": "2024-09-09T12:00:00Z",  // Publication date (if applicable)
    "last_updated": "2024-09-10T12:00:00Z",  // Last update date (if applicable)
    "canonical_url": "https://www.example.com",  // Canonical URL for SEO
    "favicon": "https://www.example.com/favicon.ico",  // URL to the site's favicon
    "og_tags": {  // Open Graph tags for social sharing
      "og:title": "Open Graph Title",
      "og:description": "Open Graph Description",
      "og:image": "https://www.example.com/image.jpg",
      "og:type": "website"
    },
    "twitter_tags": {  // Twitter Card tags for social sharing
      "twitter:card": "summary_large_image",
      "twitter:title": "Twitter Title",
      "twitter:description": "Twitter Description",
      "twitter:image": "https://www.example.com/image.jpg"
    }
  },
  "content": {
    "summary": "A brief summary of the page content.",  // A summary or abstract of the page content
    "main_topic": "The primary topic or theme of the page",  // The main topic or theme
    "headings": [  // List of all headings on the page
      {
        "tag": "h1",
        "text": "Main Heading"
      },
      {
        "tag": "h2",
        "text": "Sub Heading 1"
      }
    ],
    "paragraphs": [  // List of all paragraphs on the page
      "Paragraph 1 text...",
      "Paragraph 2 text..."
    ],
    "images": [  // List of images on the page
      {
        "url": "https://www.example.com/image1.jpg",
        "alt_text": "Description of image 1",
        "caption": "Caption for image 1"
      }
    ],
    "videos": [  // List of videos on the page
      {
        "url": "https://www.example.com/video1.mp4",
        "title": "Title of the video",
        "description": "Description of the video",
        "thumbnail": "https://www.example.com/video_thumbnail.jpg"
      }
    ],
    "links": [  // List of internal and external links
      {
        "text": "Link Text",
        "url": "https://www.example.com/some-link",
        "type": "internal"  // Can be 'internal' or 'external'
      }
    ]
  },
  "products": [  // List of products (if any)
    {
      "product_id": "12345",
      "name": "Product Name",
      "description": "Product Description",
      "price": {
        "amount": 99.99,
        "currency": "USD"
      },
      "availability": "In Stock",  // or "Out of Stock"
      "categories": ["Category 1", "Category 2"],
      "images": [
        {
          "url": "https://www.example.com/product_image.jpg",
          "alt_text": "Product Image"
        }
      ],
      "reviews": [  // List of reviews for the product
        {
          "review_id": "98765",
          "author": "Reviewer Name",
          "rating": 4.5,
          "date": "2024-09-09",
          "text": "Review text here..."
        }
      ]
    }
  ],
  "reviews": [  // General reviews (if the page is a review page)
    {
      "review_id": "54321",
      "author": "Reviewer Name",
      "rating": 4.0,
      "date": "2024-09-09",
      "title": "Review Title",
      "text": "Detailed review text...",
      "product_id": "12345"  // ID of the product being reviewed (if applicable)
    }
  ],
  "faqs": [  // Frequently Asked Questions
    {
      "question": "What is the product made of?",
      "answer": "The product is made of high-quality materials."
    }
  ],
  "comments": [  // User comments or discussion (if applicable)
    {
      "comment_id": "23456",
      "author": "Commenter Name",
      "date": "2024-09-09T12:00:00Z",
      "text": "This is a comment text.",
      "replies": [
        {
          "comment_id": "23457",
          "author": "Reply Author",
          "date": "2024-09-10T12:00:00Z",
          "text": "This is a reply to the comment."
        }
      ]
    }
  ],
  "sidebar": {  // Sidebar content (if applicable)
    "related_articles": [  // Related articles or links
      {
        "title": "Related Article 1",
        "url": "https://www.example.com/related-article-1"
      }
    ],
    "advertisements": [  // Advertisements present on the page
      {
        "ad_id": "ad123",
        "image_url": "https://www.example.com/ad.jpg",
        "target_url": "https://www.example.com/ad-target",
        "description": "Ad description"
      }
    ]
  },
  "footer": {  // Footer information
    "links": [  // List of links in the footer
      {
        "text": "Privacy Policy",
        "url": "https://www.example.com/privacy-policy"
      }
    ],
    "contact_info": {  // Contact information if available in the footer
      "email": "contact@example.com",
      "phone": "+1-234-567-8900"
    },
    "social_media": [  // Social media links if available in the footer
      {
        "platform": "Twitter",
        "url": "https://twitter.com/example"
      }
    ]
  }
}

Return as JSON.

"""
@app.post("/extract-data/")
async def extract_data(request: str):
    completion = openai.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": prompt_for_data_extraction},
                {"role": "user", "content": f"url: {request}"}
            ]
        )
    
    results = completion.choices[0].message.content

    return results

# Run the application with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
