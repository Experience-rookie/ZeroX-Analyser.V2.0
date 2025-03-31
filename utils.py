def clean_source_and_format(content):
    """
    Cleans and formats the source code to prepare for analysis.
    
    Parameters:
    - content: The raw source code content.
    
    Returns:
    - The cleaned and formatted source code as a string.
    """
    # Clean up unnecessary line breaks, excessive spaces, or anything that might interfere with vulnerability detection
    content = content.replace('\r', '').replace('\n', ' ')  # Removing line breaks and converting to single line for easier regex
    return content

def add_vuln_var(payload, plain, path, vuln_content, content, regex_var_detect):
    """
    Adds vulnerability information to the result.
    
    Parameters:
    - payload: The payload to add the vulnerability info.
    - plain: Boolean indicating whether the output is plain.
    - path: The path to the file.
    - vuln_content: The content containing vulnerability.
    - content: The full content of the file.
    - regex_var_detect: Regular expression used for detection.
    """
    global result_count  # Ensuring result_count is used globally

    result_count += 1  # Increment result count for every detected vulnerability

    # Get the line number of the detected vulnerability in the full content (this assumes vuln_content is part of the line)
    lines = content.split('\n')
    line_number = None

    # Find the line where the vulnerability was detected
    for i, line in enumerate(lines):
        if vuln_content in line:
            line_number = i + 1  # Line numbers in content start from 1
            break

    # Print information about the detected vulnerability
    print(f"Vulnerable Content: {vuln_content.strip()}")
    print(f"File Path: {path}")
    print(f"Vulnerability Type: {payload[1]}")

    # Output in plain or formatted style
    if not plain:
        print(f"Detected at Line: {line_number}")  # Line number where vulnerability was found
    else:
        print(f"Detected at Line: {vuln_content}")

