"""
Load dataset from CSV file into the database.
Run this once to populate the database with training data.
"""
import pandas as pd
from performance.models import StudentPerformance


def run():
    """
    Load data from dataset.csv into the database.
    """
    try:
        df = pd.read_csv('dataset.csv')
        count = 0
        
        for _, row in df.iterrows():
            # Check if record already exists to avoid duplicates
            if not StudentPerformance.objects.filter(
                hours_studied=row['Hours Studied'],
                previous_scores=row['Previous Scores'],
                performance_index=row['Performance Index']
            ).exists():
                StudentPerformance.objects.create(
                    hours_studied=int(row['Hours Studied']),
                    previous_scores=int(row['Previous Scores']),
                    extracurricular=row['Extracurricular Activities'].lower() == 'yes',
                    sleep_hours=int(row['Sleep Hours']),
                    sample_papers=int(row['Sample Question Papers Practiced']),
                    performance_index=float(row['Performance Index']),
                )
                count += 1
        
        print(f"Successfully loaded {count} new records into the database.")
        
    except FileNotFoundError:
        print("Error: dataset.csv not found. Make sure it's in the project root directory.")
    except Exception as e:
        print(f"Error loading data: {str(e)}")


if __name__ == '__main__':
    run()
