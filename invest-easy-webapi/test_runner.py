#!/usr/bin/env python3
"""
Simple test runner for VS Code integration.
"""

import sys
import subprocess
import os

def main():
    """Run pytest with proper configuration."""
    # Change to the webapi directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Run pytest with the tests directory
    cmd = [sys.executable, "-m", "pytest", "tests/", "-v"]
    
    # Add any additional arguments passed to this script
    cmd.extend(sys.argv[1:])
    
    try:
        result = subprocess.run(cmd, capture_output=False, text=True)
        sys.exit(result.returncode)
    except Exception as e:
        print(f"Error running tests: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
