# Book Recommendation System

A Flask-based web application that recommends books to users based on their input. The application uses a pre-trained machine learning model to suggest similar books.

## Features

- **Home Page**: Displays the most popular books with details such as title, author, rating, and number of votes.
- **Recommendation Page**: Allows users to enter a book name and get a list of similar books based on a pre-trained similarity model.
- **Interactive UI**: Responsive design using Bootstrap for a clean and user-friendly interface.

## Installation

### Prerequisites

- Python 3.7 or higher
- `pip` for installing Python packages

### Step-by-Step Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ShreyasGandhi0607/book-recommendation-system.git
   cd book-recommendation-system
   ```

2. **Create a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Required Packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Download the Model Files**:
   - Ensure the following files are present in the `notebook/` directory:
     - `popular.pkl`
     - `pt.pkl`
     - `books.pkl`
     - `similarity_score.pkl`
   - These files should be generated during the model training process or can be downloaded if provided.

5. **Run the Flask Application**:
   ```bash
   flask run
   ```

6. **Access the Application**:
   - Open your browser and go to `http://127.0.0.1:5000/` to access the home page.

## Project Structure

```plaintext
├── app.py                   # Main Flask application
├── notebook/                # Directory containing model files
│   ├── popular.pkl          # Pre-trained model for popular books
│   ├── pt.pkl               # Pivot table of book ratings
│   ├── books.pkl            # Book metadata
│   ├── similarity_score.pkl # Similarity scores between books
│   ├──recommender_system.ipynb # notebook 
├── templates/               # HTML templates for Flask
│   ├── index.html           # Home page template
│   ├── recommand.html       # Recommendation page template
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

## How It Works

1. **Data Preprocessing**:
   - The data is preprocessed and saved as pickle files (`popular.pkl`, `pt.pkl`, `books.pkl`, `similarity_score.pkl`) for efficient loading and querying.

2. **Recommendation Logic**:
   - Users enter a book name, and the app looks up the most similar books using the pre-trained similarity score matrix.
   - The system then retrieves the details of the recommended books and displays them on the recommendation page.

3. **User Interface**:
   - The application uses Bootstrap for a clean and responsive user interface.
   - Flash messages are implemented to guide users (e.g., if no book name is entered).

## Technologies Used

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS (Bootstrap)
- **Data Storage**: Pickle files for model and data persistence
- **Deployment**: Local server (for development)



## Acknowledgements

- **Dataset**: The book data is sourced from the Book Recommendation Dataset on Kaggle.
- **Inspiration**: This project is inspired by various book recommendation systems available online.
