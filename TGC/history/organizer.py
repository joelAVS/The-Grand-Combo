import os
import re

def update_slave_entries(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Check if "is_slave = yes" exists in the file
    if not any("is_slave = yes" in line for line in lines):
        return  # Skip this file if "is_slave = yes" is not found

    # Regex to match the 1861.7.1 entry with varying properties
    pattern = re.compile(
        r"(1861\.7\.1\s*=\s*\{\s*(?:owner\s*=\s*USA\s*)?(?:controller\s*=\s*USA\s*)?(?:add_core\s*=\s*USA\s*)?\s*\})",
        re.DOTALL
    )

    # Join lines for easier regex matching
    content = "".join(lines)

    # Replace the 1861.7.1 entry for USA with CSA
    replacement = (
        "1861.7.1 = {\n"
        "    owner = CSA\n"
        "    controller = CSA\n"
        "    add_core = CSA\n"
        "}"
    )
    updated_content = pattern.sub(replacement, content)

    # Write the updated content back to the file if changes were made
    if content != updated_content:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)


def process_folder(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".txt"):  # Assuming the files have a .txt extension
                update_slave_entries(os.path.join(root, file))


# Specify the folder path containing the files
folder_path = "provinces"  # Replace with your folder path
process_folder(folder_path)
