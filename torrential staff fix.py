import re

def patch_torrential_staff_full(input_file, output_file):
    # Read the file in binary mode
    with open(input_file, 'rb') as infile:
        content = infile.read()

    original_byte_size = len(content)
    print(f"Original byte size: {original_byte_size}")

    # 1. Locate the Torrential Staff block
    staff_start_marker = b'<Object id="Torrential Staff" type="0x51a7"'
    staff_index = content.find(staff_start_marker)
    
    if staff_index == -1:
        print("Error: Could not find 'Torrential Staff' in the file.")
        return

    # Find the end of this specific Object block
    staff_end_index = content.find(b'</Object>', staff_index) + len(b'</Object>')
    staff_block = content[staff_index:staff_end_index]

    # 2. Generic function to replace tag content while maintaining length
    def maintain_length(match, new_val):
        original_content = match.group(1)
        # If the new value is longer than the original, we have to truncate (unlikely here)
        if len(new_val) > len(original_content):
            return match.group(0)[:len(match.group(0))] 
        
        # Pad with spaces to match original length exactly
        padded_val = new_val + (b' ' * (len(original_content) - len(new_val)))
        
        # Reconstruct the tag with the same boundaries
        tag_name = match.group(0).split(b'>')[0][1:]
        return b'<' + tag_name + b'>' + padded_val + b'</' + tag_name + b'>'

    # 3. Apply replacements to the extracted block
    # Modify PosOffset to 0,0
    pos_pattern = rb'<PosOffset>(.*?)</PosOffset>'
    modified_block = re.sub(pos_pattern, lambda m: maintain_length(m, b"0,0"), staff_block)
    
    # Modify DefaultAngle to 0
    angle_pattern = rb'<DefaultAngle>(.*?)</DefaultAngle>'
    modified_block = re.sub(angle_pattern, lambda m: maintain_length(m, b"0"), modified_block)

    # 4. Reassemble and Verify
    content_modified = content[:staff_index] + modified_block + content[staff_end_index:]

    new_byte_size = len(content_modified)
    print(f"New byte size:      {new_byte_size}")

    if new_byte_size != original_byte_size:
        print(f"CRITICAL ERROR: Size mismatch detected! ({new_byte_size} vs {original_byte_size})")
    else:
        with open(output_file, 'wb') as outfile:
            outfile.write(content_modified)
        print("Successfully patched PosOffset and DefaultAngle for Torrential Staff.")

# Usage
patch_torrential_staff_full('resources.assets', 'resources_modified.assets')