from flask import Flask, request, render_template
from src.components.model_trainer import train_recommendation_model
from src.utils import load_object
from src.logger import logging
import requests

application = Flask(__name__)

# Train the recommendation model on application startup
transformed_data, similarity_matrix = train_recommendation_model('notebook/data/final_books.csv')
logging.info("Model trained successfully.")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        book_title = request.form['Title']
        # Perform book recommendation based on the provided title
        recommended_books = get_recommended_books(book_title)
        return render_template('response.html', Title=book_title, books=recommended_books)
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    book_title = request.form['Title']
    # Perform book recommendation based on the provided title
    recommended_books = get_recommended_books(book_title)
    return render_template('response.html', Title=book_title, books=recommended_books)

def get_recommended_books(book_title):
    # Load transformed data and similarity matrix
    transformed_data = load_object('artifacts/transformed_data.pkl')
    similarity_matrix = load_object('artifacts/similarity_matrix.pkl')
    
    # Check if the provided book title exists in the dataset
    if book_title not in transformed_data['Title'].values:
        return None  # Return None if the book title doesn't exist
    
    # Get the index of the provided book title
    book_index = transformed_data.index[transformed_data['Title'] == book_title].tolist()[0]
    
    # Get the corresponding author for the provided book title
    book_author = transformed_data.iloc[book_index]['Author']

    # Implement logic to get recommended books based on the provided title
    recommended_books = recommend_books(book_title, transformed_data, similarity_matrix)
    
    # Format the recommendations including author names and cover image URL
    formatted_recommendations = []
    for title in recommended_books:
        # Fetch book information using Google Books API
        book_info = fetch_book_info_by_title_and_author(title, book_author)
        if book_info:
            formatted_recommendations.append(book_info)
    
    return formatted_recommendations


def fetch_book_info_by_title_and_author(title, author):
    # Google Books API endpoint URL
    api_url = "https://www.googleapis.com/books/v1/volumes"
    
    # Parameters for the API request
    params = {
        'q': f'intitle:{title}+inauthor:{author}',
        'maxResults': 1  # Limiting to one result for simplicity
    }
    
    # Make a GET request to the Google Books API
    response = requests.get(api_url, params=params)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # Check if any items were returned
        if 'items' in data and len(data['items']) > 0:
            # Extract relevant book information
            book_info = data['items'][0]
            return {
                'title': title,
                'authors': [author],
                'cover_url': book_info['volumeInfo'].get('imageLinks', {}).get('thumbnail', None)
            }
    # If the request fails or no items are found, return None
    return None


# Example function for book recommendation
import numpy as np

def recommend_books(book_title, transformed_data, similarity_matrix, top_n=6):
    # Find the index of the provided book title
    book_index = transformed_data.index[transformed_data['Title'] == book_title].tolist()[0]

    # Calculate similarity scores between the provided book and all other books
    similarity_scores = similarity_matrix[book_index]

    # Sort the similarity scores in descending order and get the indices of the top recommendations
    top_indices = np.argsort(similarity_scores)[::-1][:top_n]

    # Get the titles of the recommended books
    recommended_books = transformed_data.iloc[top_indices]['Title'].tolist()

    return recommended_books

if __name__ == '__main__':
    application.run(host="0.0.0.0", port=8000)  # Change the port number as needed
