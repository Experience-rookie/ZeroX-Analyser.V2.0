#!/bin/bash

# Function to print a usage message
usage() {
    echo "Usage: $0 --dir <directory> [--plain]"
    echo "  --dir    Directory to analyze"
    echo "  --plain  Output in plain text format"
    exit 1
}

# Parse command-line arguments
DIR=""
PLAIN=false

while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --dir) DIR="$2"; shift ;;
        --plain) PLAIN=true ;;
        *) usage ;;
    esac
    shift
done

# Check if directory is provided
if [ -z "$DIR" ]; then
    echo "❌ Error: Directory is required."
    usage
fi

# Check if directory exists
if [ ! -d "$DIR" ]; then
    echo "❌ Error: The specified directory does not exist."
    exit 1
fi

# Check if there are any .php files
PHP_FILE_COUNT=$(find "$DIR" -type f -name "*.php" | wc -l)

if [ "$PHP_FILE_COUNT" -eq 0 ]; then
    echo "⚠️ No PHP files found in '$DIR'. Skipping analysis."
    exit 0
fi

# Run the analyzer
echo "🔍 Starting analysis of directory: $DIR"

# Use Windows Python if available, fallback to python3
PYTHON_BIN="python3"
if command -v python.exe &> /dev/null; then
    PYTHON_BIN="python.exe"
fi

# Execute with appropriate flags
if $PLAIN; then
    echo "📄 Running with plain output..."
    $PYTHON_BIN zeroXanalyser.py --dir "$DIR" --plain
else
    echo "✨ Running with formatted output..."
    $PYTHON_BIN zeroXanalyser.py --dir "$DIR"
fi

# Check if report was generated
if [ -f "ZeroXAnalyser_Report.pdf" ]; then
    if [ ! -s "ZeroXAnalyser_Report.pdf" ]; then
        echo "✅ Scan completed. No vulnerabilities were detected in '$DIR'."
        rm -f ZeroXAnalyser_Report.pdf  # Optional: remove empty report
    else
        echo "✅ Scan complete! Report generated: ZeroXAnalyser_Report.pdf"
    fi
else
    echo "⚠️ No scan results found."
fi

echo "✅ Analysis complete!"
