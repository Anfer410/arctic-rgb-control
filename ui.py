import dash_daq as daq
from dash import html, dcc


def create_layout(initial_color=dict(rgb=dict(r=255, g=0, b=0, a=0))):
    return html.Div([
        html.Label("Channels:"),
        dcc.RadioItems(
            id="channel",
            options=[
                {'label': "Channel 1", 'value': 'ch1'},
                {'label': "Channel 2", 'value': 'ch2'},
                {'label': "Channel 3", 'value': 'ch3'},
                {'label': "Channel 4", 'value': 'ch4'}],
            value='ch1',
            inline=True),
        html.Button(
            "Save",
            id="save",
            n_clicks=0
        ),
        daq.ColorPicker(
            id='color-picker',
            label='Pick a color',
            value=initial_color  # Initial color (red)
        ),
        html.Div(id='color'),
        html.Div(id='channel-curr'),
        html.Div(id='save-output')
    ])
