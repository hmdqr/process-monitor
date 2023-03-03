# Process Monitor

Process Monitor is a Python script to monitor running processes and start them automatically if they crash or stop running. It can also send notifications to a Telegram chat when processes are restarted.

## Note: 

This app was modified using Chat Gpt from OpenAI. While I tried my best to implement the suggested changes correctly, there may still be bugs or mistakes in the code. If you encounter any issues or have any feedback, please let me know.

## Installation

1. Clone the repository or download the ZIP file.
2. Create a `config.ini` file in the same directory as `process_watcher.py` using the example file `config-sample.ini
3. Add your processes to the `[Processes]` section of the `config.ini` file.
3. Add your Telegram chat ID and bot token to the `[Telegram]` section of the `config.ini` file (optional).

## Usage

1. Start the script using `python process_watcher.py`.
2. The script will check if each process is running every few seconds (defined in the `interval` setting in the `config.ini` file).
3. If a process is not running, the script will start it using the `os.startfile()` function on Windows or the `os.system()` function on Unix-like systems.
4. If the `update.txt` file exists in the same directory as the script, the script will not start any processes. This can be used to prevent the script from starting processes during updates.

## Configuration

The `config.ini` file is used to configure the script. Here are the available options:

### Processes

This section should contain a list of all the processes you want to monitor. Each item in the list should be a process name (as it appears in the task manager) and a process path (the path to the executable file).

Example:
`
[Processes]
my_process = C:\path\to\my\process.exe
`

### Telegram (optional)

If you want to receive notifications via Telegram, you will need to add your chat ID and bot token to the `Telegram` section of the `config.ini` file.

Example:

`
[Telegram]
chat_id = YOUR_CHAT_ID
token = YOUR_BOT_TOKEN
`


### Settings

This section contains various settings for the script.

- `interval`: The interval in seconds between checks for running processes.
- `file`: The name of the file to check for updates. If found, the script will not start any processes.

Example:


`
[Settings]
interval = 10
file = update.txt
`


## Q&A

### Why does the app sometimes run processes more than once, even when they are already running?

This is a known issue with the current version of the app. 
We are still investigating the cause of this behavior, and working on a solution. 
Please keep in mind that this app is still in development, and we appreciate your patience as we work to improve its functionality. 

### What is this app?

This app is a Python script that monitors a list of processes and starts them if they are not running. It can also notify you via Telegram if a process is started or if there is an error.

### How do I use this app?

First, you need to install Python 3 and the `psutil` and `requests` modules. Then, create a configuration file named `config.ini` in the same directory as the script. In the configuration file, list the processes you want to monitor, along with their paths and update files. You can also configure the interval between checks and your Telegram bot credentials for notifications.

### Can I use this app on Windows and Linux?

Yes, it should work on windows and linux. 

### How do I stop the script?

On Windows, press the `q` key. On Linux, type `exit` and press `Enter`.

### Can I add multiple users with their own processes to monitor?

Yes, you can create a separate configuration file for each user, and list them in the same directory as the script with the extension `.ini`. The script will load all configuration files in the directory.

### Is this app ready for production use?

No! This app is still under development and has not been thoroughly tested. Use it at your own risk.

## Contributing

This script is still under development and may contain bugs or errors. Contributions are welcome! Please create a pull request or open an issue if you find any bugs or have any suggestions.
