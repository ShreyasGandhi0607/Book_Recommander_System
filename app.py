from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
import pickle
import numpy as np
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
# Initialize Gemini API
GEMINI_API_KEY=os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)  

# Load pre-trained models and data
popular_df = pickle.load(open('notebook/popular.pkl', 'rb'))
pt = pickle.load(open('notebook/pt.pkl', 'rb'))
books = pickle.load(open('notebook/books.pkl', 'rb'))
similarity_score = pickle.load(open('notebook/similarity_score.pkl', 'rb'))

app = Flask(__name__)
app.secret_key = 'my-secret-key' 

# Gemini function for generating book summaries
def generate_book_summary(book_title):
    try:
        # Initialize the Generative Model
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = (
            f"Provide a concise, engaging summary of the book '{book_title}'. "
            f"Focus on the main plot, key themes, and what makes this book unique. Keep it under 200 words."
        )

        # Generate content
        response = model.generate_content(prompt)

        # Check if the response contains the required content
        if hasattr(response, 'text') and response.text:
            # print("Generated Summary:", response.text)
            return response.text
        else:
            print("Response Missing 'text':", response)
            return "Summary not available."

    except Exception as e:
        # Log the detailed error
        print(f"Error in generating summary: {e}")
        return "Summary not available due to an error."



@app.route('/')
def index():
    return render_template(
        "index.html",
        book_name=list(popular_df['Book-Title'].values),
        author=list(popular_df['Book-Author'].values),
        image=list(popular_df['Image-URL-M'].values),
        num_votes=list(popular_df['num_rating'].values),
        rating=list(popular_df['avg_rating'].values),
    )

@app.route("/top-50")
def top_50():
    return render_template(
        "top50.html",
        book_name=list(popular_df['Book-Title'].values),
        author=list(popular_df['Book-Author'].values),
        image=list(popular_df['Image-URL-M'].values),
        num_votes=list(popular_df['num_rating'].values),
        rating=list(popular_df['avg_rating'].values),
    )

@app.route("/recommand")
def recommand_ui():
    return render_template("recommand.html")

@app.route("/get_book_summary", methods=["POST"])
def get_book_summary():
    book_title = request.form.get('book_title')
    summary = generate_book_summary(book_title)
    return jsonify({"summary": summary})

@app.route("/recommand_books", methods=["POST"])
def recommand():
    user_input = request.form.get('user_input')
    app.logger.debug(f"User Input: {user_input}")

    # Check if user input is empty
    if not user_input:
        app.logger.debug("User input is empty.")
        flash('Please enter a book name!', 'warning')
        return redirect(url_for('recommand_ui'))

    # Ensure the book exists in the pivot table index
    if user_input not in pt.index:
        app.logger.debug(f"Book not found in pivot table index: {user_input}")
        flash('Book not found. Please try another title.', 'warning')
        return redirect(url_for('recommand_ui'))

    # Similar books logic
    try:
        index = np.where(pt.index == user_input)[0][0]
        app.logger.debug(f"Book index in pivot table: {index}")
        similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:6]

        data = []
        for i in similar_items:
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            book_title = temp_df['Book-Title'].values[0]
            app.logger.debug(f"Found similar book: {book_title}")
            item = [
                book_title,
                temp_df['Book-Author'].values[0],
                temp_df['Image-URL-M'].values[0],
                generate_book_summary(book_title)  # Generate summary
            ]
            data.append(item)

        return render_template("recommand.html", data=data, Title=user_input)
    except Exception as e:
        app.logger.error(f"Error during recommendation: {e}")
        flash('An error occurred while generating recommendations.', 'danger')
        return redirect(url_for('recommand_ui'))


# Route for book suggestions (autocomplete)
@app.route("/suggest_books", methods=["GET"])
def suggest_books():
    query = request.args.get('query', '').lower()
    suggestions = []

    if query:
        suggestions = [title for title in books['Book-Title'].unique() if query in title.lower()][:5]

    return jsonify({"suggestions": suggestions})

if __name__ == "__main__":
    app.run(debug=True)
