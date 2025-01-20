import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd
from custumer_stats import getCustomerStats

# Initialize Dash app
app = dash.Dash(__name__)

# Get all Plotly figures from getCustomerStats()
figures = getCustomerStats()

# Customize plot colors
colors = {'background': '#009090', 'text': '#ccffff'}

# For each figure, update layout and store in a list of dcc.Graph elements
graph_components = []
for i, fig in enumerate(figures):
    fig.update_layout(
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )
    graph_components.append(
        dcc.Graph(id=f'graph-{i}', figure=fig)
    )

# Define app layout
app.layout = html.Div(
    style={'backgroundColor': colors['background']},
    children=[
        html.H1(
            children='Iris Graph Display',
            style={'color': colors['text'], 'textAlign': 'center'}
        ),
        html.Div(
            children="Standard dataset visualization by LINC_STEM",
            style={'color': colors['text']}
        ),
        # Name input
        html.Div(
            children=[
                "Input - your name:",
                dcc.Input(
                    id='my-input',
                    value='your name',
                    type='text',
                    debounce=True
                )
            ],
            style={'marginTop': '20px', 'marginBottom': '20px'}
        ),
        # Output of user interaction
        html.Div(
            id='my-output',
            style={'color': colors['text'], 'marginBottom': '20px'}
        ),
        # A container that holds all the Graph components
        html.Div(children=graph_components)
    ]
)

# Callback for user interaction


@app.callback(
    dash.Output(component_id='my-output', component_property='children'),
    dash.Input(component_id='my-input', component_property='value')
)
def update_name(input_value):
    return f'Your name is {input_value}'


# Run app
if __name__ == '__main__':
    app.run_server(debug=True)


# Example of a Python decorator (unrelated to Dash)
def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper


@my_decorator
def say_hello():
    print("Hello!")


say_hello()
