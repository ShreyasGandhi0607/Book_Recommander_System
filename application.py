from flask import Flask, render_template, request

from src.utils import recommend_books
import pandas as pd
from src.utils import recommend_books
from src.utils import calculate_cosine_similarity
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

import requests

API_KEY = "AIzaSyCQ63CkSTVFecJCyWrTR7Xi3oIAFf0d9ik"  # Replace with your actual API key

def get_book_cover_url(book_title):
    """
    Searches for a book by title using the Google Books API and returns the cover image URL.

    Args:
        book_title (str): The title of the book to search for.

    Returns:
        str: The cover image URL if found, otherwise None.
    """

    base_url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": book_title,
        "key": API_KEY,
        "fields": "items(volumeInfo/imageLinks/thumbnail)"  # Specify desired fields
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        items = data.get("items", [])

        if items:
            # Assuming the first result is the desired book
            image_link = items[0]["volumeInfo"].get("imageLinks", {}).get("thumbnail")
            return image_link
        else:
            print(f"Book '{book_title}' not found in Google Books results.")
            return None
    else:
        print(f"Error: {response.status_code}")
        return None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    Title = request.form["title"]
    similarity_matrix = calculate_cosine_similarity()
    new_book = pd.read_csv('notebook/data/final_books.csv')

    recommended_books = recommend_books(new_book['Title'])  # Assuming you have a `recommend_books` function

    for book in recommended_books:
        book["cover_url"] = get_book_cover_url(book["volumeInfo"]["title"])  # Add cover URL

    return render_template("recommend.html", books=recommended_books, title=title)

if __name__ == "__main__":
    app.run(debug=True)
