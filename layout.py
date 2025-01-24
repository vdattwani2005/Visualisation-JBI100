from dash import html, dcc


def create_layout():
    return html.Div([
        html.H1("Australian Shark Incident Analysis", className="dashboard-title"),

        # Stats Bar
        html.Div([
            html.Div(id='total-incidents', className='stat-box'),
            html.Div(id='fatal-incidents', className='stat-box'),
            html.Div(id='species-count', className='stat-box'),
        ], className="stats-row"),

        # Filters
        html.Div([
            dcc.Dropdown(
                id='region-filter',
                options=[
                    {'label': 'New South Wales', 'value': 'NSW'},
                    {'label': 'Queensland', 'value': 'QLD'},
                    {'label': 'Western Australia', 'value': 'WA'},
                    {'label': 'South Australia', 'value': 'SA'},
                    {'label': 'Victoria', 'value': 'VIC'},
                    {'label': 'Tasmania', 'value': 'TAS'},
                    {'label': 'Northern Territory', 'value': 'NT'}
                ],
                placeholder="Select Region",
                className="filter"
            ),
            dcc.Dropdown(
                id='activity-filter',
                options=[
                    {'label': 'Swimming', 'value': 'Swimming'},
                    {'label': 'Surfing', 'value': 'Surfing'},
                    {'label': 'Diving', 'value': 'Diving'},
                    {'label': 'Fishing', 'value': 'Fishing'}
                ],
                placeholder="Select Activity",
                className="filter"
            ),
            dcc.RangeSlider(
                id='year-range',
                min=1791,
                max=2023,
                value=[1791, 2023],
                marks={i: str(i) for i in range(1791, 2024, 20)},
                className="year-slider"
            )
        ], className="filters-row"),

        # Main Grid
        html.Div([
            html.Div([
                html.H3("Geographic Distribution", className="chart-title"),
                dcc.Graph(id='map-chart', className="chart")
            ], className="map-container"),

            html.Div([
                html.H3("Seasonal Patterns", className="chart-title"),
                dcc.Graph(id='radar-chart', className="chart")
            ], className="radar-container"),
        ], className="top-row"),

        html.Div([
            html.Div([
                html.H3("Temporal Trends", className="chart-title"),
                dcc.Graph(id='temporal-chart', className="chart")
            ], className="chart-container"),

            html.Div([
                html.H3("Species Distribution", className="chart-title"),
                dcc.Graph(id='species-chart', className="chart")
            ], className="chart-container"),
        ], className="bottom-row")
    ], className="dashboard-container")