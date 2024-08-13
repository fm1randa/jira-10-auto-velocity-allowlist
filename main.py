import tkinter as tk
from gui import browse_log_file, browse_plugin_file, on_toggle_watch

root = tk.Tk()
root.title("Log File Watcher")

log_file_var = tk.StringVar()
plugin_file_var = tk.StringVar()
watching = tk.BooleanVar(value=False)

tk.Label(root, text="Log File:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
tk.Entry(root, textvariable=log_file_var, width=50).grid(row=0, column=1, padx=5, pady=5)
tk.Button(root, text="Browse...", command=lambda: browse_log_file(log_file_var)).grid(row=0, column=2, padx=5, pady=5)

tk.Label(root, text="Plugin XML File:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
tk.Entry(root, textvariable=plugin_file_var, width=50).grid(row=1, column=1, padx=5, pady=5)
tk.Button(root, text="Browse...", command=lambda: browse_plugin_file(plugin_file_var)).grid(row=1, column=2, padx=5, pady=5)

toggle_button = tk.Button(root, text="Start Watching", command=lambda: on_toggle_watch(log_file_var, plugin_file_var, toggle_button, watching))
toggle_button.grid(row=2, column=1, padx=5, pady=20)

root.mainloop()
