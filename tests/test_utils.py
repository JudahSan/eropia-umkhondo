import pytest
from utils import categorize_transaction, format_currency

def test_categorize_transaction_food():
    """Test that food-related transactions are correctly categorized"""
    assert categorize_transaction("Lunch at Restaurant") == "Food"
    assert categorize_transaction("Payment to Naivas Supermarket") == "Food"
    assert categorize_transaction("Carrefour groceries purchase") == "Food"
    assert categorize_transaction("Coffee at Java") == "Food"
    assert categorize_transaction("KFC payment") == "Food"
    assert categorize_transaction("Jumia Food delivery") == "Food"

def test_categorize_transaction_transport():
    """Test that transport-related transactions are correctly categorized"""
    assert categorize_transaction("Uber ride") == "Transport"
    assert categorize_transaction("Bolt taxi payment") == "Transport"
    assert categorize_transaction("Matatu fare") == "Transport"
    assert categorize_transaction("Fuel purchase at Shell") == "Transport"
    assert categorize_transaction("Parking fee payment") == "Transport"

def test_categorize_transaction_housing():
    """Test that housing-related transactions are correctly categorized"""
    assert categorize_transaction("Rent payment") == "Housing"
    assert categorize_transaction("KPLC electricity bill") == "Housing"
    assert categorize_transaction("Water bill payment") == "Housing"
    assert categorize_transaction("Airbnb accommodation") == "Housing"

def test_categorize_transaction_utilities():
    """Test that utilities-related transactions are correctly categorized"""
    assert categorize_transaction("Safaricom airtime") == "Utilities"
    assert categorize_transaction("WiFi bill payment") == "Utilities"
    assert categorize_transaction("Netflix subscription") == "Utilities"
    assert categorize_transaction("DSTV payment") == "Utilities"

def test_categorize_transaction_other_categories():
    """Test other transaction categories"""
    assert categorize_transaction("Doctor visit") == "Health"
    assert categorize_transaction("University tuition") == "Education"
    assert categorize_transaction("Jumia shopping") == "Shopping"
    assert categorize_transaction("Flight ticket") == "Travel"
    assert categorize_transaction("Cinema tickets") == "Entertainment"

def test_categorize_transaction_default():
    """Test that unknown transactions are categorized as 'Other'"""
    assert categorize_transaction("Random transaction") == "Other"
    assert categorize_transaction("Payment to unknown entity") == "Other"
    assert categorize_transaction("123456789") == "Other"
    assert categorize_transaction("") == "Other"

def test_format_currency():
    """Test currency formatting"""
    assert format_currency(1000) == "KSh 1,000.00"
    assert format_currency(1000.5) == "KSh 1,000.50"
    assert format_currency(1234567.89) == "KSh 1,234,567.89"
    assert format_currency(0) == "KSh 0.00"
    assert format_currency(0.5) == "KSh 0.50"