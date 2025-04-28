ZeroX-Analyser v2.0
🚀 ZeroX-Analyser v2.0 is an enhanced Static Application Security Testing (SAST) framework designed to automatically detect vulnerabilities in PHP-based e-commerce applications.
It focuses on identifying issues based on the OWASP Top 10 vulnerabilities and integrates seamlessly with your workflows.

✨ Features
🔍 Static code analysis for PHP e-commerce projects

🛡️ Detection of common vulnerabilities like SQL Injection, XSS, IDOR, etc.

📝 Automatic report generation in PDF format

⚙️ Bash script to automate scanning and reporting

🚀 Modular architecture for scalability and new feature additions

📁 Project Structure
ZeroX-Analyser/
├── automate_scanning.sh       # Shell script to automate scanning and reporting
├── zeroXanalyser.py            # Main analyzer script
├── detect.py                   # Vulnerability pattern detection
├── indicators.py               # Indicators for vulnerabilities
├── utils.py                    # Helper functions
├── pdfgen.py                   # PDF report generation
├── report.py                   # Handling report creation
├── feature.py                  # Additional analysis features
├── secure_ecommerce/           # Sample secure e-commerce code (testing)
├── vulnerable_code/            # Sample vulnerable code (testing)
└── ZeroXAnalyser_Report.pdf    # Sample output report

🛠️ Installation
Clone the repository
git clone https://github.com/Experience-rookie/ZeroX-Analyser.V2.0.git
cd ZeroX-Analyser.V2.0
Install required Python libraries

🚀 Usage
To scan a PHP project manually:
python3 zeroXanalyser.py --dir /path/to/php/project

To automate scanning and report generation:
bash automate_scanning.sh
The output will be saved as a PDF report containing vulnerability details.

🧩 Requirements
Python 3.8+
Bash (for shell scripting)
Libraries: fpdf, argparse, os, re, etc.

📋 Future Improvements
Add support for other languages (Node.js, Java)
CI/CD pipeline integration (GitHub Actions)
Customizable rule sets for detecting organization-specific patterns
Enhanced PDF reports with vulnerability severity ratings

👨‍💻 Author
Anubhav Dhakal — Experience-rookie
Security Researcher | CTF Player | Bug Bounty Hunter
