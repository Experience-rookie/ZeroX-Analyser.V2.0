import os
import re
import math
from indicators import *
from feature import *
from pdfgen import generate_pdf

result_count = 0
result_files = 0

# ANSI color codes
COLOR_RESET = "\033[0m"
COLOR_BOLD_YELLOW = "\033[1;33m"  # Bold Yellow for vulnerability name
COLOR_CYAN = "\033[1;36m"  # Cyan for line number
COLOR_RED = "\033[1;31m"  # Red for code snippet

scan_results = []

def shannon_entropy(data, iterator):
    if not data:
        return 0
    entropy = 0
    for x in iterator:
        p_x = float(data.count(x)) / len(data)
        if p_x > 0:
            entropy += -p_x * math.log(p_x, 2)
    return entropy


def add_vuln_var(payload, plain, path, vuln_content, content, regex_var_detect, line_number):
    global result_count, scan_results  

    # Ensure vuln_content is a string
    if isinstance(vuln_content, list):
        vuln_content = " ".join(vuln_content)  # Convert list to string

    if not plain:
        print("-" * 130)  
        print(f"{COLOR_BOLD_YELLOW}Name            Potential vulnerability found : {payload[1]}{COLOR_RESET}")
        print("-" * 130)
        print(f"{COLOR_CYAN}Line              --> {line_number} in {path}{COLOR_RESET}")
        print(f"{COLOR_RED}Code              {vuln_content.strip()}{COLOR_RESET}")  
        print("-" * 130)
    else:
        print(f"Vulnerability Detected: {payload[1]} at {path}, Line: {line_number}")
        print(f"Vulnerable content: {vuln_content.strip()}")  

    result_count += 1

    # **Append results for PDF generation**
    scan_results.append({
        "path": path,
        "name": payload[1],
        "line_number": line_number,
        "code": vuln_content.strip()
    })


def analysis(path, plain):
    global result_count
    global result_files
    
    result_files += 1  
    with open(path, 'r', encoding='utf-8', errors='replace') as content_file:
        content = content_file.readlines()
        clean_content = clean_source_and_format("".join(content))
        
        credz = ['pass', 'secret', 'token', 'pwd', 'api-key']
        for i, line in enumerate(clean_content.split('\n')):
            content_pure = line.replace(' ', '')
            regex_var_detect = r"\$[\w\s]+\s?=\s?[\"|'].*?[\"|']|define\([\"|'].*?[\"|']\)"
            regex = re.compile(regex_var_detect, re.I)
            matches = regex.findall(content_pure)
            
            for vuln_content in matches:
                if any(cred in vuln_content.lower() for cred in credz):
                    payload = ["", "Hardcoded Credential", []]
                    add_vuln_var(payload, plain, path, vuln_content, clean_content, regex_var_detect, i + 1)
        
        regex_var_detect = r".*?=\s?[\"|'].*?[\"|'].*?"
        regex = re.compile(regex_var_detect, re.I)
        BASE64_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
        HEX_CHARS = "1234567890abcdefABCDEF"
        
        for i, line in enumerate(clean_content.split('\n')):
            content_pure = line.replace(' ', '')
            matches = regex.findall(content_pure)
            
            for vuln_content in matches:
                payload = ["", "High Entropy String", []]
                if shannon_entropy(vuln_content, BASE64_CHARS) >= 4.1 or \
                   shannon_entropy(vuln_content, HEX_CHARS) >= 2.5:
                    add_vuln_var(payload, plain, path, vuln_content, clean_content, regex_var_detect, i + 1)
                    
        for i, line in enumerate(clean_content.split('\n')):
            for payload in payloads:
                regex = re.compile(payload[0] + regex_indicators)
                matches = regex.findall(line.replace(" ", "(PLACEHOLDER"))

                for vuln_content in matches:
                    vuln_content = list(vuln_content)
                    for j in range(len(vuln_content)):
                        vuln_content[j] = vuln_content[j].replace("(PLACEHOLDER", " ")
                        vuln_content[j] = vuln_content[j].replace("PLACEHOLDER", "")
                    
                    occurence = 0
                    if not check_protection(payload[2], vuln_content):
                        declaration_text, line_text = "", ""
                        sentence = "".join(vuln_content)
                        regex = re.compile(regex_indicators[2:-2])
                        
                        for vulnerable_var in regex.findall(sentence):
                            false_positive = False
                            occurence += 1

                            if not check_exception(vulnerable_var[1]):
                                false_positive, declaration_text, line_text = check_declaration(clean_content, vulnerable_var[1], path)
                            
                            is_protected = check_protection(payload[2], declaration_text)
                            false_positive = is_protected if is_protected else false_positive

                            line_vuln = i + 1

                            if "$" not in declaration_text.replace(vulnerable_var[1], ''):
                                false_positive = True

                            if not false_positive:
                                result_count += 1
                                add_vuln_var(payload, plain, path, vuln_content, clean_content, regex_var_detect, line_vuln)

# Generate PDF after analysis
if scan_results:
    generate_pdf(scan_results)
