# Jira 10 Auto Velocity Allowlist

This project is a Python-based tool for monitoring a specified log file to detect method entries and update an `atlassian-plugin.xml` file with these methods. The tool provides a graphical interface for selecting files and offers real-time feedback in the terminal.

## Features

- **Real-time Log Monitoring**: Watches a specified log file and identifies method entries that need allowlisting.
- **XML File Updater**: Automatically updates the `atlassian-plugin.xml` file with the detected methods.
- **Graphical User Interface**: Provides an easy-to-use interface for selecting the log and XML files.
- **Toggle Watch**: Allows the user to start and stop watching the log file through a single button click.
- **Feedback Messages**: Real-time feedback in the terminal with color-coded messages for better readability.

## Installation

1. **Clone the repository**:
   ```
   git clone https://github.com/fm1randa/jira-10-auto-velocity-allowlist.git
   cd jira-10-auto-velocity-allowlist
   ```

2. **Create and activate a virtual environment (optional but recommended)**:
   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. **Run the application**:
   ```
   python main.py
   ```

2. **Select the Log File**:
   - Click the "Browse..." button next to "Log File" and choose the `atlassian-jira.log` file you want to monitor.

3. **Select the Plugin XML File**:
   - Click the "Browse..." button next to "Plugin XML File" and choose the `atlassian-plugin.xml` file that will be updated.

4. **Start Watching**:
   - Click the "Start Watching" button to begin monitoring the log file. The button will toggle to "Stop Watching" when the process starts.

5. **Stop Watching**:
   - To stop monitoring, click the "Stop Watching" button.

## Terminal Feedback

The terminal provides real-time feedback while the tool is running:

- **Cyan Messages**: Informational messages (e.g., starting or stopping the watch).
- **Green Messages**: Successful operations (e.g., new methods inserted into the XML file).
- **Yellow Messages**: Warnings (e.g., a method that already exists in the XML file).
- **Red Messages**: Errors (e.g., unable to locate the velocity-allowlist section in the XML file).

## Screenshot

![image](https://github.com/user-attachments/assets/3bc3f358-05ef-43ab-a475-5581e239f6ff)


## File Structure

```
jira-10-auto-velocity-allowlist/
│
├── main.py              # Entry point for the application
├── gui.py               # Handles the graphical user interface logic
├── log_watcher.py       # Contains logic for scanning and watching the log file
└── xml_updater.py       # Handles updating the atlassian-plugin.xml file
```

## Requirements

- Python 3.7 or higher
- `colorama` for colored terminal output
- `tkinter` for the graphical user interface

## License

This project is licensed under the MIT License.
