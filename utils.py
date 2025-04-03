import re

def categorize_transaction(description):
    """Automatically categorize a transaction based on its description
    
    Args:
        description (str): Transaction description
        
    Returns:
        str: Assigned category
    """
    description = description.lower()
    
    # Food and Dining
    if any(keyword in description for keyword in [
        'restaurant', 'cafe', 'food', 'grocery', 'supermarket', 'naivas', 'carrefour', 
        'quickmart', 'dinner', 'lunch', 'breakfast', 'eat', 'meal', 'coffee', 'java', 
        'kfc', 'mcdonalds', 'jumia food', 'uber eats', 'bolt food', 'glovo'
    ]):
        return 'Food'
        
    # Transport
    if any(keyword in description for keyword in [
        'uber', 'bolt', 'little', 'taxi', 'matatu', 'bus', 'fare', 'transport', 'fuel',
        'petrol', 'diesel', 'car', 'vehicle', 'parking', 'ride', 'travel', 'transport'
    ]):
        return 'Transport'
        
    # Housing & Utilities
    if any(keyword in description for keyword in [
        'rent', 'house', 'apartment', 'water', 'electricity', 'power', 'kplc', 'bill',
        'utility', 'gas', 'housing', 'mortgage', 'accommodation', 'airbnb', 'hotel',
        'internet', 'wifi', 'safaricom home', 'zuku'
    ]):
        return 'Housing'
    
    # Bills & Utilities
    if any(keyword in description for keyword in [
        'bill', 'utility', 'internet', 'wifi', 'airtime', 'safaricom', 'telkom', 'airtel',
        'phone', 'data', 'subscription', 'dstv', 'netflix', 'spotify', 'showmax', 'bundle'
    ]):
        return 'Utilities'
        
    # Entertainment
    if any(keyword in description for keyword in [
        'cinema', 'movie', 'ticket', 'concert', 'event', 'game', 'betting', 'sportpesa',
        'betika', 'entertainment', 'party', 'club', 'bar', 'alcohol', 'beer', 'fun',
        'leisure', 'recreation'
    ]):
        return 'Entertainment'
        
    # Health
    if any(keyword in description for keyword in [
        'hospital', 'doctor', 'medical', 'health', 'pharmacy', 'medicine', 'clinic',
        'dental', 'healthcare', 'insurance', 'nhif'
    ]):
        return 'Health'
        
    # Education
    if any(keyword in description for keyword in [
        'school', 'college', 'university', 'tuition', 'fee', 'education', 'course',
        'class', 'training', 'book', 'learning', 'student'
    ]):
        return 'Education'
        
    # Shopping
    if any(keyword in description for keyword in [
        'shop', 'mall', 'store', 'purchase', 'buy', 'jumia', 'amazon', 'clothes',
        'shopping', 'item', 'product', 'electronic', 'gadget', 'furniture'
    ]):
        return 'Shopping'
        
    # Travel
    if any(keyword in description for keyword in [
        'flight', 'air', 'train', 'sgr', 'vacation', 'holiday', 'tour', 'travel',
        'trip', 'hotel', 'accommodation', 'booking', 'ticket', 'transport', 'lodge'
    ]):
        return 'Travel'
    
    # Default to 'Other' if no match
    return 'Other'

def format_currency(amount):
    """Format a number as Kenyan Shillings currency
    
    Args:
        amount (float): Amount to format
        
    Returns:
        str: Formatted currency string
    """
    return f"KSh {amount:,.2f}"

def parse_mpesa_statement(statement_text):
    """Parse M-Pesa statement text into structured transaction data
    
    Args:
        statement_text (str): Raw M-Pesa statement text
        
    Returns:
        list: List of transaction dictionaries
    """
    from datetime import datetime
    
    transactions = []
    
    # Regular expression to match M-Pesa transaction patterns
    # This is a simplified version and might need adjustment based on actual statement format
    pattern = r'(\d{2}/\d{2}/\d{4})\s+([\w\s]+)\s+(\d+[\.\d]*)\s+([\w\s]+)'
    
    matches = re.finditer(pattern, statement_text)
    
    for match in matches:
        date_str, description, amount_str, transaction_type = match.groups()
        
        # Parse date
        date = datetime.strptime(date_str, '%d/%m/%Y').date()
        
        # Parse amount
        amount = float(amount_str.replace(',', ''))
        
        # Determine transaction type (income/expense)
        if any(t in transaction_type.lower() for t in ['receive', 'deposit', 'credit']):
            type_category = 'income'
        else:
            type_category = 'expense'
            
        # Categorize the transaction
        category = categorize_transaction(description)
        
        transactions.append({
            'date': date,
            'description': description.strip(),
            'amount': amount,
            'type': type_category,
            'category': category,
            'source': 'mpesa'
        })
    
    return transactions
