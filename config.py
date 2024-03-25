import configparser
import os
from utils import hex2rgb, rgb2hex


def config_loader(config_file):
    if os.path.isfile(config_file):
        config = configparser.ConfigParser()
        config.read(config_file)

        color = {
            "ch1": hex2rgb(config["CHANNEL_1"]["color"]),
            "ch2": hex2rgb(config["CHANNEL_2"]["color"]),
            "ch3": hex2rgb(config["CHANNEL_3"]["color"]),
            "ch4": hex2rgb(config["CHANNEL_4"]["color"])}
        
        try:
            led_timer = [int(config["LED_TIMER"]["start"]), int(config["LED_TIMER"]["stop"])]
        except KeyError:
            led_timer = [8,22]

    else:
        color = {
            "ch1": dict(r=0, g=0, b=0, a=0),
            "ch2": dict(r=0, g=0, b=0, a=0),
            "ch3": dict(r=0, g=0, b=0, a=0),
            "ch4": dict(r=0, g=0, b=0, a=0)
        }

        led_start = 8
        led_stop = 22
        led_timer = [led_start, led_stop]

    return color, led_timer


def config_writer(config_file, color, led_start_time, led_stop_time):
    config = configparser.ConfigParser()
    
    if os.path.isfile(config_file):
        config.read(config_file)

    # Add sections and their respective key-value pairs    
    if None is not color['ch1']:
        # config['CHANNEL_1'] = {'color': rgb2hex(color['ch1']), 'brightness': color['ch1']['a']}
        config.set('CHANNEL_1', 'color', str(rgb2hex(color['ch1'])))
        config.set('CHANNEL_1', 'brightness', str(color['ch1']['a']))
    else:
        # config['CHANNEL_1'] = {'color': '#000000', 'brightness': '0'}
        config.set('CHANNEL_1', 'color', '#000000')
        config.set('CHANNEL_1', 'brightness', '0')

    if None is not color['ch2']:
        # config['CHANNEL_2'] = {'color': rgb2hex(color['ch2']), 'brightness': color['ch2']['a']}
        config.set('CHANNEL_2', 'color', str(rgb2hex(color['ch2'])))
        config.set('CHANNEL_2', 'brightness', str(color['ch2']['a']))
    else:
        # config['CHANNEL_2'] = {'color': '#000000', 'brightness': '0'}
        config.set('CHANNEL_2', 'color', '#000000')
        config.set('CHANNEL_2', 'brightness', '0')

    if None is not color['ch3']:
        # config['CHANNEL_3'] = {'color': rgb2hex(color['ch3']), 'brightness': color['ch3']['a']}
        config.set('CHANNEL_3', 'color', str(rgb2hex(color['ch3'])))
        config.set('CHANNEL_3', 'brightness', str(color['ch3']['a']))
    else:
        # config['CHANNEL_3'] = {'color': '#000000', 'brightness': '0'}
        config.set('CHANNEL_3', 'color', '#000000')
        config.set('CHANNEL_3', 'brightness', '0')

    if None is not color['ch4']:
        # config['CHANNEL_4'] = {'color': rgb2hex(color['ch4']), 'brightness': color['ch4']['a']}
        config.set('CHANNEL_4', 'color', str(rgb2hex(color['ch4'])))
        config.set('CHANNEL_4', 'brightness', str(color['ch4']['a']))
    else:
        # config['CHANNEL_4'] = {'color': '#000000', 'brightness': '0'}
        config.set('CHANNEL_4', 'color', '#000000')
        config.set('CHANNEL_4', 'brightness', '0')

    try:
        config.set("LED_TIMER", 'start', str(led_start_time))
        config.set("LED_TIMER", 'stop', str(led_stop_time))
    except configparser.NoSectionError:
        config.add_section("LED_TIMER")
        config.set("LED_TIMER", 'start', str(led_start_time))
        config.set("LED_TIMER", 'stop', str(led_stop_time))


    # Write to an INI file
    with open(config_file, 'w') as configfile:
        config.write(configfile)
