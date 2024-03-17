# Book Recommender System

This is a book recommender system built using Flask and integrated with the Google Books API to provide book recommendations based on a provided book title.

## Features

- **Recommendation Generation:** Given a book title, the system recommends similar books based on a trained recommendation model.
- **Integration with Google Books API:** Fetches book information including author names and cover images from the Google Books API.
- **User-Friendly Interface:** Provides a simple web interface for users to input book titles and view recommended books.

## Screenshots

### Home Page
<img width="1440" alt="Screenshot 2024-03-17 at 9 03 18 PM" src="https://github.com/ShreyasGandhi0607/Book_Recommander_System/assets/100945644/ea75e87c-4635-4b1b-a697-86cea9eefdbc">


### Recommandation Page
<img width="1440" alt="book_recommandations_ui" src="https://github.com/ShreyasGandhi0607/Book_Recommander_System/assets/100945644/b892123a-8dea-4f8d-8dff-9d373d08cf28">


## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/ShreyasGandhi0607/Book_Recommander_System.git
    ```

2. Navigate to the project directory:

    ```bash
    cd book-recommender-system
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Start the Flask application:

    ```bash
    python app.py
    ```

2. Open your web browser and navigate to `http://localhost:5001` to access the web interface.

3. Enter a book title in the provided input field and click on "Recommend Books" to view recommended books.

## Project Structure

- `app.py`: Flask application script containing routes and main logic.
- `src/`: Directory containing project source code.
  - `components/`: Directory containing components such as the model trainer.
  - `utils/`: Directory containing utility functions.
  - `logger.py`: Logger configuration script.
- `notebook/`: Directory containing notebooks for data exploration and model training.
- `templates/`: Directory containing HTML templates for the web interface.
- `artifacts/`: Directory containing trained model and data transformation artifacts.


## License

This project is licensed under the [MIT License](LICENSE).
