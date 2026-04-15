import re
import pandas as pd


def clean_text(text: str) -> str:
    #Removes excess whitespace, newlines, and unwanted characters
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def preprocess_reviews(df: pd.DataFrame) -> pd.DataFrame:
    #Applies cleaning to the review dataframe
    if df.empty:
        return df

    df['cleaned_review'] = df['review_text'].apply(clean_text)
    return df