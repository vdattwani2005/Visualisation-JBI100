import pandas as pd

file_path = "Australian Shark-Incident Database Public Version 2.xlsx"
def load_data():
    df = pd.read_excel("/Users/vdattwani/Visualisation-JBI100/Australian Shark-Incident Database Public Version (2).xlsx")

    df['Year'] = df['Incident.year']
    df['Month'] = df['Incident.month']
    df['Season'] = df['Month'].apply(get_season)

    df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
    df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')

    df['Location'] = df['Location'].fillna('Unknown')
    df['Shark.common.name'] = df['Shark.common.name'].fillna('Unknown Species')
    df['Victim.injury'] = df['Victim.injury'].fillna('Unknown')
    df['Victim.activity'] = df['Victim.activity'].str.title()  # Capitalize first letter

    return df


def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Autumn'



def process_data(start_year, end_year, region=None, activity=None, season=None):
    df = load_data()
    mask = (df['Year'] >= start_year) & (df['Year'] <= end_year)
    if region:
        mask &= df['State'] == region
    if activity:
        mask &= df['Victim.activity'] == activity
    if season:
        mask &= df['Season'] == season
    return df[mask]


def get_stats(df):
    most_dangerous = (df[df['Victim.injury'].str.lower() == 'fatal']['Shark.common.name']
                     .value_counts().index[0]
                     if len(df[df['Victim.injury'].str.lower() == 'fatal']) > 0
                     else 'No fatal incidents')
    return {
        'total': len(df),
        'fatal': len(df[df['Victim.injury'].str.lower() == 'fatal']),
        'species': df['Shark.common.name'].nunique(),
        'dangerous': most_dangerous
    }