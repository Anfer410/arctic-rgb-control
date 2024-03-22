import serial


def rgb2hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(rgb['r'], rgb['g'], rgb['b'])


def hex2rgb(hex):
    hex = hex.lstrip('#')
    rgb = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
    return dict(r=rgb[0], g=rgb[1], b=rgb[2], a=1)


def dict2tuple(color):
    return (color['r'], color['g'], color['b'])


def open_port(port='/dev/ttyUSB0'):
    serial_port = serial.Serial(
        port=port,  # Change '/dev/ttyUSB0' to your CH340 board port
        baudrate=250000,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        dsrdtr=True
        )

    return serial_port


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