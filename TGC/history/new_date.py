import os
import re

# Define the folder to scan
folder_path = "/provinces/"

# Regex pattern to find date entries like '1836.1.1 = { ... }'
date_pattern = re.compile(r"(\d{4}\.\d{1,2}\.\d{1,2})\s*=\s*\{(.*?)\}", re.DOTALL)

# Define the target date to duplicate entries to
target_date = "1861.7.1"

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Find all matches for the date pattern
    matches = date_pattern.findall(content)

    # Generate new entries
    for match in matches:
        original_date = match[0]
        content_block = match[1]

        # Construct the duplicated block with the target date
        new_block = f"{target_date} = {{ {content_block} }}"

        # Insert the new block after the original block
        content = content.replace(
            f"{original_date} = {{ {content_block} }}",
            f"{original_date} = {{ {content_block} }}\n{new_block}"
        )

    # Save the updated content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def process_folder(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".txt"):  # Adjust the file extension as needed
                file_path = os.path.join(root, file)
                process_file(file_path)

# Process the folder
process_folder(folder_path)

print("Duplication complete.")
