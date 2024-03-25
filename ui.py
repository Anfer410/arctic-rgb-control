import dash_daq as daq
from dash import html, dcc


def create_layout(led_timer, initial_color=dict(rgb=dict(r=255, g=0, b=0, a=0))):
    return html.Div([
        html.Div([
            html.Div([
                html.Label("Channels:"),
                dcc.RadioItems(
                    id="channel",
                    options=[
                        {'label': "Channel 1", 'value': 'ch1'},
                        {'label': "Channel 2", 'value': 'ch2'},
                        {'label': "Channel 3", 'value': 'ch3'},
                        {'label': "Channel 4", 'value': 'ch4'}],
                    value='ch1',
                    inline=False
                ),
                html.Button(
                    "Save",
                    id="save",
                    n_clicks=0,
                    style={'width': '100%'}
                ),
            ], style={'padding': 10, 'flex': 1, 'flex-shrink': 0}),
            html.Div([
                daq.ColorPicker(
                    id='color-picker',
                    label='Pick color',
                    size=1024,
                    value=initial_color  # Initial color (red)
                ),
                dcc.RangeSlider(
                    0,
                    23,
                    1,
                    value=led_timer,
                    id='time-slider'
                )

            ], style={'padding': 10, 'flex': 7}),
        ], style={'display': 'flex', 'flexDirection': 'row'}),
        html.Div([
            html.Div(id='color'),
            html.Div(id='channel-curr'),
            html.Div(id='save-output'),
            html.Div(id='slider-output')

        ])
    ])
