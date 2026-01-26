"""
Django settings for student_ml project.






















































































































































































































































**Built with ❤️ using React + Django**---4. Inspect network requests in DevTools3. Check browser console for errors (F12)2. Review Django backend logs1. Check the troubleshooting section aboveFor issues or questions:## Support- 🎯 Advanced filtering and search- 📧 Email notifications for predictions- 📱 Mobile app version (React Native)- 🌙 Dark mode toggle- 🔐 Add authentication/login- 📈 Add chart visualization for trends## Future Enhancements4. **Optimization**: Use Chrome DevTools Performance tab3. **Caching**: Implement API response caching2. **Memoization**: Use React.memo() for StatCard1. **Lazy Load Components**: Use React.lazy() for tabs## Performance Tips```const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';```javascriptThen update `src/api/client.js` to use it:```REACT_APP_API_URL=http://localhost:8000/api```Create a `.env` file in the frontend folder (optional):## Environment Variables```CMD ["nginx", "-g", "daemon off;"]EXPOSE 80COPY --from=build /app/build /usr/share/nginx/htmlFROM nginx:alpineRUN npm run buildCOPY . .RUN npm ciCOPY package*.json ./WORKDIR /appFROM node:18-alpine as build```dockerfileCreate a `Dockerfile` in the frontend folder:### Option 3: Docker4. Set publish directory: `build`3. Set build command: `npm run build`2. Connect the frontend folder to Netlify/Vercel1. Create a repository and push code to GitHub### Option 2: Deploy to Netlify/Vercel3. Configure Django to serve the static files2. Move the `build` folder to Django's static folder1. Build the React app### Option 1: Serve with Django (Recommended)## DeploymentThis creates an optimized production build in the `build/` folder.```npm run build```bash## Building for Production```>>> run()>>> from performance.load_data import runpython manage.py shellpython manage.py migraterm db.sqlite3```bash### Database errors  ```  >>> exit()  >>> train()  >>> from performance.train_model import train  python manage.py shell  ```bash- Train the ML model first:### Model not found error```npm start -- --port 3001```bash### Port 3000 already in use- Verify the backend has django-cors-headers installed- Check CORS is enabled in Django settings- Ensure Django backend is running on `http://localhost:8000`### "Failed to fetch records" error## Troubleshooting```color: #667eea;/* Accent colors */background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);/* Main gradient */```cssEdit `src/App.css` and component CSS files to change colors:### Customizing Colors- **Mobile**: < 768px- **Tablet**: 768px - 1023px- **Desktop**: 1024px+### Responsive Breakpoints- **Borders**: Subtle shadows and smooth transitions- **Accent**: Light purple/white backgrounds- **Primary**: Purple gradient (#667eea to #764ba2)### Color Scheme## Styling & CustomizationAll API calls are made through `src/api/client.js` using Axios.```GET /api/statistics/// Get statisticsGET /api/records/// Get all records}  "sample_papers": 3  "sleep_hours": 7,  "extracurricular": true,  "previous_scores": 78,  "hours_studied": 6,{POST /api/predict/// Prediction endpoint```javascriptThe frontend communicates with three main endpoints:## API Integration3. See insights and trends at a glance   - Average Study Hours   - Total Records   - Highest/Lowest Scores   - Median Performance   - Average Performance2. View key metrics:1. Click on the **"📊 Statistics"** tab### 3. Check Statistics   - Predicted performance index   - Input features (hours studied, scores, sleep, etc.)   - Student ID4. Table shows:3. Click **"🔄 Refresh"** to reload data2. Browse all student predictions in a sortable table1. Click on the **"📋 All Records"** tab### 2. View All Records4. View the predicted performance index immediately3. Click **"🚀 Make Prediction"** button   - **Extracurricular**: Toggle participation status   - **Sample Papers**: 0-10 papers solved   - **Sleep Hours**: 0-12 hours per night   - **Previous Scores**: 0-100%   - **Hours Studied**: 0-24 hours per week2. Use the sliders to adjust student parameters:1. Click on the **"🔮 Make Prediction"** tab### 1. Make Predictions## How to Use```└── README.md                      # This file├── package.json                   # Dependencies│   └── index.css                  # Global styles│   ├── index.js                   # React entry point│   ├── App.css│   ├── App.js                     # Main app component│   │   └── client.js              # Axios API client│   ├── api/│   │   └── StatisticsView.css│   │   ├── StatisticsView.js      # Show statistics│   │   ├── RecordsView.css│   │   ├── RecordsView.js         # Display all records│   │   ├── PredictionForm.css│   │   ├── PredictionForm.js      # Main prediction form│   ├── components/├── src/│   └── index.html                # HTML template├── public/frontend/```## Project StructureThe application will open at `http://localhost:3000````npm start```bash### Step 2: Start the Development Server```npm installcd frontend```bash### Step 1: Install Dependencies- Django backend running on `http://localhost:8000`- Node.js 14+ and npm### Prerequisites## Installation & Setup- **Chart.js** - Data visualization (optional enhancement)- **CSS3** - Modern styling with gradients and animations- **Axios** - HTTP Client for API calls- **React 18** - UI Framework## Tech Stack- ⚡ **Real-time Updates**: Automatic refresh of data after predictions- 🎨 **Responsive Design**: Works perfectly on desktop, tablet, and mobile- 📊 **Statistics Dashboard**: Real-time statistics and insights- 📋 **Records View**: Browse all predictions in an organized table- 📝 **Prediction Form**: Easy-to-use form with slider inputs for student data✨ **Interactive UI Components:**## FeaturesA modern, responsive web interface for the Django ML Prediction API."""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-your-secret-key-change-this-in-production'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'performance',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'student_ml.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'student_ml.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

CORS_ALLOW_CREDENTIALS = True
