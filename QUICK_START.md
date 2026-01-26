# 🚀 Quick Reference Card

## Start the Application (2 Steps)

### Step 1️⃣: Backend (Terminal 1)
```bash
cd "/home/humura/Documents/workings/Year 3/ML/AI_models/student_ml"
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```
✅ Backend ready at `http://localhost:8000`

### Step 2️⃣: Frontend (Terminal 2)
```bash
cd frontend
npm install  # Only needed first time
npm start
```
✅ Frontend opens at `http://localhost:3000`

---

## 🎯 Main Features

| Feature | How to Use |
|---------|-----------|
| **Make Predictions** | Tab 1: Adjust sliders → Click "Make Prediction" |
| **View Records** | Tab 2: See all predictions in a table |
| **Check Statistics** | Tab 3: View analytics & insights |

---

## 🔧 Useful Commands

```bash
# Frontend
npm start          # Start dev server
npm run build      # Production build
npm install        # Install dependencies
npm test           # Run tests

# Backend
python manage.py runserver           # Start server
python manage.py migrate             # Apply migrations
python manage.py shell               # Python interactive shell
python manage.py createsuperuser     # Create admin user
```

---

## 🆘 Fix Common Issues

```bash
# Port already in use?
npm start -- --port 3001                    # Change React port
python manage.py runserver 8001              # Change Django port

# Need to reinstall?
cd frontend && rm -rf node_modules && npm install

# Database broken?
rm db.sqlite3 && python manage.py migrate

# Model missing?
python manage.py shell
>>> from performance.train_model import train
>>> train()
>>> exit()
```

---

## 📂 File Structure

```
student_ml/
├── frontend/                    # ← React UI (NEW!)
│   ├── src/
│   │   ├── components/         # 3 main components
│   │   ├── api/                # API client
│   │   └── App.js              # Main app
│   └── package.json
├── performance/                # ML app
│   ├── models.py
│   ├── views.py               # API endpoints
│   ├── train_model.py         # Train ML model
│   └── model.pkl              # Saved model
├── requirements.txt           # Python packages
├── manage.py
├── UI_OVERVIEW.md             # UI guide
└── FRONTEND_SETUP.md          # Setup guide
```

---

## 🌐 API Endpoints

```
POST   /api/predict/        → Make prediction
GET    /api/records/        → Get all records
GET    /api/statistics/     → Get stats
GET    /admin/              → Admin panel
```

---

## ⚙️ Key Changes Made

✅ Added `django-cors-headers` to requirements.txt
✅ Updated Django settings for CORS
✅ Created React frontend with 3 tabs
✅ Built beautiful responsive UI
✅ Integrated Axios for API calls
✅ Added comprehensive documentation

---

## 📊 UI Components

1. **PredictionForm** - Input student data via sliders
2. **RecordsView** - Display predictions in table
3. **StatisticsView** - Show analytics dashboard

Each has its own JavaScript (.js) and CSS files for easy customization!

---

## 🎨 Customize Colors

Edit `frontend/src/App.css`:
```css
/* Main gradient (line ~8) */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Change to your colors, e.g.: */
background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
```

---

## 📱 Test on Phone

1. Find your computer's IP:
   ```bash
   # Mac/Linux
   ifconfig | grep inet
   
   # Windows
   ipconfig
   ```
2. On phone browser, visit: `http://[YOUR_IP]:3000`

---

## ✨ Next Steps

1. **Try it out!** Make some predictions via the UI
2. **Customize colors** - Edit frontend CSS files
3. **Deploy** - Follow deployment guides in frontend/README.md
4. **Add features** - Enhance with more components
5. **Share** - Show your beautiful ML UI to others!

---

## 📞 Troubleshooting Links

- Check `FRONTEND_SETUP.md` for setup issues
- Check `frontend/README.md` for frontend issues
- Check `COMMANDS.md` for backend commands
- Check `UI_OVERVIEW.md` for feature overview

---

## 🎓 Remember

- **Backend**: Django REST API on port 8000
- **Frontend**: React UI on port 3000
- **Both needed** for full experience
- **CORS enabled** for communication
- **Models saved** as .pkl files
- **Database**: SQLite (db.sqlite3)

---

**You now have a complete full-stack ML prediction application! 🎉**

Start both servers and enjoy! 🚀
