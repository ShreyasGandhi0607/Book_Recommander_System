import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

def transform_data(data):
    """
    Performs data transformation on the book data.

    Parameters:
    data (pd.DataFrame): DataFrame containing the book data.

    Returns:
    pd.DataFrame: Transformed DataFrame ready for recommendation system.
    """
    # Drop any rows with missing values
    data.dropna(inplace=True)

    # Encode categorical variables
    label_encoder = LabelEncoder()
    data['Genre'] = label_encoder.fit_transform(data['Genre'])
    data['SubGenre'] = label_encoder.fit_transform(data['SubGenre'])
    data['Category'] = label_encoder.fit_transform(data['Category'])

    # Standardize numerical features
    scaler = StandardScaler()
    numerical_features = ['Height']  # Add more numerical features as needed
    data[numerical_features] = scaler.fit_transform(data[numerical_features])

    return data

# Example usage:
if __name__ == "__main__":
    # Load the data into a DataFrame
    data = pd.read_csv('your_data.csv')  # Replace 'your_data.csv' with your actual data file path

    # Perform data transformation
    transformed_data = transform_data(data)

    # Display the transformed data
    print(transformed_data.head())
