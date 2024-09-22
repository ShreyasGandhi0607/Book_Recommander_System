from flask import Flask, render_template, request, flash, redirect, url_for
import pickle
import numpy as np

# Load your models and data
popular_df = pickle.load(open('notebook/popular.pkl', 'rb'))
pt = pickle.load(open('notebook/pt.pkl', 'rb'))
books = pickle.load(open('notebook/books.pkl', 'rb'))
similarity_score = pickle.load(open('notebook/similarity_score.pkl', 'rb'))

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages


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


@app.route("/recommand")
def recommand_ui():
    return render_template("recommand.html")


@app.route("/recommand_books", methods=["POST"])
def recommand():
    user_input = request.form.get('user_input')

    # Check if user input is empty
    if not user_input:
        flash('Please enter a book name!', 'warning')
        return redirect(url_for('recommand_ui'))

    # Ensure the book exists in the pivot table index before proceeding
    if user_input not in pt.index:
        flash('Book not found. Please try another title.', 'warning')
        return redirect(url_for('recommand_ui'))

    # Find the index and similar items
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:6]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend([
            temp_df['Book-Title'].values[0],
            temp_df['Book-Author'].values[0],
            temp_df['Image-URL-M'].values[0]
        ])
        data.append(item)

    return render_template("recommand.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)
