import dash
from dash import html, dcc
from custumer_stats import getCustomerStats
from data_cleaning import getSignificantTables, getCorrelationHeatmap
from pröva import getConfusion, roc


app = dash.Dash(__name__)


figures = getCustomerStats()

colors = {'background': '#b0c4de', 'text': '#000036'}

graph_components = []
for i, fig in enumerate(figures):
    fig.update_layout(
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )
    graph_components.append(
        dcc.Graph(id=f'graph-{i}', figure=fig)
    )


app.layout = html.Div(
    style={'backgroundColor': colors['background']},
    children=[
        html.H1(
            children='Variable relevance for attribution',
            style={'color': colors['text'], 'textAlign': 'center'}
        ),
        html.Div(
            children="",
            style={'color': colors['text']}
        ),


        html.Div(
            id='my-output',
            style={'color': colors['text'], 'marginBottom': '20px'}
        ),

        html.Div(children=graph_components),
        html.H1("Credit Card Customer Analysis", style={'textAlign': 'center'}),
        html.Div([
            html.H2("Significant Categories Table"),
            getSignificantTables()
        ]),
        html.Div([
            html.H2("Correlation Heatmap"),
            dcc.Graph(figure=getCorrelationHeatmap())
        ]),
        html.Div([
            html.H2("Confusion Matrix ("),
            dcc.Graph(figure=getConfusion())
        ]),
        html.Div([
            html.H1("Random Forest ROC Curve Example"),
            dcc.Graph(
                id='roc-graph',
                figure=roc()  # pass the Plotly figure
            )])
    ]
)


def update_name(input_value):
    return f'Your name is {input_value}'


if __name__ == '__main__':
    app.run_server(debug=True)


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
