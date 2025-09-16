#!/usr/bin/env python3
"""
Test runner script for Satoshi Sensei backend
"""

import subprocess
import sys
import os


def run_command(command, description):
    """Run a command and return success status."""
    print(f"\n{'='*60}")
    print(f"  {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=False)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with exit code {e.returncode}")
        return False


def main():
    """Main test runner function."""
    print("🧪 Satoshi Sensei Backend Test Runner")
    print("=" * 60)
    
    # Change to backend directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Install dependencies first
    if not run_command("pip install -r requirements.txt", "Installing Dependencies"):
        print("❌ Failed to install dependencies")
        return False
    
    # Run linting
    run_command("python -m flake8 app/ --max-line-length=100", "Code Linting")
    
    # Run type checking (if mypy is available)
    run_command("python -m mypy app/ --ignore-missing-imports", "Type Checking")
    
    # Run tests with coverage
    if not run_command(
        "python -m pytest tests/ -v --cov=app --cov-report=html --cov-report=term-missing --cov-fail-under=90",
        "Running Tests with Coverage"
    ):
        print("❌ Tests failed or coverage below 90%")
        return False
    
    # Run API demo (optional)
    print(f"\n{'='*60}")
    print("  API Demo (Optional)")
    print(f"{'='*60}")
    print("To run the API demo, start the server first:")
    print("  uvicorn main:app --reload")
    print("Then run:")
    print("  python api_demo.py")
    
    print("\n🎉 All tests completed successfully!")
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
