"""
Test the model against bias scenarios and edge cases.
This script verifies that the model handles extreme inputs reasonably.
"""
import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler


def create_advanced_features(df):
    """Create the same advanced features as in training"""
    df_copy = df.copy()
    
    df_copy['study_sleep_interaction'] = df_copy['Hours Studied'] * df_copy['Sleep Hours']
    df_copy['study_papers_interaction'] = df_copy['Hours Studied'] * df_copy['Sample Question Papers Practiced']
    df_copy['papers_score_interaction'] = df_copy['Sample Question Papers Practiced'] * df_copy['Previous Scores']
    
    df_copy['hours_squared'] = df_copy['Hours Studied'] ** 2
    df_copy['sleep_squared'] = df_copy['Sleep Hours'] ** 2
    df_copy['papers_squared'] = df_copy['Sample Question Papers Practiced'] ** 2
    
    df_copy['study_efficiency'] = np.where(
        df_copy['Sleep Hours'] > 0,
        df_copy['Hours Studied'] / df_copy['Sleep Hours'],
        0
    )
    
    df_copy['sleep_quality'] = np.abs(df_copy['Sleep Hours'] - 8)
    df_copy['score_percentile'] = df_copy['Previous Scores'] / 100.0
    
    df_copy['total_effort'] = (
        (df_copy['Hours Studied'] / 24) +
        (df_copy['Sample Question Papers Practiced'] / 10) +
        df_copy['Extracurricular Activities']
    ) / 3
    
    return df_copy


def test_bias_scenarios():
    """Test model against bias scenarios"""
    try:
        model = joblib.load('performance/model.pkl')
        scaler = joblib.load('performance/scaler.pkl')
        feature_names = joblib.load('performance/features.pkl')
        
        # Test scenarios
        test_cases = [
            # Scenario 1: 0 sleep
            {'Hours Studied': 8, 'Previous Scores': 75, 'Extracurricular Activities': 1, 'Sleep Hours': 0, 'Sample Question Papers Practiced': 5},
            
            # Scenario 2: 24 hours sleep (study + sleep = 24, so study = 0)
            {'Hours Studied': 0, 'Previous Scores': 70, 'Extracurricular Activities': 0, 'Sleep Hours': 24, 'Sample Question Papers Practiced': 2},
            
            # Scenario 3: 0 hours studied
            {'Hours Studied': 0, 'Previous Scores': 60, 'Extracurricular Activities': 1, 'Sleep Hours': 8, 'Sample Question Papers Practiced': 3},
            
            # Scenario 4: 16 hours studied + 8 hours sleep = 24 (realistic extreme)
            {'Hours Studied': 16, 'Previous Scores': 80, 'Extracurricular Activities': 1, 'Sleep Hours': 8, 'Sample Question Papers Practiced': 10},
            
            # Scenario 5: 0 hours studied, 0 sleep
            {'Hours Studied': 0, 'Previous Scores': 40, 'Extracurricular Activities': 0, 'Sleep Hours': 0, 'Sample Question Papers Practiced': 0},
            
            # Scenario 6: Perfect scenario
            {'Hours Studied': 8, 'Previous Scores': 95, 'Extracurricular Activities': 1, 'Sleep Hours': 8, 'Sample Question Papers Practiced': 8},
            
            # Scenario 7: 12 hours studied + 12 hours sleep = 24 (MAXIMUM REALISTIC)
            {'Hours Studied': 12, 'Previous Scores': 90, 'Extracurricular Activities': 1, 'Sleep Hours': 12, 'Sample Question Papers Practiced': 10},
            
            # Scenario 8: Extreme sleep deprivation (20h study + 1h sleep = 21h)
            {'Hours Studied': 20, 'Previous Scores': 70, 'Extracurricular Activities': 0, 'Sleep Hours': 1, 'Sample Question Papers Practiced': 9},
            
            # Scenario 9: Low effort
            {'Hours Studied': 1, 'Previous Scores': 30, 'Extracurricular Activities': 0, 'Sleep Hours': 6, 'Sample Question Papers Practiced': 0},
            
            # Scenario 10: Average case
            {'Hours Studied': 5, 'Previous Scores': 70, 'Extracurricular Activities': 1, 'Sleep Hours': 7, 'Sample Question Papers Practiced': 3},
        ]
        
        df_test = pd.DataFrame(test_cases)
        df_enhanced = create_advanced_features(df_test)
        df_enhanced = df_enhanced[feature_names]
        df_scaled = scaler.transform(df_enhanced)
        
        predictions = model.predict(df_scaled)
        
        print("="*80)
        print("BIAS TEST SCENARIOS - MODEL PREDICTIONS")
        print("="*80)
        
        for i, (case, pred) in enumerate(zip(test_cases, predictions), 1):
            pred_clipped = np.clip(pred, 0, 100)
            print(f"\nScenario {i}:")
            print(f"  Hours Studied: {case['Hours Studied']:2d} | Sleep: {case['Sleep Hours']:2d} | "
                  f"Previous Score: {case['Previous Scores']:3d} | Papers: {case['Sample Question Papers Practiced']:2d} | "
                  f"Extracurricular: {bool(case['Extracurricular Activities'])}")
            print(f"  → Predicted Performance: {pred_clipped:.2f}/100")
        
        print("\n" + "="*80)
        print("SANITY CHECKS:")
        print("="*80)
        
        # Check if extreme cases are handled
        scenario_names = [
            "Zero Sleep",
            "24h Sleep",
            "No Study",
            "24h Study (no sleep)",
            "Complete Zero Effort",
            "Perfect Scenario",
            "Extreme Scenario (24h study + 24h sleep)",
            "Sleep Deprivation",
            "Low Effort",
            "Average Case"
        ]
        
        for name, pred in zip(scenario_names, predictions):
            pred_clipped = np.clip(pred, 0, 100)
            status = "✓ REASONABLE" if 10 <= pred_clipped <= 90 else "⚠ EXTREME"
            print(f"{name:40s}: {pred_clipped:6.2f}/100 {status}")
        
        print("="*80)
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Make sure the model has been trained first!")
    except Exception as e:
        print(f"Error testing bias scenarios: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    test_bias_scenarios()
