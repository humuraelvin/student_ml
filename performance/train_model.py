"""
Train and save the machine learning model with bias reduction.
Handles extreme cases without validation to improve robustness.
"""
import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder, StandardScaler, PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler


def generate_bias_resistant_data(df):
    """
    Generate synthetic data to handle edge cases and extreme scenarios.
    This ensures the model learns to handle:
    - 0 hours sleep / 24 hours sleep
    - 0 hours studied / 24 hours studied
    - 0 papers / max papers
    - Low scores / high scores combinations
    - All extracurricular combinations
    """
    base_data = df.copy()
    synthetic_samples = []
    
    # Edge case 1: Student with 0 sleep (worst case)
    for hours in [0, 1, 2]:
        for studied in range(0, 25, 6):
            for papers in range(0, 11, 3):
                for extra in ['Yes', 'No']:
                    for prev_score in [20, 40, 60, 80]:
                        # Severely penalize lack of sleep
                        performance = max(10, (studied * 2.5) + (prev_score * 0.4) + (papers * 1.5) + (2 if extra == 'Yes' else 0) - (24 - hours) * 3)
                        synthetic_samples.append({
                            'Hours Studied': studied,
                            'Previous Scores': prev_score,
                            'Extracurricular Activities': extra,
                            'Sleep Hours': hours,
                            'Sample Question Papers Practiced': papers,
                            'Performance Index': performance
                        })
    
    # Edge case 2: Student with 24 hours sleep (oversleeping)
    for hours in [23, 24]:
        for studied in range(0, 25, 6):
            for papers in range(0, 11, 3):
                for extra in ['Yes', 'No']:
                    for prev_score in [20, 40, 60, 80]:
                        # Penalize oversleeping too
                        base_perf = (studied * 3) + (prev_score * 0.5) + (papers * 2) + (3 if extra == 'Yes' else 0)
                        oversleep_penalty = max(0, (hours - 9) * 1.5)
                        performance = max(15, base_perf - oversleep_penalty)
                        synthetic_samples.append({
                            'Hours Studied': studied,
                            'Previous Scores': prev_score,
                            'Extracurricular Activities': extra,
                            'Sleep Hours': hours,
                            'Sample Question Papers Practiced': papers,
                            'Performance Index': performance
                        })
    
    # Edge case 3: 0 hours studied
    for sleep in range(0, 25, 3):
        for papers in range(0, 11, 3):
            for extra in ['Yes', 'No']:
                for prev_score in [30, 50, 70]:
                    # Very low performance with no studying
                    performance = (prev_score * 0.3) + (papers * 0.5) + (1 if extra == 'Yes' else 0) + max(0, (sleep - 8) * 0.5)
                    synthetic_samples.append({
                        'Hours Studied': 0,
                        'Previous Scores': prev_score,
                        'Extracurricular Activities': extra,
                        'Sleep Hours': sleep,
                        'Sample Question Papers Practiced': papers,
                        'Performance Index': performance
                    })
    
    # Edge case 4: High study hours with realistic sleep (study + sleep ≤ 24)
    for sleep in range(0, 10, 2):
        max_study = max(0, 24 - sleep)  # Can't study + sleep more than 24 hours
        for studied in [max(0, max_study - 2), max_study]:
            for papers in range(0, 11, 2):
                for extra in ['Yes', 'No']:
                    for prev_score in [30, 60, 90]:
                        # Extreme studying with minimal sleep is counterproductive
                        exhaustion_penalty = max(0, (24 - sleep) * 2)
                        performance = min(100, (prev_score * 0.6) + (papers * 3) + (2 if extra == 'Yes' else 0) + 20 - exhaustion_penalty)
                        synthetic_samples.append({
                            'Hours Studied': studied,
                            'Previous Scores': prev_score,
                            'Extracurricular Activities': extra,
                            'Sleep Hours': sleep,
                            'Sample Question Papers Practiced': papers,
                            'Performance Index': performance
                        })
    
    # Edge case 5: Realistic combinations (study + sleep ≤ 24)
    for hours in range(1, 25):
        for sleep in range(5, 10):
            if hours + sleep <= 24:  # Enforce: study + sleep ≤ 24 hours
                for papers in range(1, 11):
                    for prev_score in [50, 75, 95]:
                        for extra in ['Yes', 'No']:
                            # Realistic progression model
                            base = (hours * 2.5) + (prev_score * 0.6) + (papers * 1.5) + (3 if extra == 'Yes' else 0)
                            sleep_effect = 0 if 7 <= sleep <= 9 else abs(sleep - 8) * 1.5
                            performance = np.clip(base - sleep_effect, 10, 100)
                            synthetic_samples.append({
                                'Hours Studied': hours,
                                'Previous Scores': prev_score,
                                'Extracurricular Activities': extra,
                                'Sleep Hours': sleep,
                                'Sample Question Papers Practiced': papers,
                                'Performance Index': performance
                            })
    
    # Edge case 6: Diminishing returns at extremes (study + sleep ≤ 24)
    for hours in range(12, 25):
        for sleep in range(6, 10):
            if hours + sleep <= 24:  # Enforce: study + sleep ≤ 24 hours
                for papers in range(5, 11):
                    for prev_score in [40, 70, 95]:
                        for extra in ['Yes', 'No']:
                            # More hours doesn't always mean better performance
                            base = (hours * 2) + (prev_score * 0.7) + (papers * 2) + (3 if extra == 'Yes' else 0)
                            diminishing_return = max(0, (hours - 12) * 0.3)
                            performance = np.clip(base - diminishing_return, 20, 100)
                            synthetic_samples.append({
                                'Hours Studied': hours,
                                'Previous Scores': prev_score,
                                'Extracurricular Activities': extra,
                                'Sleep Hours': sleep,
                                'Sample Question Papers Practiced': papers,
                                'Performance Index': performance
                            })
    
    synthetic_df = pd.DataFrame(synthetic_samples)
    combined_df = pd.concat([base_data, synthetic_df], ignore_index=True)
    return combined_df


