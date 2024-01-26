import subprocess
import re
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

app = "Ableton Live 11 Lite"
restart_app = True
dir_path = "/Users/matt/Library/Preferences/Ableton/Live 11.3.21"
file_path = f"{dir_path}/Log.txt"
tag = "RemoteScriptError:"
lines_old = []


class Logger(FileSystemEventHandler):
    # Log events on change
    def handle_change(self, event):
        is_file = event.src_path == file_path
        if is_file:
            print("🟢")
            with open(file_path, "r") as f:
                lines = f.readlines()
                for line in lines:
                    # If the line contains the tag and is not already in the list
                    if tag in line and line not in lines_old:
                        lines_old.append(line)
                        error_match = re.search(
                            f"(?<={tag})(.*)", line)
                        error = error_match.group(0).strip()
                        print(error)

    def on_created(self, event):
        self.handle_change(event)

    def on_modified(self, event):
        self.handle_change(event)


def start():
    # Clear log file, print directory
    open(file_path, 'w').close()
    print("🚀")
    print(file_path)

    # Restart Live
    if restart_app:
        subprocess.call(
            ['osascript', '-e', f'tell application "{app}" to quit saving no'])
        time.sleep(2)
        subprocess.call(
            ['osascript', '-e', f'tell application "{app}" to open'])

    # Start logging
    if __name__ == "__main__":

        # Start changes event
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')

        event_handler = Logger()
        observer = Observer()
        observer.schedule(event_handler, dir_path, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()


start()
