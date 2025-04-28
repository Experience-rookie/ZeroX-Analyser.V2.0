#!/usr/bin/python
# -*- coding: utf-8 -*- 

import time
import sys
import os
import argparse
from detect import *  # Import functions from detect.py

def recursive(path, depth, plain):
    """
    Recursively explores directories to find files and analyze them.
    
    Parameters:
    - path: The starting directory path.
    - depth: The current level of recursion (used to control depth if needed).
    - plain: Flag to control output format (plain text or not).
    """
    try:
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                if file_path.endswith('.php'):  # Adjust the file type as needed
                    analysis(file_path, plain)
    except Exception as e:
        print(f"Error occurred during directory scan: {e}")

if __name__ == "__main__":
    # Set up an argument parser to handle command-line inputs
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', action='store', dest='dir', help="Provide Directory to analyze")
    parser.add_argument('--plain', action='store_true', dest='plain', help="Plain output (without color)")
    results = parser.parse_args()

    # Check if a directory has been specified and proceed with the analysis.
    if results.dir is not None:
        # Check if the provided directory exists
        if not os.path.exists(results.dir):
            print(f"\033[91m[!] Error!! Invalid directory path: {results.dir}\033[0m")
            sys.exit(1)

        """Check if a directory has been specified and proceed with the analysis.
          To browse files recursively, higher threshold"""
        sys.setrecursionlimit(1000000)
        ascii_art = r"""
 __________                 ____  ___    _____                .__                              
\____    /___________  ____\   \/  /   /  _  \   ____ _____  |  | ___.__. ______ ___________  
  /     // __ \_  __ \/  _ \\     /   /  /_\  \ /    \\__  \ |  |<   |  |/  ___// __ \_  __ \ 
 /     /\  ___/|  | \(  <_> )     \  /    |    \   |  \/ __ \|  |_\___  |\___ \\  ___/|  | \/ 
/_______ \___  >__|   \____/___/\  \ \____|__  /___|  (____  /____/ ____/____  >\___  >__|    
        \/   \/                  \_/         \/     \/     \/     \/         \/     \/      
                                          
                                                                    Made By: Anubhav Dhakal | ZeroX Analyser
"""
        print(ascii_art)
        print("\n{}Analyzing '{}' source code{}".format('' if results.plain else '\033[1m', results.dir, '' if results.plain else '\033[0m'))
        time.sleep(5)

        # Check if directory is empty
        if os.path.isdir(results.dir) and not any(os.scandir(results.dir)):
            print(f"\n\033[91m[!] The directory '{results.dir}' is empty. Cannot proceed with the scan.\033[0m")
            sys.exit(1)

        # Check if directory (or file) contains at least one PHP file
        has_php = False
        if os.path.isfile(results.dir) and results.dir.endswith('.php'):
            has_php = True
        elif os.path.isdir(results.dir):
            for root, dirs, files in os.walk(results.dir):
                for file in files:
                    if file.endswith('.php'):
                        has_php = True
                        break
                if has_php:
                    break

        if not has_php:
            print(f"\n\033[91m[!] No PHP files found in the specified path. Skipping scan.\033[0m")
            sys.exit(1)

        # Proceed with scanning
        if os.path.isfile(results.dir):
            analysis(results.dir, results.plain)
        else:
            recursive(results.dir, 0, results.plain)

        # After analysis completes, generate the PDF report if there are scan results
        if scan_results:
            generate_pdf(scan_results, "ZeroXAnalyser_Report.pdf")
    else:
        parser.print_help()
