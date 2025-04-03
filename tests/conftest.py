import pytest
import os
import yaml
import tempfile
import shutil
from datetime import date
from auth_manager import AuthManager
from data_manager import DataManager

@pytest.fixture
def temp_config_file():
    """Create a temporary YAML config file for testing"""
    with tempfile.NamedTemporaryFile(suffix='.yaml', delete=False) as temp_file:
        # Create a test config
        test_config = {
            'cookie': {'expiry_days': 30, 'key': 'test_cookie', 'name': 'test_cookie'},
            'credentials': {
                'usernames': {
                    'testuser': {
                        'email': 'testuser@example.com',
                        'name': 'Test User',
                        'password': '$2b$12$ZnAREWBZyYtG/YWkjmUr5Odn.ACZlRPD029QKzKYq3PvmvD7Zhgey',  # 'password'
                        'phone_number': '2547123456789',
                        'role': 'user'
                    }
                }
            },
            'preauthorized': {'emails': []}
        }
        yaml.dump(test_config, temp_file)
        config_path = temp_file.name
    
    yield config_path
    
    # Clean up the temp file
    if os.path.exists(config_path):
        os.unlink(config_path)
        
@pytest.fixture
def auth_manager(temp_config_file):
    """Create an AuthManager instance for testing"""
    return AuthManager(config_path=temp_config_file)

@pytest.fixture
def temp_data_dir():
    """Create a temporary directory for test data"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    
    # Clean up the temp directory
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
        
@pytest.fixture
def data_manager(temp_data_dir):
    """Create a DataManager instance for testing"""
    dm = DataManager(username='testuser', data_dir=temp_data_dir)
    
    # Add some test transactions
    transactions = [
        {
            'date': date(2025, 4, 1),
            'description': 'Grocery shopping',
            'amount': 1000.0,
            'type': 'expense',
            'category': 'Food'
        },
        {
            'date': date(2025, 4, 2),
            'description': 'Salary deposit',
            'amount': 5000.0,
            'type': 'income',
            'category': 'Salary'
        },
        {
            'date': date(2025, 4, 3),
            'description': 'Uber ride',
            'amount': 300.0,
            'type': 'expense',
            'category': 'Transport'
        }
    ]
    
    for t in transactions:
        dm.add_transaction(t)
        
    return dm

@pytest.fixture
def sample_transactions():
    """Return a list of sample transactions for testing"""
    return [
        {
            'date': date(2025, 4, 1),
            'description': 'Grocery shopping',
            'amount': 1000.0,
            'type': 'expense',
            'category': 'Food'
        },
        {
            'date': date(2025, 4, 2),
            'description': 'Salary deposit',
            'amount': 5000.0,
            'type': 'income',
            'category': 'Salary'
        },
        {
            'date': date(2025, 4, 3),
            'description': 'Uber ride',
            'amount': 300.0,
            'type': 'expense',
            'category': 'Transport'
        },
        {
            'date': date(2025, 4, 4),
            'description': 'Restaurant dinner',
            'amount': 800.0,
            'type': 'expense',
            'category': 'Food'
        },
        {
            'date': date(2025, 4, 5),
            'description': 'Side hustle payment',
            'amount': 2000.0,
            'type': 'income',
            'category': 'Freelance'
        }
    ]