from tkinter import filedialog, messagebox
from log_watcher import start_watching, stop_watching

def browse_log_file(log_file_var):
    log_file_path = filedialog.askopenfilename(title="Select Log File")
    log_file_var.set(log_file_path)

def browse_plugin_file(plugin_file_var):
    plugin_xml_path = filedialog.askopenfilename(title="Select Plugin XML File")
    plugin_file_var.set(plugin_xml_path)

def on_toggle_watch(log_file_var, plugin_file_var, toggle_button, watching):
    log_file_path = log_file_var.get()
    plugin_xml_path = plugin_file_var.get()

    if not log_file_path or not plugin_xml_path:
        messagebox.showerror("Error", "Please select both files.")
        return

    if not watching.get():
        start_watching(log_file_path, plugin_xml_path)
        watching.set(True)
        toggle_button.config(text="Stop Watching")
    else:
        stop_watching()
        watching.set(False)
        toggle_button.config(text="Start Watching")
