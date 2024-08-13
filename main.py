import re
import time
import tkinter as tk
from tkinter import filedialog, messagebox
import threading

# Define the regex pattern to match the log entries
log_entry_pattern = re.compile(
    r'.*Method needs allowlisting: ([\w\.]+#[\w\.]+\([\w\. ]+\))'
)

def update_plugin_xml(method_name, plugin_xml_path):
    """Update the atlassian-plugin.xml file with the new method if not already present."""
    with open(plugin_xml_path, 'r') as f:
        lines = f.readlines()

    start_idx = -1
    end_idx = -1
    inside_allowlist = False
    allowlist_content = []
    methods = []

    # Locate the velocity-allowlist section and capture its content
    for idx, line in enumerate(lines):
        if '<velocity-allowlist' in line:
            inside_allowlist = True
            start_idx = idx
            allowlist_content.append(line)
        elif '</velocity-allowlist>' in line:
            end_idx = idx
            allowlist_content.append(line)
            break
        elif inside_allowlist:
            allowlist_content.append(line)
            if '<method>' in line:
                method = line.strip()[len('<method>'):-len('</method>')]
                methods.append(method)

    if start_idx == -1 or end_idx == -1:
        print("Could not locate the velocity-allowlist section.")
        return

    if method_name not in methods:
        methods.append(method_name)
        methods.sort()

        # Rebuild the method section with one method per line
        method_lines = [f'        <method>{m}</method>\n' for m in methods]

        # Handle the case where no methods exist initially
        if not methods[:-1]:  # If there were no previous methods
            new_allowlist_content = allowlist_content[:-1] + method_lines + [allowlist_content[-1]]
        else:
            # Replace the old method lines with the new sorted method lines
            new_allowlist_content = []
            for line in allowlist_content:
                if '<method>' not in line:
                    new_allowlist_content.append(line)
                else:
                    break

            new_allowlist_content.extend(method_lines)
            new_allowlist_content.append('    </velocity-allowlist>\n')

        # Reconstruct the full content
        new_lines = lines[:start_idx] + new_allowlist_content + lines[end_idx+1:]

        # Write the updated content back to the XML file
        with open(plugin_xml_path, 'w') as f:
            f.writelines(new_lines)

        print(f"Inserted new method: {method_name}")
    else:
        print(f"Method already exists: {method_name}")

def watch_log_file(log_file_path, plugin_xml_path):
    """Watch the log file for matching entries and update the XML file."""
    with open(log_file_path, 'r') as log_file:
        log_file.seek(0, 2)  # Move to the end of the file

        while True:
            line = log_file.readline()
            if not line:
                time.sleep(1)  # Sleep briefly before trying to read more lines
                continue

            match = log_entry_pattern.match(line)
            if match:
                method_name = match.group(1)
                update_plugin_xml(method_name, plugin_xml_path)

def start_watching(log_file_path, plugin_xml_path):
    """Start a new thread to watch the log file."""
    thread = threading.Thread(target=watch_log_file, args=(log_file_path, plugin_xml_path))
    thread.daemon = True
    thread.start()
    messagebox.showinfo("Watching", "Started watching the log file.")

def browse_log_file():
    """Open a file dialog to select the log file."""
    log_file_path = filedialog.askopenfilename(title="Select Log File")
    log_file_var.set(log_file_path)

def browse_plugin_file():
    """Open a file dialog to select the atlassian-plugin.xml file."""
    plugin_xml_path = filedialog.askopenfilename(title="Select Plugin XML File")
    plugin_file_var.set(plugin_xml_path)

def on_start():
    """Start watching the log file."""
    log_file_path = log_file_var.get()
    plugin_xml_path = plugin_file_var.get()

    if not log_file_path or not plugin_xml_path:
        messagebox.showerror("Error", "Please select both files.")
        return

    start_watching(log_file_path, plugin_xml_path)

# Create the main window
root = tk.Tk()
root.title("Log File Watcher")

# Variables to hold the selected file paths
log_file_var = tk.StringVar()
plugin_file_var = tk.StringVar()

# Create and place the UI elements
tk.Label(root, text="Log File:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
tk.Entry(root, textvariable=log_file_var, width=50).grid(row=0, column=1, padx=5, pady=5)
tk.Button(root, text="Browse...", command=browse_log_file).grid(row=0, column=2, padx=5, pady=5)

tk.Label(root, text="Plugin XML File:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
tk.Entry(root, textvariable=plugin_file_var, width=50).grid(row=1, column=1, padx=5, pady=5)
tk.Button(root, text="Browse...", command=browse_plugin_file).grid(row=1, column=2, padx=5, pady=5)

tk.Button(root, text="Start Watching", command=on_start).grid(row=2, column=1, padx=5, pady=20)

# Start the Tkinter main loop
root.mainloop()
