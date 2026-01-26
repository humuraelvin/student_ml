# Quick Start Guide - Full Stack Setup

## Backend Setup (Django)

### 1. Navigate to Project
```bash
cd "/home/humura/Documents/workings/Year 3/ML/AI_models/student_ml"
```

### 2. Create and Activate Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

Note: `django-cors-headers` is now included for frontend integration.

### 4. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Load Dataset
```bash
python manage.py shell
```
Then type:
```python
from performance.load_data import run
run()
exit()
```

### 6. Train ML Model
```bash
python manage.py shell
```
Then type:
```python
from performance.train_model import train
train()
exit()
```

### 7. Start Backend Server
```bash
python manage.py runserver
```

The backend will be available at `http://localhost:8000`

---

## Frontend Setup (React)

### 1. Navigate to Frontend Folder
```bash
cd frontend
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Start Development Server
```bash
npm start
```

The frontend will open at `http://localhost:3000`

---

## Quick Commands Reference

**Backend Commands:**
```bash
# Activate virtual environment
source venv/bin/activate

# Run migrations
python manage.py migrate

# Load data
python manage.py shell < load_data.py

# Train model
python manage.py shell < train_model.py

# Start server
python manage.py runserver

# Stop server
Ctrl + C
```

**Frontend Commands:**
```bash
# Install dependencies
npm install

# Start dev server
npm start

# Build for production
npm run build

# Stop dev server
Ctrl + C
```

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│         React Frontend (localhost:3000)             │
│         - Prediction Form                           │
│         - Records Table                             │
│         - Statistics Dashboard                      │
│                                                     │
└──────────────────┬──────────────────────────────────┘
                   │ HTTP/REST
                   ↓
┌─────────────────────────────────────────────────────┐
│                                                     │
│      Django Backend (localhost:8000)                │
│      - /api/predict/ - Make predictions             │
│      - /api/records/ - Get all records              │
│      - /api/statistics/ - Get stats                 │
│      - /admin/ - Admin panel                        │
│                                                     │
└──────────────────┬──────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────┐
│                                                     │
│        Machine Learning Model                       │
│        RandomForestRegressor (model.pkl)            │
│        - Trained on student dataset                 │
│        - Predicts performance index                 │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## Troubleshooting

### Frontend not connecting to backend
1. Ensure Django is running on `http://localhost:8000`
2. Check browser console (F12) for CORS errors
3. Verify CORS settings in `student_ml/settings.py`

### "Port 3000 already in use"
```bash
npm start -- --port 3001
```

### "Port 8000 already in use"
```bash
python manage.py runserver 8001
```

### Model not found error
Retrain the model:
```bash
python manage.py shell
>>> from performance.train_model import train
>>> train()
>>> exit()
```

### Database errors
```bash
rm db.sqlite3
python manage.py migrate
# Then reload data and retrain model
```

---

## Testing the Full Stack

### 1. Make a Prediction via UI
- Open `http://localhost:3000`
- Fill in the form and click "Make Prediction"
- View the result

### 2. Check Records
- Click "All Records" tab
- Should see your prediction in the table

### 3. View Statistics
- Click "Statistics" tab
- Should see updated statistics

### 4. Test API Directly (curl)
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

---

## Next Steps

1. **Customize the UI**: Edit components in `frontend/src/components/`
2. **Add More Features**: Implement authentication, charts, etc.
3. **Deploy**: Follow deployment guides in `frontend/README.md`
4. **Enhance Model**: Experiment with different ML algorithms in `performance/train_model.py`

---

## File Locations

| Component | Location |
|-----------|----------|
| Django Settings | `student_ml/settings.py` |
| API Views | `performance/views.py` |
| Data Models | `performance/models.py` |
| ML Model | `performance/model.pkl` |
| Dataset | `dataset.csv` |
| React App | `frontend/src/App.js` |
| Components | `frontend/src/components/` |
| API Client | `frontend/src/api/client.js` |

---

**Everything is ready! Start both servers and enjoy the full-stack application! 🚀**
