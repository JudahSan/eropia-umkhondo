import pytest
from utils import parse_mpesa_statement
from datetime import date

def test_parse_mpesa_statement():
    """Test parsing M-Pesa statement text"""
    # Sample statement text
    statement_text = """
    01/04/2025 MPESA Payment to Carrefour 2,500.00 debit
    02/04/2025 MPESA Receive from John Doe 5,000.00 credit
    03/04/2025 MPESA Payment to Uber 450.75 debit
    """
    
    transactions = parse_mpesa_statement(statement_text)
    
    # Check if we got 3 transactions
    assert len(transactions) == 3
    
    # Check first transaction
    assert transactions[0]['date'] == date(2025, 4, 1)
    assert transactions[0]['description'] == 'MPESA Payment to Carrefour'
    assert transactions[0]['amount'] == 2500.0
    assert transactions[0]['type'] == 'expense'
    assert transactions[0]['category'] == 'Food'  # Should be categorized as Food
    assert transactions[0]['source'] == 'mpesa'
    
    # Check second transaction
    assert transactions[1]['date'] == date(2025, 4, 2)
    assert transactions[1]['description'] == 'MPESA Receive from John Doe'
    assert transactions[1]['amount'] == 5000.0
    assert transactions[1]['type'] == 'income'
    assert transactions[1]['source'] == 'mpesa'
    
    # Check third transaction
    assert transactions[2]['date'] == date(2025, 4, 3)
    assert transactions[2]['description'] == 'MPESA Payment to Uber'
    assert transactions[2]['amount'] == 450.75
    assert transactions[2]['type'] == 'expense'
    assert transactions[2]['category'] == 'Transport'  # Should be categorized as Transport
    assert transactions[2]['source'] == 'mpesa'

def test_parse_mpesa_statement_empty():
    """Test parsing empty M-Pesa statement text"""
    statement_text = ""
    transactions = parse_mpesa_statement(statement_text)
    assert len(transactions) == 0  # Should return empty list

def test_parse_mpesa_statement_malformed():
    """Test parsing malformed M-Pesa statement text"""
    # Malformed statement text with incorrect date format
    statement_text = """
    2025-04-01 MPESA Payment to Carrefour 2,500.00 debit
    """
    
    transactions = parse_mpesa_statement(statement_text)
    assert len(transactions) == 0  # Should not match the pattern