# Review Summarizer using LLM

## Features
- Scrapes product reviews
- Cleans and preprocesses text
- Uses Google gemini API for summarization
- Handles rate limits and errors
- Stores results in CSV

## How to Run

1. Clone repo
2. Install dependencies:
   pip install -r requirements.txt

3. Set API key:

4. Run:
   python app.py

## Example URL
Goodreads product review page

## Output
CSV file with:
- Review text
- Metadata
- LLM summary

## Limitations
- Site structure dependent
- Limited pages scraped