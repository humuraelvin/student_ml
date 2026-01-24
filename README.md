# Django ML Prediction API – Student Performance

A comprehensive Django REST API for predicting student performance using machine learning.

## Project Structure

```
student_ml/
├── student_ml/              # Django project settings
│   ├── __init__.py
│   ├── settings.py         # Project settings
│   ├── urls.py             # Main URL configuration
│   └── wsgi.py             # WSGI application
├── performance/            # Django app for ML predictions
│   ├── migrations/         # Database migrations
│   ├── __init__.py
│   ├── admin.py           # Django admin configuration
│   ├── apps.py            # App configuration
│   ├── models.py          # Database models
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # API views
│   ├── urls.py            # App URL routing
│   ├── load_data.py       # Script to load dataset
│   ├── train_model.py     # Script to train ML model
│   └── model.pkl          # Trained ML model (generated)
├── manage.py              # Django management script
├── dataset.csv            # Training dataset
└── requirements.txt       # Python dependencies
```

## Installation & Setup Commands

### 1. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Create Initial Migrations
```bash
cd student_ml
python manage.py makemigrations
python manage.py migrate
```

### 4. Load Dataset into Database
```bash
python manage.py shell
>>> from performance.load_data import run
>>> run()
>>> exit()
```

### 5. Train Machine Learning Model
```bash
python manage.py shell
>>> from performance.train_model import train
>>> train()
>>> exit()
```

### 6. Run Development Server
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

## API Endpoints

### 1. Predict Performance (Main Endpoint)
**POST** `/api/predict/`

Request body:
```json
{
    "hours_studied": 6,
    "previous_scores": 78,
    "extracurricular": true,
    "sleep_hours": 7,
    "sample_papers": 3
}
```

Response:
```json
{
    "predicted_performance_index": 72.45,
    "input_features": {
        "hours_studied": 6,
        "previous_scores": 78,
        "extracurricular": true,
        "sleep_hours": 7,
        "sample_papers": 3
    }
}
```

### 2. Get All Records
**GET** `/api/records/`

Response: List of all student performance records in database

### 3. Get Record by ID
**GET** `/api/records/{id}/`

Response: Single student performance record

### 4. Create New Record
**POST** `/api/records/create/`

Request body:
```json
{
    "hours_studied": 7,
    "previous_scores": 85,
    "extracurricular": true,
    "sleep_hours": 8,
    "sample_papers": 4,
    "performance_index": 79.5
}
```

### 5. Get Statistics
**GET** `/api/statistics/`

Response:
```json
{
    "total_records": 30,
    "average_performance": 77.23,
    "max_performance": 92.1,
    "min_performance": 62.7,
    "average_hours_studied": 6.1,
    "average_sleep_hours": 7.3
}
```

## Database Model

### StudentPerformance Model

Fields:
- `hours_studied` (Integer): Hours spent studying
- `previous_scores` (Integer): Previous exam scores (0-100)
- `extracurricular` (Boolean): Participation in extracurricular activities
- `sleep_hours` (Integer): Average sleep hours per night
- `sample_papers` (Integer): Number of sample papers practiced
- `performance_index` (Float): Target performance score
- `created_at` (DateTime): Record creation timestamp
- `updated_at` (DateTime): Last update timestamp

## Machine Learning Model

**Model Type**: RandomForestRegressor
**Features**: 5 input features (as listed above)
**Target**: Performance Index (Regression)
**Model Performance**: 
- Trained on 80% of data (24 samples)
- Tested on 20% of data (6 samples)
- Model file: `performance/model.pkl`

## Technologies & Libraries

### Core Technologies
- **Django**: Web framework
- **Django REST Framework**: REST API toolkit
- **SQLite**: Default database

### ML & Data Processing
- **scikit-learn**: Machine learning library
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **joblib**: Model serialization

## Admin Interface

Access Django admin at `/admin/`
- Username: admin
- Password: (set during superuser creation)

Create superuser:
```bash
python manage.py createsuperuser
```

## Deployment Notes

### Production Considerations

1. **Database Migration**: Switch from SQLite to PostgreSQL
   ```python
   # Update settings.py
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'student_ml_db',
           'USER': 'your_user',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

2. **Model Storage**: Store `model.pkl` outside repository or in secure location
   
3. **Security**:
   - Change `SECRET_KEY` in settings.py
   - Set `DEBUG = False`
   - Set `ALLOWED_HOSTS` appropriately
   - Use environment variables for sensitive data

4. **WSGI Server**: Use Gunicorn or uWSGI instead of Django development server

## Questions & Answers

### a. What is the purpose of joblib?

**Joblib** is a Python library that provides utilities for serialization and parallel computing. Its main purposes are:

1. **Model Serialization**: Save and load machine learning models efficiently
2. **Parallel Computing**: Parallelize loops and function calls
3. **Memory-Mapping**: Reduce memory overhead for large arrays
4. **Caching**: Cache function outputs for efficiency

In this project, joblib is used to:
- Save the trained RandomForestRegressor model as `model.pkl`
- Load the model for making predictions in the API

Example usage:
```python
import joblib

# Save model
joblib.dump(model, 'model.pkl')

# Load model
model = joblib.load('model.pkl')
```

### b. Other libraries that can achieve the same as joblib

Alternative libraries for model serialization and ML operations:

1. **pickle** (Python built-in)
   - Simple object serialization
   - Less efficient for large arrays
   - No compression support

2. **dill**
   - Extended pickle with more object support
   - Can serialize more complex Python objects

3. **cloudpickle**
   - Enhanced pickle for distributed computing
   - Better support for lambda functions and closures

4. **onnx** (Open Neural Network Exchange)
   - Framework-agnostic model format
   - Better interoperability across platforms
   - Optimized for inference

5. **h5py / HDF5**
   - Hierarchical data format
   - Good for large datasets
   - Platform-independent

6. **protobuf** (Protocol Buffers)
   - Language-independent data serialization
   - Compact and efficient
   - Used by TensorFlow

7. **MLflow**
   - Full ML lifecycle management
   - Model tracking and versioning
   - Cross-framework support

### Comparison Table

| Library | Use Case | Size | Speed | Cross-Platform |
|---------|----------|------|-------|-----------------|
| joblib | ML models | Medium | Fast | Yes |
| pickle | General objects | Medium | Medium | Limited |
| onnx | Neural networks | Small | Very Fast | Yes |
| h5py | Large datasets | Large | Medium | Yes |
| cloudpickle | Distributed computing | Medium | Medium | Yes |
| MLflow | Full ML lifecycle | Varies | Medium | Yes |

**Joblib remains the preferred choice for scikit-learn models due to its efficiency and direct integration.**

## API Testing with cURL

```bash
# Predict performance
curl -X POST http://127.0.0.1:8000/api/predict/ \
  -H "Content-Type: application/json" \
  -d '{
    "hours_studied": 6,
    "previous_scores": 78,
    "extracurricular": true,
    "sleep_hours": 7,
    "sample_papers": 3
  }'

# Get all records
curl http://127.0.0.1:8000/api/records/

# Get statistics
curl http://127.0.0.1:8000/api/statistics/
```

## License

This project is for educational purposes.

## Support

For issues or questions, please refer to the Django and Django REST Framework documentation.
