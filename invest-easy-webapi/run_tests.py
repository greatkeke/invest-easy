#!/usr/bin/env python3
"""
Test runner script for the invest-easy-webapi project.
"""

import subprocess
import sys
import os


def run_tests():
    """Run pytest with coverage report."""
    try:
        # Change to the webapi directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        # Run pytest
        cmd = [
            "python", "-m", "pytest",
            "tests/",
            "-v",
            "--tb=short",
            "-x"  # Stop on first failure
        ]
        
        # Add coverage if available
        try:
            subprocess.run([sys.executable, "-c", "import pytest_cov"], 
                         capture_output=True, check=True)
            cmd.extend([
                "--cov=app/",
                "--cov-report=term-missing",
                "--cov-report=html"
            ])
        except subprocess.CalledProcessError:
            print("pytest-cov not available, running tests without coverage")
        
        result = subprocess.run(cmd, capture_output=False, text=True)
        return result.returncode == 0
        
    except Exception as e:
        print(f"Error running tests: {e}")
        return False


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
