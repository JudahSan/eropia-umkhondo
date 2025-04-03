import pytest
import os
import pandas as pd
from datetime import date
from data_manager import DataManager

def test_data_manager_initialization(temp_data_dir):
    """Test that DataManager initializes correctly"""
    # Test with username
    dm = DataManager(username='testuser', data_dir=temp_data_dir)
    assert dm.username == 'testuser'
    assert dm.data_dir == temp_data_dir
    
    # Test without username (shared data)
    dm = DataManager(data_dir=temp_data_dir)
    assert dm.username is None
    assert dm.data_dir == temp_data_dir

def test_file_path_generation(temp_data_dir):
    """Test file path generation for different users"""
    # Test with username
    dm = DataManager(username='testuser', data_dir=temp_data_dir)
    file_path = dm._get_file_path()
    assert file_path.endswith('transactions_testuser.csv')
    
    # Test without username (shared data)
    dm = DataManager(data_dir=temp_data_dir)
    file_path = dm._get_file_path()
    assert file_path.endswith('transactions.csv')

def test_ensure_data_file_exists(temp_data_dir):
    """Test data file creation"""
    dm = DataManager(username='testuser', data_dir=temp_data_dir)
    dm.ensure_data_file_exists()
    
    # Check if file was created
    file_path = dm._get_file_path()
    assert os.path.exists(file_path)
    
    # Read the file to check if it has the correct header
    df = pd.read_csv(file_path)
    expected_columns = ['date', 'description', 'amount', 'type', 'category']
    for col in expected_columns:
        assert col in df.columns

def test_add_transaction(temp_data_dir):
    """Test adding transactions"""
    dm = DataManager(username='testuser', data_dir=temp_data_dir)
    
    # Add a transaction
    transaction = {
        'date': date(2025, 4, 1),
        'description': 'Test transaction',
        'amount': 1000.0,
        'type': 'expense',
        'category': 'Testing'
    }
    dm.add_transaction(transaction)
    
    # Verify transaction was added
    df = dm.get_transactions()
    assert len(df) == 1
    assert df.iloc[0]['description'] == 'Test transaction'
    assert df.iloc[0]['amount'] == 1000.0
    assert df.iloc[0]['type'] == 'expense'
    assert df.iloc[0]['category'] == 'Testing'
    
    # Add another transaction
    transaction2 = {
        'date': date(2025, 4, 2),
        'description': 'Second transaction',
        'amount': 500.0,
        'type': 'income',
        'category': 'Salary'
    }
    dm.add_transaction(transaction2)
    
    # Verify both transactions exist
    df = dm.get_transactions()
    assert len(df) == 2

def test_update_transaction_category(data_manager):
    """Test updating transaction category"""
    # Initial data has 3 transactions from the fixture
    
    # Update category of first transaction
    data_manager.update_transaction_category(0, 'Shopping')
    
    # Verify category was updated
    df = data_manager.get_transactions()
    assert df.iloc[0]['category'] == 'Shopping'
    assert df.iloc[1]['category'] == 'Salary'  # Unchanged
    assert df.iloc[2]['category'] == 'Transport'  # Unchanged

def test_delete_transaction(data_manager):
    """Test deleting transactions"""
    # Initial data has 3 transactions from the fixture
    
    # Get initial count
    initial_df = data_manager.get_transactions()
    initial_count = len(initial_df)
    
    # Delete first transaction
    data_manager.delete_transaction(0)
    
    # Verify first transaction was deleted
    df = data_manager.get_transactions()
    assert len(df) == initial_count - 1
    assert df.iloc[0]['description'] == 'Salary deposit'  # Now the first transaction

def test_get_transactions_by_date_range(data_manager, sample_transactions):
    """Test getting transactions by date range"""
    # Clear existing transactions and add sample with known dates
    for i in range(len(data_manager.get_transactions())):
        data_manager.delete_transaction(0)
    
    for t in sample_transactions:
        data_manager.add_transaction(t)
    
    # Test filtering by date range (only April 1-3)
    filtered_df = data_manager.get_transactions_by_date_range(
        start_date=date(2025, 4, 1),
        end_date=date(2025, 4, 3)
    )
    
    assert len(filtered_df) == 3
    descriptions = filtered_df['description'].tolist()
    assert 'Grocery shopping' in descriptions
    assert 'Salary deposit' in descriptions
    assert 'Uber ride' in descriptions
    assert 'Restaurant dinner' not in descriptions
    assert 'Side hustle payment' not in descriptions

def test_get_transactions_by_category(data_manager, sample_transactions):
    """Test getting transactions by category"""
    # Clear existing transactions and add sample with known categories
    for i in range(len(data_manager.get_transactions())):
        data_manager.delete_transaction(0)
    
    for t in sample_transactions:
        data_manager.add_transaction(t)
    
    # Test filtering by Food category
    filtered_df = data_manager.get_transactions_by_category('Food')
    
    assert len(filtered_df) == 2
    descriptions = filtered_df['description'].tolist()
    assert 'Grocery shopping' in descriptions
    assert 'Restaurant dinner' in descriptions
    assert 'Uber ride' not in descriptions
    assert 'Salary deposit' not in descriptions
    assert 'Side hustle payment' not in descriptions