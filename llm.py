
import os
import time
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions


def initialize_gemini():
    """Initializes and returns the Gemini model."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Critical Rule: GEMINI_API_KEY environment variable is not set.")

    genai.configure(api_key=api_key)
    # gemini-2.5-flash is ideal for high-volume ETL tasks
    return genai.GenerativeModel('gemini-2.5-flash')


# Initialize the model at the module level
model = initialize_gemini()


def analyze_review_with_llm(review_text: str, retries: int = 3) -> str:
    #Calls the Gemini API to summarize and analyze sentiment
    if not review_text:
        return "No text provided."

    prompt = f"""
    Analyze the following product review. 
    1. Identify the overall sentiment (Positive, Negative, or Neutral).
    2. Provide a 1-2 sentence concise summary of the key points.

    Review: {review_text}

    Output Format:
    Sentiment: [Sentiment]
    Summary: [Summary]
    """

    for attempt in range(retries):
        try:
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3,
                    max_output_tokens=150,
                )
            )
            return response.text.strip()

        except google_exceptions.ResourceExhausted:
            wait_time = (2 ** attempt) * 2  # Exponential backoff
            print(f"Rate limit hit. Waiting {wait_time} seconds...")
            time.sleep(wait_time)
        except google_exceptions.GoogleAPIError as e:
            print(f"Google API Error: {e}")
            return "Error: API Failure"
        except Exception as e:
            print(f"Unexpected Error during Gemini call: {e}")
            return "Error: Unexpected Failure"

    return "Error: Max retries exceeded"