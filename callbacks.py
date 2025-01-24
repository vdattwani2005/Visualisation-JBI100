from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from data_processing import process_data, get_stats
from dash import html
import calendar


def register_callbacks(app):
    @app.callback(
        [Output('map-chart', 'figure'),
         Output('radar-chart', 'figure'),
         Output('temporal-chart', 'figure'),
         Output('species-chart', 'figure'),
         Output('total-incidents', 'children'),
         Output('fatal-incidents', 'children'),
         Output('species-count', 'children'),
         Output('most-dangerous-species', 'children'),
         Output('insights-content', 'children')],
        [Input('year-range', 'value'),
         Input('region-filter', 'value'),
         Input('activity-filter', 'value'),
         Input('season-filter', 'value')]
    )
    def update_dashboard(year_range, region, activity, season):
        df = process_data(year_range[0], year_range[1], region, activity, season)

        # Map
        map_fig = go.Figure(go.Scattermapbox(
            lat=df['Latitude'],
            lon=df['Longitude'],
            mode='markers',
            marker=dict(size=8, color='#4287f5'),
            text=df.apply(
                lambda
                    x: f"Location: {x['Location']}<br>Date: {x['Year']}<br>Activity: {x['Victim.activity']}<br>Species: {x['Shark.common.name']}<br>Outcome: {x['Victim.injury']}",
                axis=1),
            hoverinfo='text'
        ))
        map_fig.update_layout(
            mapbox=dict(
                style="carto-darkmatter",
                center=dict(lat=-25.2744, lon=133.7751),
                zoom=3
            ),
            margin=dict(r=0, t=0, l=0, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )

        # Monthly Radar Chart
        monthly = df.groupby('Month').size().reindex(range(1, 13), fill_value=0)
        month_names = [calendar.month_name[i] for i in range(1, 13)]

        radar_fig = go.Figure(go.Scatterpolar(
            r=monthly.values,
            theta=month_names,
            fill='toself',
            fillcolor='rgba(66, 135, 245, 0.5)',
            line=dict(color='#4287f5', width=2)
        ))
        radar_fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    showticklabels=True,
                    gridcolor="white",
                    gridwidth=0.5
                ),
                angularaxis=dict(
                    gridcolor="white",
                    gridwidth=0.5,
                    direction='clockwise'
                )
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(r=0, t=0, l=0, b=0)
        )

        # Temporal Trends
        temporal = df.groupby('Year').size().reset_index(name='Count')
        temporal_fig = go.Figure(go.Scatter(
            x=temporal['Year'],
            y=temporal['Count'],
            mode='lines',
            line=dict(color='#4287f5', width=2)
        ))
        temporal_fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0.1)',
            xaxis=dict(
                showgrid=True,
                gridcolor='rgba(255,255,255,0.1)',
                title='Year'
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(255,255,255,0.1)',
                title='Number of Incidents'
            ),
            font=dict(color='white'),
            margin=dict(r=20, t=20, l=20, b=20)
        )

        # Species Distribution
        species_data = df['Shark.common.name'].value_counts().head(7)
        species_fig = go.Figure(data=[
            go.Bar(
                x=species_data.index,
                y=species_data.values,
                marker_color='#4287f5'
            )
        ])
        species_fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0.1)',
            xaxis=dict(
                showgrid=True,
                gridcolor='rgba(255,255,255,0.1)',
                title='Species'
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(255,255,255,0.1)',
                title='Number of Incidents'
            ),
            font=dict(color='white'),
            margin=dict(r=20, t=20, l=20, b=20)
        )

        # Generate insights
        peak_month = calendar.month_name[monthly.idxmax()]
        peak_year = df.groupby('Year').size().idxmax() if len(df) > 0 else "N/A"
        fatal_percentage = (df['Victim.injury'].str.lower() == 'fatal').mean() * 100 if len(df) > 0 else 0

        insights = html.Div([
            html.P(f"Peak activity recorded in {peak_year} with most incidents occurring in {peak_month}."),
            html.P(f"Fatal incidents comprise {fatal_percentage:.1f}% of all recorded encounters."),
            html.P(f"Most incidents occur along the eastern coast of Australia.")
        ])

        stats = get_stats(df)
        return (
            map_fig,
            radar_fig,
            temporal_fig,
            species_fig,
            f"Total Incidents: {stats['total']}",
            f"Fatal Incidents: {stats['fatal']}",
            f"Unique Species: {stats['species']}",
            f"Most Dangerous: {stats['dangerous']}",
            insights
        )