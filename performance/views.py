"""
API Views for the performance prediction endpoints.
"""
import joblib
import numpy as np
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import StudentPerformanceSerializer, PredictionSerializer
from .models import StudentPerformance


# Load the pre-trained model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')

try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    model = None


@api_view(['POST'])
def predict_performance(request):
    """
    Predict student performance based on input features.
    
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
    
    # Validate input data
    serializer = PredictionSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    data = serializer.validated_data
    
    # Prepare features in the correct order
    # Order: hours_studied, previous_scores, extracurricular, sleep_hours, sample_papers
    features = np.array([[
        data['hours_studied'],
        data['previous_scores'],
        1 if data['extracurricular'] else 0,  # Convert boolean to int
        data['sleep_hours'],
        data['sample_papers'],
    ]])
    
    # Make prediction
    try:
        prediction = model.predict(features)[0]
        
        return Response({
            'predicted_performance_index': round(float(prediction), 2),
            'input_features': {
                'hours_studied': data['hours_studied'],
                'previous_scores': data['previous_scores'],
                'extracurricular': data['extracurricular'],
                'sleep_hours': data['sleep_hours'],
                'sample_papers': data['sample_papers'],
            }
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
