import os
import re

def modify_population_sizes(directory):
    """
    Recursively find all files in directory and increase size values by 15%
    """
    # Pattern to match "size = number"
    pattern = re.compile(r'(size\s*=\s*)(\d+)')
    
    # Walk through all files in directory
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            
            # Read the file content
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                # Function to increase number by 15%
                def increase_size(match):
                    prefix = match.group(1)  # "size = "
                    number = int(match.group(2))  # the actual number
                    new_number = int(number * 1.15)  # increase by 15%
                    return f"{prefix}{new_number}"
                
                # Replace all size values
                new_content = pattern.sub(increase_size, content)
                
                # Write back to file if changes were made
                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as file:
                        file.write(new_content)
                        print(f"Updated: {filepath}")
                
            except Exception as e:
                print(f"Error processing {filepath}: {str(e)}")

# Example usage
if __name__ == "__main__":
    directory = "1861.7.1"
    if os.path.exists(directory):
        modify_population_sizes(directory)
        print("Processing complete!")
    else:
        print("Directory not found!")