def create_advanced_features(X):
    """
    Create advanced features to capture non-linear relationships
    and interactions that reduce bias.
    """
    X_enhanced = X.copy()
    
    # Interaction features
    X_enhanced['study_sleep_interaction'] = X_enhanced['Hours Studied'] * X_enhanced['Sleep Hours']
    X_enhanced['study_papers_interaction'] = X_enhanced['Hours Studied'] * X_enhanced['Sample Question Papers Practiced']
    X_enhanced['papers_score_interaction'] = X_enhanced['Sample Question Papers Practiced'] * X_enhanced['Previous Scores']
    
    # Non-linear features
    X_enhanced['hours_squared'] = X_enhanced['Hours Studied'] ** 2
    X_enhanced['sleep_squared'] = X_enhanced['Sleep Hours'] ** 2
    X_enhanced['papers_squared'] = X_enhanced['Sample Question Papers Practiced'] ** 2
    
    # Efficiency metrics
    X_enhanced['study_efficiency'] = np.where(
        X_enhanced['Sleep Hours'] > 0,
        X_enhanced['Hours Studied'] / X_enhanced['Sleep Hours'],
        0
    )
    
    # Sleep quality indicator (optimal range is 7-9 hours)
    X_enhanced['sleep_quality'] = np.abs(X_enhanced['Sleep Hours'] - 8)
    
    # Normalized previous scores
    X_enhanced['score_percentile'] = X_enhanced['Previous Scores'] / 100.0
    
    # Combined effort metric
    X_enhanced['total_effort'] = (
        (X_enhanced['Hours Studied'] / 24) +
        (X_enhanced['Sample Question Papers Practiced'] / 10) +
        X_enhanced['Extracurricular Activities']
    ) / 3
    
    return X_enhanced


def train():
    """
    Train multiple models with bias reduction techniques
    """
    try:
        # Read the dataset
        df = pd.read_csv('dataset.csv')
        
        print("Original dataset shape:", df.shape)
        print("Dataset columns:", df.columns.tolist())
        
        # Generate bias-resistant data with synthetic edge cases
        df = generate_bias_resistant_data(df)
        print(f"Enhanced dataset shape with synthetic data: {df.shape}")
        
        # Encode categorical variable
        le = LabelEncoder()
        df['Extracurricular Activities'] = le.fit_transform(df['Extracurricular Activities'])
        
        # Prepare features and target
        X = df.drop('Performance Index', axis=1)
        y = df['Performance Index']
        
        # Create advanced features
        X = create_advanced_features(X)
        
        print(f"Features after enhancement: {X.shape[1]} features")
        print(f"Feature names: {X.columns.tolist()}")
        
        # Standardize features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        X_scaled = pd.DataFrame(X_scaled, columns=X.columns)
        
        # Split with stratified approach for better distribution
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.15, random_state=42
        )
        
        print(f"Training set size: {X_train.shape[0]}, Test set size: {X_test.shape[0]}")
        
        # Train Gradient Boosting Model (less prone to bias than Random Forest)
        model = GradientBoostingRegressor(
            n_estimators=500,
            learning_rate=0.05,
            max_depth=7,
            min_samples_split=5,
            min_samples_leaf=2,
            subsample=0.8,
            random_state=42,
            loss='huber',  # Robust to outliers
            alpha=0.9
        )
        
        print("Training Gradient Boosting model...")
        model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)
        
        train_mse = mean_squared_error(y_train, y_pred_train)
        test_mse = mean_squared_error(y_test, y_pred_test)
        train_r2 = r2_score(y_train, y_pred_train)
        test_r2 = r2_score(y_test, y_pred_test)
        train_mae = mean_absolute_error(y_train, y_pred_train)
        test_mae = mean_absolute_error(y_test, y_pred_test)
        
        # Cross-validation score
        cv_scores = cross_val_score(model, X_scaled, y, cv=5, scoring='r2')
        
        print("\n" + "="*60)
        print("MODEL PERFORMANCE METRICS")
        print("="*60)
        print(f"Train MSE: {train_mse:.4f}")
        print(f"Test MSE: {test_mse:.4f}")
        print(f"Train R² Score: {train_r2:.4f}")
        print(f"Test R² Score: {test_r2:.4f}")
        print(f"Train MAE: {train_mae:.4f}")
        print(f"Test MAE: {test_mae:.4f}")
        print(f"Cross-validation R² (mean): {cv_scores.mean():.4f}")
        print(f"Cross-validation R² (std): {cv_scores.std():.4f}")
        print("="*60)
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': X.columns,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\nTop 10 Feature Importances:")
        print(feature_importance.head(10).to_string())
        
        # Save model
        model_dir = 'performance'
        os.makedirs(model_dir, exist_ok=True)
        
        model_path = os.path.join(model_dir, 'model.pkl')
        joblib.dump(model, model_path)
        
        # Save scaler
        scaler_path = os.path.join(model_dir, 'scaler.pkl')
        joblib.dump(scaler, scaler_path)
        
        # Save feature names
        features_path = os.path.join(model_dir, 'features.pkl')
        joblib.dump(X.columns.tolist(), features_path)
        
        print(f"\nModel saved at: {model_path}")
        print(f"Scaler saved at: {scaler_path}")
        print(f"Features saved at: {features_path}")
        
    except FileNotFoundError:
        print("Error: dataset.csv not found. Make sure it's in the project root directory.")
    except Exception as e:
        print(f"Error training model: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    train()

