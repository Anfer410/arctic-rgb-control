import asyncio
from dash import Dash, Input, Output, callback
from ui import create_layout
from threading import Thread
from config import config_loader, config_writer
from datetime import datetime
from utils import send_data, open_port, dict2tuple

# ** Global variables**
color = config_loader("config.ini")
queue = asyncio.Queue()
queue.put_nowait(color)
channel = 'ch1'
led_start_time = 8
led_stop_time = 22


# ** Async Part **
def serial_writer(port, data):
    send_data(
        port, 0,
        dict2tuple(data['ch1']),
        dict2tuple(data['ch2']),
        dict2tuple(data['ch3']),
        dict2tuple(data['ch4']))


async def queue_processor(queue):
    last_message = None
    serial_port = open_port()
    global color

    while True:
        if datetime.now().hour >= led_start_time and datetime.now().hour <= led_stop_time:
            try:
                message = await asyncio.wait_for(queue.get(), timeout=1)
                if message:
                    serial_writer(serial_port, message)
                    last_message = message
                    color = message

            except asyncio.TimeoutError:
                if last_message:
                    serial_writer(serial_port, last_message)
        else:
            await asyncio.sleep(10)


async def async_main():
    """Main async function"""
    global queue
    await asyncio.gather(queue_processor(queue))


def async_main_wrapper():
    """Not async Wrapper around async_main to run it as target function of Thread"""
    asyncio.run(async_main())


# *** Dash Part ***:
app = Dash(__name__)
app.layout = create_layout()


# Callback to handle color selection
@callback(
    Output('color', 'children'),
    Input('color-picker', 'value')
)
def handle_color_selection(value):
    global queue
    data = dict(ch1=None, ch2=None, ch3=None, ch4=None)
    if None is not value:
        for chan in color:
            if chan == channel:
                data[chan] = value['rgb']
            else:
                data[chan] = color[chan]

        queue.put_nowait(data)
        return f"Selected color: {data}"


# Callback to handle channel selection
@callback(
    Output('color-picker', 'value'),
    Input('channel', 'value')
)
def handle_channel_selection(value):
    global channel
    channel = value
    return dict(rgb=color[channel])


@callback(
    Output('save-output', 'children'),
    Input('save', 'n_clicks')
)
def handle_save_action(n_clicks):
    config_writer('config.ini', color)

@callback(
    Output('slider-output', 'children'),
    Input('time-slider', 'value')
)
def handle_led_timer(value):
    global led_start_time
    global led_stop_time
    led_start_time, led_stop_time = value
    return f"Start: {value[0]}, Stop: {value[1]}"



if __name__ == '__main__':
    # run all async stuff in another thread
    th = Thread(target=async_main_wrapper)
    th.start()
    # run Dash server
    app.run(port=9000, debug=False)
    th.join()
    