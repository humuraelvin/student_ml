# Django ML Prediction API - COMMANDS TO RUN

## Complete Setup Instructions

Follow these exact commands in order:

### Step 1: Navigate to Project
```bash
cd "/home/humura/Documents/workings/Year 3/ML/AI_model/student_ml"
```

### Step 2: Create Virtual Environment
```bash
python3 -m venv venv
```

### Step 3: Activate Virtual Environment
```bash
source venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Create Migrations
```bash
python manage.py makemigrations
```

### Step 6: Apply Migrations
```bash
python manage.py migrate
```

### Step 7: Load Dataset
```bash
python manage.py shell
```

Then in the Python shell, type:
```python
from performance.load_data import run
run()
exit()
```

### Step 8: Train Model
```bash
python manage.py shell
```

Then in the Python shell, type:
```python
from performance.train_model import train
train()
exit()
```

### Step 9: Create Superuser (Optional - For Admin Access)
```bash
python manage.py createsuperuser
```

Follow the prompts to create admin credentials.

### Step 10: Run Server
```bash
python manage.py runserver
```

The API will be available at: `http://127.0.0.1:8000/`

---

## API Test Commands (After Server is Running)

Open a new terminal and run these curl commands:

### Test 1: Predict Performance
```bash
curl -X POST http://127.0.0.1:8000/api/predict/ \
  -H "Content-Type: application/json" \
  -d '{
    "hours_studied": 6,
    "previous_scores": 78,
    "extracurricular": true,
    "sleep_hours": 7,
    "sample_papers": 3
  }'
```

Expected response:
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

### Test 2: Get All Records
```bash
curl http://127.0.0.1:8000/api/records/
```

### Test 3: Get Statistics
```bash
curl http://127.0.0.1:8000/api/statistics/
```

### Test 4: Admin Panel
Open in browser: `http://127.0.0.1:8000/admin/`
Use superuser credentials created in Step 9

---

## File Locations

**Project Root**: `/home/humura/Documents/workings/Year 3/ML/AI_model/student_ml/`

**Key Files Created**:
- `manage.py` - Django management script
- `requirements.txt` - Dependencies
- `dataset.csv` - Training data
- `README.md` - Full documentation
- `SETUP_GUIDE.md` - Setup instructions
- `student_ml/settings.py` - Django settings
- `student_ml/urls.py` - Main URL routing
- `performance/models.py` - Database model
- `performance/views.py` - API endpoints
- `performance/serializers.py` - Data serializers
- `performance/urls.py` - App URL routing
- `performance/load_data.py` - Data loading script
- `performance/train_model.py` - Model training script
- `performance/tests.py` - Unit tests

---

## Key Information

**Database**: SQLite (db.sqlite3 - created automatically)
**ML Model**: RandomForestRegressor (model.pkl - created after training)
**Framework**: Django 4.2.7 + Django REST Framework 3.14.0
**Python Version**: 3.x (recommended 3.8+)

---

## Troubleshooting

### Virtual environment not activating
```bash
chmod +x venv/bin/activate
source venv/bin/activate
```

### Port 8000 already in use
```bash
python manage.py runserver 8001
```

### Database errors
```bash
rm db.sqlite3
python manage.py migrate
```

### Import errors
Make sure you're in the activated virtual environment:
```bash
which python  # Should show venv/bin/python
```

---

## Next Steps After Setup

1. Modify dataset.csv with your own data
2. Retrain the model after loading new data
3. Experiment with different ML models in train_model.py
4. Deploy to production (see README.md for details)
5. Create additional features via the API

---

## Questions Answered (From Assignment)

### a. What is the purpose of joblib?

Joblib is used for:
1. **Model Serialization**: Save/load ML models as .pkl files
2. **Parallel Processing**: Speed up computations with multiple cores
3. **Memory Efficiency**: Memory-mapping for large arrays
4. **Caching**: Store function results

In this project: Saves trained RandomForestRegressor to `performance/model.pkl`

### b. Other libraries that can achieve the same as joblib

1. **pickle** - Built-in, basic serialization
2. **dill** - Extended pickle with more object types
3. **cloudpickle** - Better for distributed computing
4. **onnx** - Standard model format (cross-framework)
5. **h5py** - Hierarchical data format
6. **protobuf** - Platform-independent serialization
7. **MLflow** - Full ML lifecycle management

**joblib is best for scikit-learn models** - it's optimized for numpy arrays and sparse matrices.

---

All files are ready to use. Just run the commands above!
