import re
from colorama import Fore

def update_plugin_xml(method_name, plugin_xml_path):
    with open(plugin_xml_path, 'r') as f:
        lines = f.readlines()

    start_idx = -1
    end_idx = -1
    inside_allowlist = False
    allowlist_content = []
    methods = []

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
        print(f"{Fore.RED}Could not locate the velocity-allowlist section.")
        return

    if method_name not in methods:
        methods.append(method_name)
        methods.sort()

        method_lines = [f'        <method>{m}</method>\n' for m in methods]

        if not methods[:-1]:
            new_allowlist_content = allowlist_content[:-1] + method_lines + [allowlist_content[-1]]
        else:
            new_allowlist_content = []
            for line in allowlist_content:
                if '<method>' not in line:
                    new_allowlist_content.append(line)
                else:
                    break

            new_allowlist_content.extend(method_lines)
            new_allowlist_content.append('    </velocity-allowlist>\n')

        new_lines = lines[:start_idx] + new_allowlist_content + lines[end_idx+1:]

        with open(plugin_xml_path, 'w') as f:
            f.writelines(new_lines)

        print(f"{Fore.GREEN}Inserted new method: {method_name}")
    else:
        print(f"{Fore.YELLOW}Method already exists: {method_name}")

def scan_log_file(log_file_path, plugin_xml_path):
    print(f"{Fore.CYAN}Scanning the log file: {log_file_path}")
    with open(log_file_path, 'r') as log_file:
        for line in log_file:
            method_name = extract_method_name(line)
            if method_name:
                update_plugin_xml(method_name, plugin_xml_path)
    print(f"{Fore.CYAN}Finished scanning the log file.")

def extract_method_name(line):
    log_entry_pattern = re.compile(
        r'.*Method needs allowlisting: ([\w\.]+#[\w\.]+\([\w\. ]+\))'
    )
    match = log_entry_pattern.match(line)
    if match:
        return match.group(1)
    return None
