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

    else:
        color = {
            "ch1": dict(r=0, g=0, b=0, a=0),
            "ch2": dict(r=0, g=0, b=0, a=0),
            "ch3": dict(r=0, g=0, b=0, a=0),
            "ch4": dict(r=0, g=0, b=0, a=0)
        }

    return color


def config_writer(config_file, color):
    config = configparser.ConfigParser()
    
    # Add sections and their respective key-value pairs    
    if None is not color['ch1']:
        config['CHANNEL_1'] = {'color': rgb2hex(color['ch1']), 'brightness': color['ch1']['a']}
    else:
        config['CHANNEL_1'] = {'color': '#000000', 'brightness': '0'}
    
    if None is not color['ch2']:
        config['CHANNEL_2'] = {'color': rgb2hex(color['ch2']), 'brightness': color['ch2']['a']}
    else:
        config['CHANNEL_2'] = {'color': '#000000', 'brightness': '0'}
    
    if None is not color['ch3']:
        config['CHANNEL_3'] = {'color': rgb2hex(color['ch3']), 'brightness': color['ch3']['a']}
    else:
        config['CHANNEL_3'] = {'color': '#000000', 'brightness': '0'}
    
    if None is not color['ch4']:
        config['CHANNEL_4'] = {'color': rgb2hex(color['ch4']), 'brightness': color['ch4']['a']}
    else:
        config['CHANNEL_4'] = {'color': '#000000', 'brightness': '0'}
    
    # Write to an INI file
    with open(config_file, 'w') as configfile:
        config.write(configfile)