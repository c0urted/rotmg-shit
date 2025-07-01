import re

def replace_flow_dx_dy_binary(input_file, output_file):
    # Read the file in binary mode
    with open(input_file, 'rb') as infile:
        content = infile.read()

    original_byte_size = len(content)
    print(f"Original byte size: {original_byte_size}")

    # Define regex pattern for dx="..." and dy="..." inside Flow Animate tags in bytes
    pattern_dx = rb'dx="([-+]?\d*\.?\d+)"'
    pattern_dy = rb'dy="([-+]?\d*\.?\d+)"'
    
    # Function to replace digits with 0's in the matched bytes
    def replace_value_binary(match):
        original_value = match.group(1)
        # Replace all digits with '0' in bytes, but preserve '-' and '.'
        zeroed_value = bytearray(b''.join(b'0' if chr(c).isdigit() else bytes([c]) for c in original_value))
        return match.group(0).replace(original_value, zeroed_value)

    # Only replace dx and dy values inside Animate tags with Flow
    content_modified = re.sub(pattern_dx, replace_value_binary, content)
    content_modified = re.sub(pattern_dy, replace_value_binary, content_modified)

    new_byte_size = len(content_modified)
    print(f"New byte size: {new_byte_size}")

    # Check if the new size matches the original
    if new_byte_size != original_byte_size:
        print(f"Error: Modified file size ({new_byte_size}) differs from original ({original_byte_size})!")
    else:
        # Write the modified binary content to the output file
        with open(output_file, 'wb') as outfile:
            outfile.write(content_modified)
        print("File modified successfully without changing the byte size.")

# Usage
input_file = 'resources.assets'  # Replace with the asset file
output_file = 'output.assets'
replace_flow_dx_dy_binary(input_file, output_file)