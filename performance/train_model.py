"""
Train and save the machine learning model.
Run this script to train the RandomForestRegressor on the dataset.
"""
import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score


def train():
    """
    Train the ML model and save it as model.pkl
    """
    try:
        # Read the dataset
        df = pd.read_csv('dataset.csv')
        
        # Encode categorical variable (Extracurricular Activities)
        df['Extracurricular Activities'] = LabelEncoder().fit_transform(
            df['Extracurricular Activities']
        )
        
        # Prepare features and target
        X = df.drop('Performance Index', axis=1)
        y = df['Performance Index']
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train the model
        model = RandomForestRegressor(
            n_estimators=200,
            max_depth=20,
            random_state=42,
            n_jobs=-1
        )
        model.fit(X_train, y_train)
        
        # Evaluate the model
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        print(f"Model Performance:")
        print(f"Mean Squared Error: {mse:.4f}")
        print(f"R² Score: {r2:.4f}")
        
        # Create model directory if it doesn't exist
        model_dir = 'performance'
        os.makedirs(model_dir, exist_ok=True)
        
        # Save the model
        model_path = os.path.join(model_dir, 'model.pkl')
        joblib.dump(model, model_path)
        
        print(f"Model trained and saved successfully at: {model_path}")
        
    except FileNotFoundError:
        print("Error: dataset.csv not found. Make sure it's in the project root directory.")
    except Exception as e:
        print(f"Error training model: {str(e)}")


if __name__ == '__main__':
    train()
