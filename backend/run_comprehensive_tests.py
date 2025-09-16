#!/usr/bin/env python3
"""
Comprehensive test runner for Satoshi Sensei backend
"""

import subprocess
import sys
import os
import time
import argparse
from pathlib import Path


def run_command(command, description, capture_output=False):
    """Run a command and return success status."""
    print(f"\n{'='*60}")
    print(f"  {description}")
    print(f"{'='*60}")
    
    try:
        if capture_output:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            return result.returncode == 0, result.stdout, result.stderr
        else:
            result = subprocess.run(command, shell=True, check=True)
            print(f"✅ {description} completed successfully")
            return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with exit code {e.returncode}")
        if capture_output:
            return False, "", str(e)
        return False


def install_dependencies():
    """Install test dependencies."""
    print("📦 Installing dependencies...")
    success = run_command("pip install -r requirements.txt", "Installing Dependencies")
    if not success:
        print("❌ Failed to install dependencies")
        return False
    return True


def run_linting():
    """Run code linting."""
    print("🔍 Running code linting...")
    success = run_command(
        "python -m flake8 app/ --max-line-length=100 --exclude=__pycache__",
        "Code Linting"
    )
    return success


def run_type_checking():
    """Run type checking."""
    print("🔍 Running type checking...")
    success = run_command(
        "python -m mypy app/ --ignore-missing-imports --no-strict-optional",
        "Type Checking"
    )
    return success


def run_unit_tests():
    """Run unit tests."""
    print("🧪 Running unit tests...")
    success = run_command(
        "python -m pytest tests/test_models.py tests/test_main.py -v --cov=app --cov-report=term-missing",
        "Unit Tests"
    )
    return success


def run_auth_tests():
    """Run authentication tests."""
    print("🔐 Running authentication tests...")
    success = run_command(
        "python -m pytest tests/test_auth.py -v --cov=app --cov-report=term-missing",
        "Authentication Tests"
    )
    return success


def run_wallet_tests():
    """Run wallet tests."""
    print("💰 Running wallet tests...")
    success = run_command(
        "python -m pytest tests/test_wallet.py -v --cov=app --cov-report=term-missing",
        "Wallet Tests"
    )
    return success


def run_strategy_tests():
    """Run strategy tests."""
    print("🎯 Running strategy tests...")
    success = run_command(
        "python -m pytest tests/test_strategy.py -v --cov=app --cov-report=term-missing",
        "Strategy Tests"
    )
    return success


def run_education_tests():
    """Run education tests."""
    print("📚 Running education tests...")
    success = run_command(
        "python -m pytest tests/test_education.py -v --cov=app --cov-report=term-missing",
        "Education Tests"
    )
    return success


def run_error_handling_tests():
    """Run error handling tests."""
    print("⚠️ Running error handling tests...")
    success = run_command(
        "python -m pytest tests/test_error_handling.py -v --cov=app --cov-report=term-missing",
        "Error Handling Tests"
    )
    return success


def run_integration_tests():
    """Run integration tests."""
    print("🔗 Running integration tests...")
    success = run_command(
        "python -m pytest tests/test_integration.py -v --cov=app --cov-report=term-missing",
        "Integration Tests"
    )
    return success


def run_performance_tests():
    """Run performance tests."""
    print("⚡ Running performance tests...")
    success = run_command(
        "python -m pytest tests/test_performance.py -v --cov=app --cov-report=term-missing",
        "Performance Tests"
    )
    return success


def run_all_tests():
    """Run all tests with coverage."""
    print("🚀 Running all tests with coverage...")
    success = run_command(
        "python -m pytest tests/ -v --cov=app --cov-report=html --cov-report=term-missing --cov-fail-under=80",
        "All Tests with Coverage"
    )
    return success


def run_api_demo():
    """Run API demo."""
    print("🎭 Running API demo...")
    print("Note: This requires the server to be running")
    print("Start server with: uvicorn main:app --reload")
    print("Then run: python api_demo.py")
    return True


def generate_coverage_report():
    """Generate detailed coverage report."""
    print("📊 Generating coverage report...")
    success = run_command(
        "python -m pytest tests/ --cov=app --cov-report=html --cov-report=xml --cov-report=term-missing",
        "Coverage Report Generation"
    )
    if success:
        print("📈 Coverage report generated in htmlcov/index.html")
    return success


def run_specific_test_category(category):
    """Run specific test category."""
    test_categories = {
        "unit": run_unit_tests,
        "auth": run_auth_tests,
        "wallet": run_wallet_tests,
        "strategy": run_strategy_tests,
        "education": run_education_tests,
        "error": run_error_handling_tests,
        "integration": run_integration_tests,
        "performance": run_performance_tests,
        "all": run_all_tests
    }
    
    if category not in test_categories:
        print(f"❌ Unknown test category: {category}")
        print(f"Available categories: {', '.join(test_categories.keys())}")
        return False
    
    return test_categories[category]()


def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(description="Satoshi Sensei Backend Test Runner")
    parser.add_argument(
        "--category",
        choices=["unit", "auth", "wallet", "strategy", "education", "error", "integration", "performance", "all"],
        help="Run specific test category"
    )
    parser.add_argument(
        "--skip-deps",
        action="store_true",
        help="Skip dependency installation"
    )
    parser.add_argument(
        "--skip-lint",
        action="store_true",
        help="Skip linting"
    )
    parser.add_argument(
        "--skip-type-check",
        action="store_true",
        help="Skip type checking"
    )
    parser.add_argument(
        "--coverage-only",
        action="store_true",
        help="Only run coverage report"
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run API demo"
    )
    
    args = parser.parse_args()
    
    print("🧪 Satoshi Sensei Backend Comprehensive Test Runner")
    print("=" * 60)
    
    # Change to backend directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    start_time = time.time()
    
    # Install dependencies
    if not args.skip_deps:
        if not install_dependencies():
            return False
    
    # Run specific category if requested
    if args.category:
        success = run_specific_test_category(args.category)
        if not success:
            return False
    elif args.coverage_only:
        success = generate_coverage_report()
        if not success:
            return False
    elif args.demo:
        success = run_api_demo()
        if not success:
            return False
    else:
        # Run full test suite
        if not args.skip_lint:
            run_linting()
        
        if not args.skip_type_check:
            run_type_checking()
        
        # Run all tests
        success = run_all_tests()
        if not success:
            print("❌ Some tests failed")
            return False
        
        # Generate coverage report
        generate_coverage_report()
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"\n🎉 Test suite completed in {total_time:.2f} seconds!")
    print("\n📋 Next Steps:")
    print("1. Review test results above")
    print("2. Check coverage report: htmlcov/index.html")
    print("3. Fix any failing tests")
    print("4. Run API demo: python api_demo.py")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
