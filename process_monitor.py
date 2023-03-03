import os
import time
import logging
import psutil
import requests
import sys
import configparser

if os.name == 'nt': # for Windows
    import msvcrt
else: # for Linux and Mac
    import select

logging.basicConfig(
    filename='monitor.log',
    level=logging.INFO,
    format='%(asctime)s %(message)s'
)

# Get a list of all configuration files in the current directory
config_files = [f for f in os.listdir('.') if f.endswith('.ini')]

# Load each configuration file into a dictionary
config = {}
for config_file in config_files:
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    user = os.path.splitext(config_file)[0]
    config[user] = config_parser

def check_update_file(file_path):
    return os.path.exists(file_path)

def check_process(process_name):
    for process in psutil.process_iter():
        try:
            if process.name() == process_name:
                return True
        except psutil.NoSuchProcess:
            pass
    return False

def start_process(process_path):
    try:
        if sys.platform == 'win32':
            os.startfile(process_path)
        else:
            os.system(process_path)
        logging.info(f'Process started: {process_path}')
    except Exception as e:
        logging.error(f'Could not start process: {process_path}, {e}')
        send_telegram_message(f'Could not start process: {process_path}, {e}')

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
    except requests.exceptions.RequestException as e:
        logging.error(f'Could not send Telegram notification: {e}')

process_status = {}
while True:
    for user in config:
        processes = config[user]['Processes']
        settings = config[user]['Settings']
        update_file = settings['file']
        if not check_update_file(update_file):
            for process_name, process_path in processes.items():
                if process_name not in process_status or not check_process(process_name):
                    process_status[process_name] = True
                    start_process(process_path)
        else:
            process_status = {}
        time.sleep(int(settings['interval']))
    
    # Check for user input
    if os.name == 'nt': # for Windows
        if msvcrt.kbhit() and msvcrt.getch() == b'q':
            break
    else: # for Linux and Mac
        if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
            input_string = sys.stdin.readline().strip()
            if input_string == "exit":
                break
