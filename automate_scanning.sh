#!/usr/bin/env bash

echo "Generating report"
mkdir Report 2> /dev/null
python3 "C:/Users/Anubhav Dhakal/OneDrive/Desktop/ZeroXAnalyser/zeroXanalyser.py" --dir "C:/Users/Anubhav Dhakal/OneDrive/Desktop/ZeroXAnalyser/atreya-online-e-commerce" --plain > "C:/Users/Anubhav Dhakal/OneDrive/Desktop/ZeroXAnalyser/Report/exported.txt"

cat "C:/Users/Anubhav Dhakal/OneDrive/Desktop/ZeroXAnalyser/Report/exported.txt" | grep "Remote Co" -A4 > "C:/Users/Anubhav Dhakal/OneDrive/Desktop/ZeroXAnalyser/Report/RemoteCodeExecution.txt"
# (Repeat for other vulnerabilities similarly)

echo "Generating PDF"
python3 "C:/Users/Anubhav Dhakal/OneDrive/Desktop/ZeroXAnalyser/pdfgen.py" && mv output.pdf "C:/Users/Anubhav Dhakal/OneDrive/Desktop/ZeroXAnalyser/Report/"
ls -ail "C:/Users/Anubhav Dhakal/OneDrive/Desktop/ZeroXAnalyser/Report"
