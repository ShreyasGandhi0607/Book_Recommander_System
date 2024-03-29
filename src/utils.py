import os
import sys
import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.impute import SimpleImputer

from src.exception import CustomException

def save_object(file_path, obj):
    try:
        # Extract directory path from the file path
        dir_path = os.path.dirname(file_path)
        
        # Create directory if it doesn't exist
        os.makedirs(dir_path, exist_ok=True)

        # Save the object to file
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        # Handle exceptions and raise CustomException
        raise CustomException(e, sys)

def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)

    except Exception as e:
        raise CustomException(e, sys)

def calculate_cosine_similarity(file_path):
    try:
        # Read the CSV file
        new_book = pd.read_csv('notebook/data/final_books.csv')
        
        # Impute NaN values using mean imputation
        imputer = SimpleImputer(strategy='mean')
        new_book_imputed = imputer.fit_transform(new_book.drop(columns=['Title', 'Author']))

        # Calculate cosine similarity between all pairs of books based on their features
        similarity_matrix = cosine_similarity(new_book_imputed)
        return similarity_matrix

    except Exception as e:
        raise CustomException(e, sys)

def recommend_books(book_title, new_book, similarity_matrix, num_recommendations=5):
    try:
        # Find the index of the book in the DataFrame
        books = pd.read_csv('notebook/data/final_books.csv')

        book_index = books[books['Title'] == book_title].index[0]
        
        # Get similarity scores for the book with other books
        sim_scores = list(enumerate(similarity_matrix[book_index]))
        
        # Sort the books based on similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Get the indices of the top similar books (excluding the book itself)
        similar_books_indices = [i for i, _ in sim_scores[1:num_recommendations+1]]
        
        # Return the titles, genres, and subgenres of recommended books
        recommended_books = books.iloc[similar_books_indices][['Title', 'Genre', 'Subgenre']]
        return recommended_books

    except Exception as e:
        raise CustomException(e, sys)
