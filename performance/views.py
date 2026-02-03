"""
API Views for the performance prediction endpoints.
Includes bias-resistant predictions using advanced feature engineering.
"""
import joblib
import numpy as np
import pandas as pd
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import StudentPerformanceSerializer, PredictionSerializer
from .models import StudentPerformance


# Load the pre-trained model, scaler, and features
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')
SCALER_PATH = os.path.join(os.path.dirname(__file__), 'scaler.pkl')
FEATURES_PATH = os.path.join(os.path.dirname(__file__), 'features.pkl')

try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    model = None

try:
    scaler = joblib.load(SCALER_PATH)
except FileNotFoundError:
    scaler = None

try:
    feature_names = joblib.load(FEATURES_PATH)
except FileNotFoundError:
    feature_names = None


def create_advanced_features_for_prediction(hours_studied, previous_scores, 
                                           extracurricular, sleep_hours, sample_papers):
    """
    Create the same advanced features used during training
    to ensure consistent predictions without bias.
    """
    features_dict = {
        'Hours Studied': hours_studied,
        'Previous Scores': previous_scores,
        'Extracurricular Activities': 1 if extracurricular else 0,
        'Sleep Hours': sleep_hours,
        'Sample Question Papers Practiced': sample_papers,
    }
    
    # Base features
    base_df = pd.DataFrame([features_dict])
    
    # Create advanced features (same as training)
    base_df_copy = base_df.copy()
    
    base_df['study_sleep_interaction'] = base_df['Hours Studied'] * base_df['Sleep Hours']
    base_df['study_papers_interaction'] = base_df['Hours Studied'] * base_df['Sample Question Papers Practiced']
    base_df['papers_score_interaction'] = base_df['Sample Question Papers Practiced'] * base_df['Previous Scores']
    
    base_df['hours_squared'] = base_df['Hours Studied'] ** 2
    base_df['sleep_squared'] = base_df['Sleep Hours'] ** 2
    base_df['papers_squared'] = base_df['Sample Question Papers Practiced'] ** 2
    
    base_df['study_efficiency'] = np.where(
        base_df['Sleep Hours'] > 0,
        base_df['Hours Studied'] / base_df['Sleep Hours'],
        0
    )
    
    base_df['sleep_quality'] = np.abs(base_df['Sleep Hours'] - 8)
    
    base_df['score_percentile'] = base_df['Previous Scores'] / 100.0
    
    base_df['total_effort'] = (
        (base_df['Hours Studied'] / 24) +
        (base_df['Sample Question Papers Practiced'] / 10) +
        base_df['Extracurricular Activities']
    ) / 3
    
    return base_df


@api_view(['POST'])
def predict_performance(request):
    """
    Predict student performance with bias-resistant model.
    Uses advanced feature engineering to handle extreme cases.
    
    Expected POST data:
    {
        "hours_studied": int,
        "previous_scores": int,
        "extracurricular": boolean,
        "sleep_hours": int,
        "sample_papers": int
    }
    
    Returns:
    {
        "predicted_performance_index": float
    }
    """
    if model is None:
        return Response(
            {'error': 'Model not found. Please train the model first.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    if scaler is None:
        return Response(
            {'error': 'Scaler not found. Please train the model first.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    if feature_names is None:
        return Response(
            {'error': 'Features configuration not found. Please train the model first.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # Validate input data
    serializer = PredictionSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    data = serializer.validated_data
    
    # VALIDATION: study_hours + sleep_hours must be ≤ 24
    if data['hours_studied'] + data['sleep_hours'] > 24:
        return Response(
            {'error': f'Invalid input: Hours Studied ({data["hours_studied"]}) + Sleep Hours ({data["sleep_hours"]}) = {data["hours_studied"] + data["sleep_hours"]}, which exceeds 24 hours in a day. Please reduce one of these values.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Create advanced features
        features_df = create_advanced_features_for_prediction(
            data['hours_studied'],
            data['previous_scores'],
            data['extracurricular'],
            data['sleep_hours'],
            data['sample_papers']
        )
        
        # Reorder columns to match training features
        features_df = features_df[feature_names]
        
        # Scale features using the same scaler as training
        features_scaled = scaler.transform(features_df)
        
        # Make prediction
        prediction = model.predict(features_scaled)[0]
        
        # Clip prediction to realistic range (0-100)
        prediction = np.clip(prediction, 0, 100)
        
        return Response({
            'predicted_performance_index': round(float(prediction), 2),
            'input_features': {
                'hours_studied': data['hours_studied'],
                'previous_scores': data['previous_scores'],
                'extracurricular': data['extracurricular'],
                'sleep_hours': data['sleep_hours'],
                'sample_papers': data['sample_papers'],
            },
            'model_info': 'Bias-resistant prediction using advanced feature engineering'
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response(
            {'error': f'Prediction error: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_all_records(request):
    """
    Retrieve all student performance records from the database.
    Supports pagination.
    """
    records = StudentPerformance.objects.all()
    serializer = StudentPerformanceSerializer(records, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_record_by_id(request, pk):
    """
    Retrieve a specific student performance record by ID.
    """
    try:
        record = StudentPerformance.objects.get(pk=pk)
        serializer = StudentPerformanceSerializer(record)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except StudentPerformance.DoesNotExist:
        return Response(
            {'error': 'Record not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
def create_record(request):
    """
    Create a new student performance record.
    """
    serializer = StudentPerformanceSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_statistics(request):
    """
    Get statistics about the student performance data.
    """
    records = StudentPerformance.objects.all()
    
    if not records.exists():
        return Response(
            {'error': 'No records found in database'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    performance_indices = [r.performance_index for r in records]
    
    stats = {
        'total_records': records.count(),
        'average_performance': round(sum(performance_indices) / len(performance_indices), 2),
        'max_performance': round(max(performance_indices), 2),
        'min_performance': round(min(performance_indices), 2),
        'average_hours_studied': round(sum([r.hours_studied for r in records]) / len(records), 2),
        'average_sleep_hours': round(sum([r.sleep_hours for r in records]) / len(records), 2),
    }
    
    return Response(stats, status=status.HTTP_200_OK)
