"""
Setup and initialization script for the Django ML Prediction API
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

# Add project to path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_ml.settings')
django.setup()


def initialize_project():
    """
    Run all initialization steps for the project.
    """
    print("=" * 60)
    print("Django ML Prediction API - Initialization")
    print("=" * 60)
    
    # Step 1: Makemigrations
    print("\n[1/4] Creating database migrations...")
    try:
        execute_from_command_line(['manage.py', 'makemigrations'])
        print("✓ Migrations created successfully")
    except Exception as e:
        print(f"✗ Error: {e}")
        return False
    
    # Step 2: Migrate
    print("\n[2/4] Applying migrations...")
    try:
        execute_from_command_line(['manage.py', 'migrate'])
        print("✓ Database migrated successfully")
    except Exception as e:
        print(f"✗ Error: {e}")
        return False
    
    # Step 3: Load data
    print("\n[3/4] Loading dataset...")
    try:
        from performance.load_data import run as load_data
        load_data()
        print("✓ Dataset loaded successfully")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Step 4: Train model
    print("\n[4/4] Training ML model...")
    try:
        from performance.train_model import train
        train()
        print("✓ Model trained successfully")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "=" * 60)
    print("Initialization complete!")
    print("Run 'python manage.py runserver' to start the API")
    print("=" * 60)


if __name__ == '__main__':
    initialize_project()
