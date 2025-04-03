#!/bin/bash

# Run all tests
echo "===== Running All Tests ====="
python -m pytest -v

# Run with coverage report
echo -e "\n\n===== Running Tests with Coverage Report ====="
python -m pytest --cov=. --cov-report=term-missing

# Run individual test files
echo -e "\n\n===== Running Specific Test Files ====="
echo "--- Utils Tests ---"
python -m pytest -v tests/test_utils.py
echo "--- Auth Manager Tests ---"
python -m pytest -v tests/test_auth_manager.py
echo "--- Data Manager Tests ---"
python -m pytest -v tests/test_data_manager.py
echo "--- M-Pesa Parser Tests ---"
python -m pytest -v tests/test_mpesa_parser.py