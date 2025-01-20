import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd

# Initialize Dash app
app = dash.Dash(__name__)

# Load Iris dataset
df_iris = px.data.iris()

# Customize the plot
colors = {'background': '#004d4d', 'text': '#ccffff'}
fig = px.scatter(
    df_iris,
    x='sepal_width',
    y='sepal_length',
    size='petal_length',
    color='species'
)
fig.update_layout(
    paper_bgcolor=colors['background'],
    font_color=colors['text']
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
            children="Standard dataset visualization by LINC_STEM"
        ),
        # Add input
        html.Div(
            children=[
                "Input - your name:",
                dcc.Input(
                    id='my-input',
                    value='your name',
                    type='text',
                    debounce=True
                )
            ]
        ),
        # Add output of user interaction
        html.Div(id='my-output'),
        # Add graph
        dcc.Graph(id='example-graph', figure=fig)
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

# Example of a decorator
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
