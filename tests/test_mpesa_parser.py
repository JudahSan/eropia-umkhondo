import pytest
from utils import parse_mpesa_statement
from datetime import date

def test_parse_mpesa_statement():
    """Test parsing M-Pesa statement text"""
    # Sample statement text
    statement_text = """
    03/04/2025 MPESA Payment to Uber 450.75 debit
    """
    
    transactions = parse_mpesa_statement(statement_text)
    
    # Check if we got the transaction
    assert len(transactions) == 1
    
    # Check transaction
    assert transactions[0]['date'] == date(2025, 4, 3)
    assert transactions[0]['description'] == 'MPESA Payment to Uber'
    assert transactions[0]['amount'] == 450.75
    assert transactions[0]['type'] == 'expense'
    assert transactions[0]['category'] == 'Transport'  # Should be categorized as Transport
    assert transactions[0]['source'] == 'mpesa'

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