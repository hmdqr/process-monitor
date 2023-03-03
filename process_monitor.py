import os
import time
import logging
import psutil
import requests
import sys
import configparser

if os.name == 'nt':
    import msvcrt
else:
    import select

logging.basicConfig(filename='monitor.log', level=logging.INFO, format='%(asctime)s %(message)s')

config_files = [f for f in os.listdir('.') if f.endswith('.ini')]

config = {}
for config_file in config_files:
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    user = os.path.splitext(config_file)[0]
    config[user] = config_parser

def check_update_file(file_path):
    return os.path.exists(file_path)

def check_process(process_path):
    for process in psutil.process_iter():
        try:
            if process.name() == os.path.basename(process_path) and process.exe() == process_path:
                return True
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            pass
    return False

def start_process(process_path):
    try:
        if sys.platform == 'win32':
            os.startfile(process_path)
        else:
            os.system(process_path)
        logging.info(f'Process started: {process_path}')
    except Exception as error:
        logging.error(f'Could not start process: {process_path}, {error}')
        send_telegram_message(f'Could not start process: {process_path}, {error}')

def send_telegram_message(message, user):
    telegram = config[user]['Telegram']
    url = f'https://api.telegram.org/bot{telegram["token"]}/sendMessage'
    data = {
        'chat_id': telegram['chat_id'],
        'text': message
    }
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        logging.info(f'Telegram notification sent: {message}')
    except requests.exceptions.RequestException as error:
        logging.error(f'Could not send Telegram notification: {error}')

process_status = {}
while True:
    for user in config:
        processes = config[user]['Processes']
        settings = config[user]['Settings']
        update_file = settings['file']
        if not check_update_file(update_file):
            for process_name, process_path in processes.items():
                if process_name not in process_status or not process_status[process_name]:
                    if check_process(process_path):
                        process_status[process_name] = True
                    else:
                        start_process(process_path)
                        process_status[process_name] = True
                else:
                    logging.info(f'Process already running: {process_name}')
        else:
            process_status = {}
        start_time = time.monotonic()
        while time.monotonic() < start_time + int(settings['interval']):
            if os.name == 'nt' and msvcrt.kbhit() and msvcrt.getch() == b'q':
                sys.exit()
            elif os.name != 'nt' and select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                input_string = sys.stdin.readline().strip()
                if input_string == "exit":
                    sys.exit()
