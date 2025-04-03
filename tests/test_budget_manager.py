import pytest
import pandas as pd
from datetime import datetime, date, timedelta
import os
import tempfile
import shutil
from budget_manager import BudgetManager
from data_manager import DataManager

@pytest.fixture
def temp_budget_dir():
    """Create a temporary directory for test budget data"""
    test_dir = tempfile.mkdtemp()
    yield test_dir
    shutil.rmtree(test_dir)

@pytest.fixture
def budget_manager(temp_budget_dir):
    """Create a BudgetManager instance for testing"""
    test_username = "testuser"
    return BudgetManager(username=test_username, data_dir=temp_budget_dir)

@pytest.fixture
def sample_budget():
    """Return a sample budget item for testing"""
    today = date.today()
    return {
        'category': 'Food',
        'amount': 5000.0,
        'period': 'monthly',
        'start_date': today,
        'end_date': date(today.year, today.month + 1 if today.month < 12 else 1, min(today.day, 28))
    }

def test_budget_manager_initialization(temp_budget_dir):
    """Test that BudgetManager initializes correctly"""
    test_username = "testuser"
    budget_manager = BudgetManager(username=test_username, data_dir=temp_budget_dir)
    
    # Check that the budget file exists
    budget_file = os.path.join(temp_budget_dir, f"budget_{test_username}.csv")
    assert os.path.exists(budget_file)
    
    # Check that the budget file has the correct columns
    df = pd.read_csv(budget_file)
    expected_columns = ['category', 'amount', 'period', 'start_date', 'end_date', 'created_at', 'modified_at']
    assert all(col in df.columns for col in expected_columns)

def test_add_budget(budget_manager, sample_budget):
    """Test adding a budget item"""
    # Add a budget item
    budget_manager.add_budget(sample_budget)
    
    # Get all budgets
    budgets = budget_manager.get_budgets()
    
    # Check that the budget item was added
    assert len(budgets) == 1
    assert budgets.iloc[0]['category'] == sample_budget['category']
    assert budgets.iloc[0]['amount'] == sample_budget['amount']
    assert budgets.iloc[0]['period'] == sample_budget['period']

def test_update_budget(budget_manager, sample_budget):
    """Test updating a budget item"""
    # Add a budget item
    budget_manager.add_budget(sample_budget)
    
    # Update the budget item
    updates = {'amount': 6000.0}
    budget_manager.update_budget(0, updates)
    
    # Get all budgets
    budgets = budget_manager.get_budgets()
    
    # Check that the budget item was updated
    assert budgets.iloc[0]['amount'] == 6000.0

def test_delete_budget(budget_manager, sample_budget):
    """Test deleting a budget item"""
    # Add a budget item
    budget_manager.add_budget(sample_budget)
    
    # Delete the budget item
    budget_manager.delete_budget(0)
    
    # Get all budgets
    budgets = budget_manager.get_budgets()
    
    # Check that the budget item was deleted
    assert len(budgets) == 0

def test_get_active_budgets(budget_manager):
    """Test getting active budgets"""
    today = date.today()
    
    # Add an active budget
    active_budget = {
        'category': 'Food',
        'amount': 5000.0,
        'period': 'monthly',
        'start_date': today - timedelta(days=5),
        'end_date': today + timedelta(days=25)
    }
    budget_manager.add_budget(active_budget)
    
    # Add an inactive budget (past)
    past_budget = {
        'category': 'Transport',
        'amount': 3000.0,
        'period': 'monthly',
        'start_date': today - timedelta(days=60),
        'end_date': today - timedelta(days=30)
    }
    budget_manager.add_budget(past_budget)
    
    # Add an inactive budget (future)
    future_budget = {
        'category': 'Entertainment',
        'amount': 2000.0,
        'period': 'monthly',
        'start_date': today + timedelta(days=30),
        'end_date': today + timedelta(days=60)
    }
    budget_manager.add_budget(future_budget)
    
    # Get active budgets
    active_budgets = budget_manager.get_active_budgets()
    
    # Check that only the active budget is returned
    assert len(active_budgets) == 1
    assert active_budgets.iloc[0]['category'] == 'Food'

def test_get_budget_by_category(budget_manager):
    """Test getting budgets by category"""
    today = date.today()
    
    # Add budgets for different categories
    food_budget = {
        'category': 'Food',
        'amount': 5000.0,
        'period': 'monthly',
        'start_date': today,
        'end_date': today + timedelta(days=30)
    }
    budget_manager.add_budget(food_budget)
    
    transport_budget = {
        'category': 'Transport',
        'amount': 3000.0,
        'period': 'monthly',
        'start_date': today,
        'end_date': today + timedelta(days=30)
    }
    budget_manager.add_budget(transport_budget)
    
    # Get budget for Food category
    food_budgets = budget_manager.get_budget_by_category('Food')
    
    # Check that only the Food budget is returned
    assert len(food_budgets) == 1
    assert food_budgets.iloc[0]['category'] == 'Food'
    assert food_budgets.iloc[0]['amount'] == 5000.0