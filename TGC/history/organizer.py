import os
import re

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Variables to track modifications
    modified = False
    owner_line = None
    controller_line = None
    inside_date_entry = False  # Tracks if we're inside a date entry

    # Process lines
    new_lines = []
    for line in lines:
        stripped_line = line.strip()

        # Check if entering a date entry
        if re.match(r"^\d{4}\.\d{1,2}\.\d{1,2} = \{", stripped_line):
            inside_date_entry = True

        # Check if exiting a date entry
        if inside_date_entry and stripped_line == "}":
            inside_date_entry = False

        # Capture `owner` and `controller` lines only if they are not inside a date entry
        if not inside_date_entry:
            if stripped_line.startswith("owner =") and not owner_line:
                owner_line = stripped_line
                modified = True
                continue
            elif stripped_line.startswith("controller =") and not controller_line:
                controller_line = stripped_line
                modified = True
                continue

        # Add the current line to the output
        new_lines.append(line)

    # Add the new `1815.8.1` entry if `owner` or `controller` were found
    if modified:
        new_entry = ["\n1815.8.1 = {\n"]
        if owner_line:
            new_entry.append(f"    {owner_line}\n")
        if controller_line:
            new_entry.append(f"    {controller_line}\n")
        new_entry.append("}\n")

        # Insert the new entry at the top of the file (before any other entries)
        # Or just before the first date-based block like `1836.1.1 = {`
        insert_index = next(
            (i for i, line in enumerate(new_lines) if re.match(r"^\d{4}\.\d{1,2}\.\d{1,2} = \{", line.strip())),
            len(new_lines)
        )
        new_lines = new_lines[:insert_index] + new_entry + new_lines[insert_index:]

    # Write back to the file if modifications were made
    if modified:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(new_lines)


def process_folder(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path.endswith(".txt"):  # Assuming the files have a .txt extension
                process_file(file_path)


# Specify the folder path containing the files
folder_path = "provinces"
process_folder(folder_path)
