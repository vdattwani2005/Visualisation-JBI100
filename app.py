from dash import Dash
import dash_bootstrap_components as dbc
from layout import create_layout
from callbacks import register_callbacks

app = Dash(__name__,
          suppress_callback_exceptions=True,
          external_stylesheets=[dbc.themes.DARKLY])

app.title = "Australian Shark Incident Dashboard"
app.layout = create_layout()
register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)