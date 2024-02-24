import time
import serial
import configparser
import os


def rgb2hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])


def hex2rgb(hex):
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))


def spawn_config():
    # Create a configparser object
    config = configparser.ConfigParser()

    # Add sections and their respective key-value pairs
    config['PORT'] = {'port': '/dev/ttyUSB1'}
    config['CHANNEL_1'] = {'color': '#03f8fc', 'brightness': '100'}
    config['CHANNEL_2'] = {'color': '#7b03fc', 'brightness': '70'}
    config['CHANNEL_3'] = {'color': '#03f8fc', 'brightness': '100'}
    config['CHANNEL_4'] = {'color': '#03f8fc', 'brightness': '0'}

    # Write to an INI file
    with open('config.ini', 'w') as configfile:
        config.write(configfile)


def open_port(port='/dev/ttyUSB1'):
    try:
        serial_port = serial.Serial(
            port=port,  # Change '/dev/ttyUSB0' to your CH340 board port
            baudrate=250000,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            dsrdtr=True
            )
    except Exception as ex:
        print(ex)

    return serial_port


def calculate_brightness(*args):
    color = args[0]
    brightness = int(args[1])
    if brightness > 0:
        brightness = brightness / 100

    return (
        int(color[0]*brightness),
        int(color[1]*brightness),
        int(color[2]*brightness))


def get_colors():
    config = configparser.ConfigParser()
    config.read("conf.ini")
    color_1 = calculate_brightness(
        hex2rgb(config["CHANNEL_1"]["color"]),
        int(config["CHANNEL_1"]["brightness"]))
    color_2 = calculate_brightness(
        hex2rgb(config["CHANNEL_2"]["color"]),
        int(config["CHANNEL_2"]["brightness"]))
    color_3 = calculate_brightness(
        hex2rgb(config["CHANNEL_3"]["color"]),
        int(config["CHANNEL_3"]["brightness"]))
    color_4 = calculate_brightness(
        hex2rgb(config["CHANNEL_4"]["color"]),
        int(config["CHANNEL_4"]["brightness"]))

    return color_1, color_2, color_3, color_4


def set_data(sc_code, color_1, color_2, color_3, color_4):
    header = [1, 2, 3, 255, 5, 255, 2, 3]

    if sc_code != 0:
        sc_code = 98
        array = [*header, sc_code, 1, 254, 1, 254]
        array = [*array, 0, len(array)]

    else:
        array = [*header, sc_code, *color_1, *color_2, *color_3, *color_4]
        array = [*array, 0, len(array)]

    return array


def send_data(serial_port, sc_code, color_1, color_2, color_3, color_4):
    data = set_data(sc_code, color_1, color_2, color_3, color_4)
    try:
        serial_port.write(bytearray(data))
    except Exception as ex:
        print(ex)


def main():
    # If config doesn't exist, create it
    if not os.path.isfile('config.ini'):
        spawn_config()
    serial_port = open_port()

    while True:
        color_1, color_2, color_3, color_4 = get_colors()

        send_data(serial_port, 0, color_1, color_2, color_3, color_4)
        time.sleep(1)


if __name__ == "__main__":
    main()
