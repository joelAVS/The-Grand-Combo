import os
import re

# Function to find date entries in a file
def find_date_entries(lines):
    date_entries = {}
    date_pattern = re.compile(r"^(\d{4}\.\d{1,2}\.\d{1,2}) = \{")
    current_date = None
    entry_lines = []

    for line in lines:
        stripped_line = line.strip()
        date_match = date_pattern.match(stripped_line)

        if date_match:
            # If a new date entry is found, save the previous one
            if current_date:
                date_entries[current_date] = entry_lines
            # Start a new date entry
            current_date = date_match.group(1)
            entry_lines = [line]
        elif current_date:
            # Collect lines for the current date entry
            entry_lines.append(line)

    # Save the last date entry
    if current_date:
        date_entries[current_date] = entry_lines

    return date_entries

# Function to process a single file
def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Find all date entries in the file
    date_entries = find_date_entries(lines)

    # Check which date entries exist
    required_dates = ["1815.8.1", "1836.1.1", "1861.7.1"]
    existing_dates = sorted(date_entries.keys())
    missing_dates = [date for date in required_dates if date not in existing_dates]

    # If all required dates exist, do nothing
    if not missing_dates:
        return

    # Determine the latest existing date to use for copying
    latest_date = existing_dates[-1] if existing_dates else None

    # Create new date entries for missing dates
    new_entries = []
    for missing_date in missing_dates:
        if latest_date:
            # Copy the latest existing entry and update its date
            copied_entry = [line.replace(latest_date, missing_date, 1) if latest_date in line else line
                            for line in date_entries[latest_date]]
            new_entries.extend(copied_entry)

    # Append the new entries to the file content
    lines.extend(new_entries)

    # Write the updated content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)

# Function to process all files in a folder and its subfolders
def process_folder(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".txt"):  # Assuming the files have a .txt extension
                process_file(os.path.join(root, file))

# Specify the folder path containing the files
folder_path = "provinces"
process_folder(folder_path)
