"""
Tests for the performance prediction API
"""
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import StudentPerformance
import json


class PredictionAPITestCase(TestCase):
    """Test cases for the prediction API endpoint"""
    
    def setUp(self):
        """Set up test client and sample data"""
        self.client = APIClient()
        
        # Create sample record
        StudentPerformance.objects.create(
            hours_studied=6,
            previous_scores=78,
            extracurricular=True,
            sleep_hours=7,
            sample_papers=3,
            performance_index=72.45
        )
    
    def test_prediction_valid_input(self):
        """Test prediction with valid input"""
        data = {
            "hours_studied": 6,
            "previous_scores": 78,
            "extracurricular": True,
            "sleep_hours": 7,
            "sample_papers": 3
        }
        response = self.client.post('/api/predict/', data, format='json')
        
        # Should return 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Should have prediction key
        self.assertIn('predicted_performance_index', response.data)
    
    def test_prediction_missing_field(self):
        """Test prediction with missing required field"""
        data = {
            "hours_studied": 6,
            "previous_scores": 78,
            "extracurricular": True,
            "sleep_hours": 7,
            # Missing sample_papers
        }
        response = self.client.post('/api/predict/', data, format='json')
        
        # Should return 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_prediction_invalid_type(self):
        """Test prediction with invalid data type"""
        data = {
            "hours_studied": "six",  # Should be integer
            "previous_scores": 78,
            "extracurricular": True,
            "sleep_hours": 7,
            "sample_papers": 3
        }
        response = self.client.post('/api/predict/', data, format='json')
        
        # Should return 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class StudentPerformanceModelTestCase(TestCase):
    """Test cases for StudentPerformance model"""
    
    def setUp(self):
        """Set up test data"""
        self.record = StudentPerformance.objects.create(
            hours_studied=7,
            previous_scores=85,
            extracurricular=True,
            sleep_hours=8,
            sample_papers=4,
            performance_index=79.8
        )
    
    def test_create_record(self):
        """Test creating a student performance record"""
        self.assertEqual(self.record.hours_studied, 7)
        self.assertEqual(self.record.performance_index, 79.8)
        self.assertTrue(self.record.extracurricular)
    
    def test_record_string_representation(self):
        """Test string representation of record"""
        expected_str = "Performance Index: 79.8"
        self.assertEqual(str(self.record), expected_str)


class RecordsAPITestCase(TestCase):
    """Test cases for records endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        
        # Create sample records
        for i in range(3):
            StudentPerformance.objects.create(
                hours_studied=5 + i,
                previous_scores=70 + (i * 5),
                extracurricular=bool(i % 2),
                sleep_hours=6 + i,
                sample_papers=2 + i,
                performance_index=65.0 + (i * 5)
            )
    
    def test_get_all_records(self):
        """Test retrieving all records"""
        response = self.client.get('/api/records/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
    
    def test_get_record_by_id(self):
        """Test retrieving specific record"""
        record = StudentPerformance.objects.first()
        response = self.client.get(f'/api/records/{record.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], record.id)
    
    def test_get_nonexistent_record(self):
        """Test retrieving non-existent record"""
        response = self.client.get('/api/records/9999/')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class StatisticsAPITestCase(TestCase):
    """Test cases for statistics endpoint"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        
        # Create sample records
        StudentPerformance.objects.create(
            hours_studied=5, previous_scores=70, extracurricular=True,
            sleep_hours=6, sample_papers=2, performance_index=65.0
        )
        StudentPerformance.objects.create(
            hours_studied=8, previous_scores=90, extracurricular=False,
            sleep_hours=8, sample_papers=4, performance_index=85.0
        )
    
    def test_get_statistics(self):
        """Test retrieving statistics"""
        response = self.client.get('/api/statistics/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_records', response.data)
        self.assertIn('average_performance', response.data)
        self.assertIn('max_performance', response.data)
        self.assertIn('min_performance', response.data)
