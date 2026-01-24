"""
Serializers for the performance API.
"""
from rest_framework import serializers
from .models import StudentPerformance


class StudentPerformanceSerializer(serializers.ModelSerializer):
    """
    Serializer for StudentPerformance model.
    Converts model instances to/from JSON.
    """
    class Meta:
        model = StudentPerformance
        fields = [
            'id',
            'hours_studied',
            'previous_scores',
            'extracurricular',
            'sleep_hours',
            'sample_papers',
            'performance_index',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class PredictionSerializer(serializers.Serializer):
    """
    Serializer for prediction API requests.
    Validates input features for ML prediction.
    """
    hours_studied = serializers.IntegerField(min_value=0, max_value=24)
    previous_scores = serializers.IntegerField(min_value=0, max_value=100)
    extracurricular = serializers.BooleanField()
    sleep_hours = serializers.IntegerField(min_value=0, max_value=24)
    sample_papers = serializers.IntegerField(min_value=0, max_value=50)

    def validate(self, data):
        """
        Validate that all required fields are present.
        """
        required_fields = [
            'hours_studied',
            'previous_scores',
            'extracurricular',
            'sleep_hours',
            'sample_papers'
        ]
        
        for field in required_fields:
            if field not in data:
                raise serializers.ValidationError(f"{field} is required.")
        
        return data
