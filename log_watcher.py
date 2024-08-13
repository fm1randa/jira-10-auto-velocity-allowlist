import re
import time
import threading
from colorama import Fore
from xml_updater import scan_log_file, update_plugin_xml

def watch_log_file(log_file_path, plugin_xml_path):
    with open(log_file_path, 'r') as log_file:
        log_file.seek(0, 2)
        print(f"{Fore.CYAN}Started watching the log file: {log_file_path}")

        while True:
            line = log_file.readline()
            if not line:
                time.sleep(1)
                continue

            method_name = extract_method_name(line)
            if method_name:
                print(f"{Fore.GREEN}New method found while watching: {method_name}")
                update_plugin_xml(method_name, plugin_xml_path)

def extract_method_name(line):
    log_entry_pattern = re.compile(
        r'.*Method needs allowlisting: ([\w\.]+#[\w\.]+\([\w\. ]+\))'
    )
    match = log_entry_pattern.match(line)
    if match:
        return match.group(1)
    return None

def start_watching(log_file_path, plugin_xml_path):
    scan_log_file(log_file_path, plugin_xml_path)
    thread = threading.Thread(target=watch_log_file, args=(log_file_path, plugin_xml_path))
    thread.daemon = True
    thread.start()
    print("Finished scanning and started watching the log file.")
