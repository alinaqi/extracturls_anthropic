
```markdown
# Extract URLs Using FastAPI and Anthropic API

This repository contains a FastAPI application that takes a URL of a website's sitemap as input and extracts all the URLs with their page titles and summaries using the Anthropic API.

## Table of Contents

- [Setup](#setup)
- [Environment Variables](#environment-variables)
- [Running the Application](#running-the-application)
- [Usage](#usage)
- [API Endpoint](#api-endpoint)
- [Example](#example)
- [Dependencies](#dependencies)

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

   Create a `.env` file in the root directory of the project and add your Anthropic API key:

   ```env
   ANTHROPIC_KEY=your_actual_anthropic_api_key
   ```

## Environment Variables

Make sure to replace `your_actual_anthropic_api_key` with your actual Anthropic API key in the `.env` file.

## Running the Application

To run the FastAPI application, use the following command:

```bash
uvicorn main:app --reload
```

The application will be available at `http://127.0.0.1:8000`.

## Usage

The application provides an endpoint that accepts a URL of a website's sitemap and returns all URLs within the sitemap, including page titles and summaries.

### API Endpoint

- **POST** `/extract-urls/`

  - **Request Body:**
    - `url` (string): The URL of the website sitemap to extract URLs from.

  - **Response:**
    - Returns a JSON object containing all extracted URLs, page titles, and summaries.

### Example

You can use `curl` or any API client like Postman to test the endpoint.

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

## Dependencies

- `fastapi`
- `uvicorn`
- `pydantic`
- `anthropic`
- `python-dotenv`

Install all dependencies using the `requirements.txt` file provided in the repository.

## License

No license.. enjoy ;)

## Acknowledgements

This project uses the [Anthropic API](https://www.anthropic.com/) to interact with a large language model for extracting URLs and information from a website sitemap.
```