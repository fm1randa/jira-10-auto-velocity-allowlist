import time
import threading
import re
from colorama import Fore
from xml_updater import scan_log_file, update_plugin_xml

watching_thread = None
stop_event = threading.Event()
processed_methods = set()

def watch_log_file(log_file_path, plugin_xml_path):
    with open(log_file_path, 'r') as log_file:
        log_file.seek(0, 2)
        print(f"{Fore.CYAN}Started watching the log file: {log_file_path}")

        while not stop_event.is_set():
            line = log_file.readline()
            if not line:
                time.sleep(1)
                continue

            method_name = extract_method_name(line)
            if method_name and method_name not in processed_methods:
                print(f"{Fore.GREEN}New method found while watching: {method_name}")
                update_plugin_xml(method_name, plugin_xml_path)
                processed_methods.add(method_name)

        print(f"{Fore.YELLOW}Stopped watching the log file.")

def extract_method_name(line):
    log_entry_pattern = re.compile(
        r'.*Method needs allowlisting: ([\w\.]+#[\w\.]+\([\w\. ]+\))'
    )
    match = log_entry_pattern.match(line)
    if match:
        return match.group(1)
    return None

def start_watching(log_file_path, plugin_xml_path):
    global watching_thread, stop_event, processed_methods
    processed_methods = scan_log_file(log_file_path, plugin_xml_path)
    stop_event.clear()
    watching_thread = threading.Thread(target=watch_log_file, args=(log_file_path, plugin_xml_path))
    watching_thread.daemon = True
    watching_thread.start()
    print("Finished scanning and started watching the log file.")

def stop_watching():
    global watching_thread, stop_event
    if watching_thread and watching_thread.is_alive():
        stop_event.set()
        watching_thread.join()
    print("Watching has been stopped.")
