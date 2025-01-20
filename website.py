import dash
import plotly.express as px
import pandas as pd 

app = dash.Dash(__name__)
if __name__ == '__main__':
    app.run_server(debug=True)
 #%%
 # Customize the plot
colors = {'background' : '#004d4d',
          'text' : '#ccffff'}
fig = px.scatter(df_iris, x = 'sepal_width', 
                 y = 'sepal_length', 
                 size = 'petal_length', 
                 color = 'species')

fig.update_layout(
    #plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
    )
app = dash.Dash(__name__)
app.layout = dash.html.Div(
    style={'backgroundColor':colors['background']},
    children=[
    dash.html.H1(
        children = 'Iris Graph Display', 
        style={'color':colors['text'], 
                'textAlign':'Center'}),
    dash.html.Div(
        children = '''
        Standard dataset visualization by LINC_STEM
        '''),
    # Add input
    dash.html.Div(
        children = ["Input - your name:",
                    dash.dcc.Input( # input creates input box
                        id='my-input',
                        value='your name',  
                        type='text',  # type specifies format of inputcallback invocations
                        debounce= True)]), # Add debounce to reduce 
    # Adding output of user interaction.
    dash.html.Div(
        id='my-output'
        ),
    dash.dcc.Graph(
        id = 'example-graph',
        figure=fig)
    ]
 )
@app.callback(dash.Output(component_id='my-output', 
component_property='children'),
              # Checks if enter has been pressed
              dash.Input(component_id='my-input', 
component_property='n_submit'),
              dash.State(component_id='my-input', 
component_property='value'))
def update_name(n_submit, input_value):
    if n_submit is not None:
        return f'Your name is {input_value}'
 # Note that we can add a bunch of callbacks after each other.
if __name__ == '__main__':
    app.run_server(debug=True)
 #%%
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