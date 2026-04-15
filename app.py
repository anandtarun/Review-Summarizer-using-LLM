import time
import pandas as pd
from scraper import scrape_reviews
from preprocess import preprocess_reviews
from llm import analyze_review_with_llm


def main():
    # 1. Configuration
    # Replace this with the publicly available product page URL you chose
    target_url = "https://www.goodreads.com/book/show/54493401-project-hail-mary"

    # 2. Extract
    print("Starting data extraction...")
    raw_reviews = scrape_reviews(target_url, max_pages=2)
    df = pd.DataFrame(raw_reviews)

    if df.empty:
        print("No data scraped. Exiting.")
        return

    # 3. Transform (Preprocess)
    print("Preprocessing data...")
    df = preprocess_reviews(df)

    # 4. Transform (LLM Analysis)
    print("Sending data to Gemini for sentiment and summary analysis...")
    llm_results = []

    # Process sequentially to avoid aggressive rate limiting
    for index, row in df.iterrows():
        print(f"Processing review {index + 1}/{len(df)}...")

        # Add [:1500] to truncate the text!
        # If the scraper accidentally grabbed the whole page, this saves your quota.
        safe_text = row['cleaned_review'][:1500]
        analysis = analyze_review_with_llm(safe_text)

        llm_results.append(analysis)
        time.sleep(5)  # Gentle delay between API calls

    df['llm_analysis'] = llm_results

    # 5. Load (Save Data)
    output_filename = "processed_reviews.csv"
    df.to_csv(output_filename, index=False, encoding='utf-8')
    print(f"Process complete. Data successfully saved to {output_filename}")


if __name__ == "__main__":
    # Ensure environment variables are checked/set before running the main logic
    import os

    if not os.environ.get("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY environment variable is missing.")
        print(
            "Please set it using: export GEMINI_API_KEY='your_key' (Linux/Mac) or set GEMINI_API_KEY='your_key' (Windows)")
    else:
        main()