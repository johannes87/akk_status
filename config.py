import configparser

def get_bar_raspberry_host_port():
    config = configparser.ConfigParser()
    config.read("net.ini")
    host = config['DEFAULT']['BarRaspberryHost']
    port = int(config['DEFAULT']['BarRaspberryPort'])
    return (host, port)
