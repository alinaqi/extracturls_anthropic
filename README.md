
```markdown
# Extract URLs and Data Using FastAPI, Anthropic API, and OpenAI API

This repository contains a FastAPI application that provides two main functionalities:
1. Extract URLs with their page titles and summaries from a website's sitemap using the Anthropic API.
2. Extract structured data from a webpage and convert it to JSON format using OpenAI's API.

## Table of Contents

- [Setup](#setup)
- [Environment Variables](#environment-variables)
- [Running the Application](#running-the-application)
- [Usage](#usage)
  - [API Endpoints](#api-endpoints)
    - [Extract URLs from Sitemap](#extract-urls-from-sitemap)
    - [Extract Data from Web Page](#extract-data-from-web-page)
- [Example](#example)
- [Dependencies](#dependencies)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Setup

To set up the project, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/alinaqi/extracturls_anthropic.git
   cd extracturls_anthropic
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file:**  

   Create a `.env` file in the root directory of the project and add your API keys:

   ```env
   ANTHROPIC_KEY=your_actual_anthropic_api_key
   OPENAI_API_KEY=your_actual_openai_api_key
   ```

## Environment Variables

Make sure to replace `your_actual_anthropic_api_key` and `your_actual_openai_api_key` with your actual API keys in the `.env` file.

## Running the Application

To run the FastAPI application, use the following command:

```bash
uvicorn main:app --reload
```

The application will be available at `http://127.0.0.1:8000`.

## Usage

The application provides two endpoints:

### API Endpoints

#### Extract URLs from Sitemap

- **Endpoint:** **POST** `/extract-urls/`

  - **Request Body:**
    - `url` (string): The URL of the website sitemap to extract URLs from.

  - **Response:**
    - Returns a JSON object containing all extracted URLs, page titles, and summaries.

#### Extract Data from Web Page

- **Endpoint:** **POST** `/extract-data/`

  - **Request Body:**
    - `url` (string): The URL of the webpage to extract data from.

  - **Response:**
    - Returns a JSON object containing the extracted data from the webpage, organized into various entities like metadata, content, products, reviews, FAQs, etc.

## Example

You can use `curl` or any API client like Postman to test the endpoints.

### Extract URLs from Sitemap

**Request:**

```bash
curl -X POST "http://127.0.0.1:8000/extract-urls/" -H "Content-Type: application/json" -d '{"url": "http://www.example.com/sitemap_index.xml"}'
```

**Response:**

```json
{
  "urls": [
    {
      "url": "http://www.example.com/page1",
      "title": "Page 1 Title",
      "summary": "Summary of Page 1"
    },
    {
      "url": "http://www.example.com/page2",
      "title": "Page 2 Title",
      "summary": "Summary of Page 2"
    }
    // more URLs...
  ]
}
```

### Extract Data from Web Page

**Request:**

```bash
curl -X POST "http://127.0.0.1:8000/extract-data/" -H "Content-Type: application/json" -d '{"url": "http://www.example.com"}'
```

**Response:**

```json
{
  "url": "https://www.example.com",
  "metadata": {
    "title": "Page Title",
    "description": "A brief description of the page content",
    "keywords": ["keyword1", "keyword2", "keyword3"],
    "author": "Author Name",
    "language": "en",
    "publish_date": "2024-09-09T12:00:00Z",
    "last_updated": "2024-09-10T12:00:00Z",
    "canonical_url": "https://www.example.com",
    "favicon": "https://www.example.com/favicon.ico",
    "og_tags": {
      "og:title": "Open Graph Title",
      "og:description": "Open Graph Description",
      "og:image": "https://www.example.com/image.jpg",
      "og:type": "website"
    },
    "twitter_tags": {
      "twitter:card": "summary_large_image",
      "twitter:title": "Twitter Title",
      "twitter:description": "Twitter Description",
      "twitter:image": "https://www.example.com/image.jpg"
    }
  },
  "content": {
    "summary": "A brief summary of the page content.",
    "main_topic": "The primary topic or theme of the page",
    "headings": [
      {
        "tag": "h1",
        "text": "Main Heading"
      },
      {
        "tag": "h2",
        "text": "Sub Heading 1"
      }
    ],
    "paragraphs": [
      "Paragraph 1 text...",
      "Paragraph 2 text..."
    ],
    "images": [
      {
        "url": "https://www.example.com/image1.jpg",
        "alt_text": "Description of image 1",
        "caption": "Caption for image 1"
      }
    ],
    // more extracted content...
  }
}
```

## Dependencies

- `fastapi`
- `uvicorn`
- `pydantic`
- `anthropic`
- `openai`
- `python-dotenv`

Install all dependencies using the `requirements.txt` file provided in the repository.

## License

No license.. enjoy ;)

## Acknowledgements

This project uses the [Anthropic API](https://www.anthropic.com/) to interact with a large language model for extracting URLs and information from a website sitemap and the [OpenAI API](https://www.openai.com/) for extracting structured data from a webpage.
```
