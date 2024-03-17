import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OrdinalEncoder  # Import OrdinalEncoder for encoding non-numeric data
from sklearn.metrics.pairwise import cosine_similarity
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import transform_data
from src.utils import save_object
from src.logger import logging
from src.exception import CustomException

def train_recommendation_model(data_path):
    try:
        # Step 1: Data Ingestion
        logging.info("Starting data ingestion...")
        data_ingestion = DataIngestion()
        train_data_path, _ = data_ingestion.initiate_data_ingestion(data_path)
        logging.info("Data ingestion completed.")

        # Step 2: Data Transformation
        logging.info("Starting data transformation...")
        train_data = pd.read_csv(train_data_path)
        transformed_data = transform_data(train_data)
        logging.info("Data transformation completed.")

        # Step 3: Encode non-numeric data
        logging.info("Encoding non-numeric data...")
        encoder = OrdinalEncoder()
        transformed_data_encoded = encoder.fit_transform(transformed_data)
        logging.info("Non-numeric data encoding completed.")

        # Step 4: Calculate similarity matrix
        logging.info("Calculating similarity matrix...")
        imputer = SimpleImputer(strategy='mean')
        new_book_imputed = imputer.fit_transform(transformed_data_encoded)
        similarity_matrix = cosine_similarity(new_book_imputed)
        logging.info("Similarity matrix calculation completed.")

        # Step 5: Save the similarity matrix
        logging.info("Saving the similarity matrix...")
        save_object('artifacts/similarity_matrix.pkl', similarity_matrix)
        logging.info("Similarity matrix saved.")

        # Step 6: Save the transformed data (optional)
        logging.info("Saving the transformed data...")
        save_object('artifacts/transformed_data.pkl', transformed_data)
        logging.info("Transformed data saved.")

        # Remaining steps (optional)...

        return transformed_data, similarity_matrix

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None, None  # Return None for both outputs in case of an error

# Example usage
if __name__ == "__main__":
    transformed_data, similarity_matrix = train_recommendation_model('notebook/data/final_books.csv')
    if transformed_data is None or similarity_matrix is None:
        logging.error("Model training failed.")
    else:
        logging.info("Model training successful.")

