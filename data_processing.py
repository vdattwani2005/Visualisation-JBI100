import pandas as pd

file_path = "Australian Shark-Incident Database Public Version 2.xlsx"
def load_data():
    df = pd.read_excel("/Users/vdattwani/Visualisation-JBI100/Australian Shark-Incident Database Public Version (2).xlsx")

    # Clean and preprocess
    df['Year'] = df['Incident.year']
    df['Month'] = df['Incident.month']
    df['Season'] = df['Month'].apply(get_season)

    # Handle missing values
    df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
    df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')

    # Clean location names
    df['Location'] = df['Location'].fillna('Unknown')

    return df


def get_season(month):
    if month in [12, 1, 2]:
        return 'Summer'
    elif month in [3, 4, 5]:
        return 'Autumn'
    elif month in [6, 7, 8]:
        return 'Winter'
    else:
        return 'Spring'


def process_data(start_year, end_year, region=None, activity=None):
    df = load_data()

    # Apply filters
    mask = (df['Year'] >= start_year) & (df['Year'] <= end_year)
    if region:
        mask &= df['State'] == region
    if activity:
        mask &= df['Victim.activity'] == activity

    return df[mask]


def get_stats(df):
    return {
        'total': len(df),
        'fatal': len(df[df['Victim.injury'] == 'fatal']),
        'species': df['Shark.common.name'].nunique()
    }