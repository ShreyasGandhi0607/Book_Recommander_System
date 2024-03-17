import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder
from src.logger import logging  # Import logger from logger.py

def transform_data(book):
    # Drop rows with missing titles
    logging.info("Dropping rows with missing titles")
    book = book.dropna(subset=['Title'])

    # Tokenize and extract features from titles and authors using TF-IDF
    logging.info("Tokenizing and extracting features from titles and authors using TF-IDF")
    title_vectorizer = TfidfVectorizer()
    title_features = title_vectorizer.fit_transform(book['Title'])

    author_vectorizer = TfidfVectorizer()
    author_features = author_vectorizer.fit_transform(book['Author'])

    # One-hot encode Genre and SubGenre columns
    logging.info("One-hot encoding Genre and SubGenre columns")
    genre_dummies = pd.get_dummies(book['Genre'], prefix='Genre')
    subgenre_dummies = pd.get_dummies(book['SubGenre'], prefix='SubGenre')

    # Concatenate the original DataFrame with the new features
    logging.info("Concatenating the original DataFrame with the new features")
    new_book = pd.concat([book, 
                        pd.DataFrame(title_features.toarray(), columns=title_vectorizer.get_feature_names_out()),
                        pd.DataFrame(author_features.toarray(), columns=author_vectorizer.get_feature_names_out()),
                        genre_dummies, subgenre_dummies], axis=1)

    # Drop original categorical columns and other irrelevant columns
    
    logging.info("Data transformation completed")
    return new_book

# Example usage
if __name__ == "__main__":
    # Load your data
    book_data = pd.read_csv('notebook/data/final_books.csv')
    
    # Transform the data
    transformed_data = transform_data(book_data)
