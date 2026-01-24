"""
URL configuration for the performance app.
"""
from django.urls import path
from .views import (
    predict_performance,
    get_all_records,
    get_record_by_id,
    create_record,
    get_statistics
)

app_name = 'performance'

urlpatterns = [
    # Prediction endpoints
    path('predict/', predict_performance, name='predict_performance'),
    
    # Database CRUD endpoints
    path('records/', get_all_records, name='get_all_records'),
    path('records/create/', create_record, name='create_record'),
    path('records/<int:pk>/', get_record_by_id, name='get_record_by_id'),
    
    # Statistics endpoint
    path('statistics/', get_statistics, name='get_statistics'),
]
