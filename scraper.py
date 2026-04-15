import time
import requests
from bs4 import BeautifulSoup
from utils import HEADERS


def scrape_reviews(url: str, max_pages: int = 1) -> list:
    """Scrapes review data from a given product URL."""
    reviews_data = []

    for page in range(1, max_pages + 1):
        # Handle pagination depending on the site structure
        page_url = f"{url}&pageNumber={page}" if "?" in url else f"{url}?pageNumber={page}"
        print(f"Scraping page {page}...")

        try:
            response = requests.get(page_url, headers=HEADERS, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Network error on page {page}: {e}")
            break

        soup = BeautifulSoup(response.content, 'html.parser')

        # EXTRACTION
        review_cards = soup.find_all('article', class_='ReviewCard')
        print(f"--> Found {len(review_cards)} review cards on page {page}.")

        for card in review_cards:
            try:
                # 2. Find the specific section holding the text
                text_section = card.find('section', class_='ReviewText__content')

                # If a user just left 5 stars but no written text, skip them
                if not text_section:
                    continue

                    # Extract the clean paragraph
                raw_text = text_section.get_text(separator=' ', strip=True)

                # Basic sanity check to ensure it's not empty
                if len(raw_text) < 15:
                    continue

                # 3. Get Metadata (Author)
                # Goodreads stores the name in the 'ReviewerProfile__name' class
                author_elem = card.find(class_='ReviewerProfile__name')
                author = author_elem.get_text(strip=True) if author_elem else "Goodreads User"

                # 4. Append the clean data!
                reviews_data.append({
                    'author': author,
                    'rating': "N/A",  # Star ratings use hidden SVGs here, so we skip them to keep the pipeline fast
                    'date': "N/A",
                    'review_text': raw_text
                })

            except Exception as e:
                print(f"--> Error extracting review data: {e}")
                continue

        time.sleep(2)  # Polite delay between page requests

    return reviews_data