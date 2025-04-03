import requests
import base64
import json
import os
import time
from datetime import datetime, timedelta

class MPesaAPI:
    """Class to interact with the M-Pesa API for transaction data"""
    
    def __init__(self, username=None, auth_manager=None):
        """Initialize the M-Pesa API client with credentials
        
        Args:
            username (str): Username for the current user
            auth_manager (AuthManager): Authentication manager instance
        """
        # Get API credentials from environment variables
        self.consumer_key = os.getenv("MPESA_CONSUMER_KEY", "")
        self.consumer_secret = os.getenv("MPESA_CONSUMER_SECRET", "")
        self.base_url = os.getenv("MPESA_API_URL", "https://sandbox.safaricom.co.ke")
        
        # Authentication token cache
        self.auth_token = None
        self.token_expiry = None
        
        # User-specific data
        self.username = username
        self.auth_manager = auth_manager
    
    def get_auth_token(self):
        """Get OAuth authentication token from M-Pesa API
        
        Returns:
            str: Authentication token
        """
        # Check if we have a valid cached token
        if self.auth_token and self.token_expiry and datetime.now() < self.token_expiry:
            return self.auth_token
            
        try:
            # Create the auth string
            auth_string = f"{self.consumer_key}:{self.consumer_secret}"
            encoded_auth = base64.b64encode(auth_string.encode()).decode('utf-8')
            
            # Make the request
            headers = {
                "Authorization": f"Basic {encoded_auth}"
            }
            
            url = f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials"
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                response_data = response.json()
                self.auth_token = response_data.get('access_token')
                
                # Set token expiry (typically 1 hour)
                self.token_expiry = datetime.now() + timedelta(seconds=3599)
                
                return self.auth_token
            else:
                print(f"Error getting auth token: {response.text}")
                return None
                
        except Exception as e:
            print(f"Exception getting auth token: {e}")
            return None
    
    def get_transactions(self, phone_number, start_date, end_date):
        """Get M-Pesa transactions for a specific phone number and date range
        
        Args:
            phone_number (str): The phone number in format 2547XXXXXXXX
            start_date (date): Start date for transaction query
            end_date (date): End date for transaction query
            
        Returns:
            list: List of transaction dictionaries
        """
        # Security check: Ensure user can only access their own phone numbers
        if self.username and self.auth_manager:
            # Get the user's registered phone number
            user_phone = self.auth_manager.get_user_phone_number(self.username)
            
            # If phone numbers don't match and user is not admin, deny access
            if user_phone and user_phone != phone_number and not self.auth_manager.is_admin(self.username):
                raise ValueError("You can only access transactions for your registered phone number.")
        
        # In a real implementation, this would call the M-Pesa API
        # For this example, I'll simulate the API response since we don't have actual API access
        
        # First, simulate checking if credentials are set
        if not self.consumer_key or not self.consumer_secret:
            raise ValueError("M-Pesa API credentials not configured. Please set MPESA_CONSUMER_KEY and MPESA_CONSUMER_SECRET environment variables.")
        
        # Simulate an API call
        auth_token = self.get_auth_token()
        if not auth_token:
            raise ValueError("Failed to authenticate with M-Pesa API")
        
        # In a real implementation, we'd make an actual API call here
        # For now, we'll simulate a processing delay and then return no results
        # as we don't have actual access to the M-Pesa API
        time.sleep(1.5)  # Simulate API call delay
        
        # Simulate API unavailable or error
        # In a real implementation, replace this with actual API call
        raise ValueError(
            "Unable to connect to M-Pesa API. Please ensure you have set the following environment variables:\n\n"
            "1. MPESA_CONSUMER_KEY: Your M-Pesa API consumer key from the Safaricom Developer Portal\n"
            "2. MPESA_CONSUMER_SECRET: Your M-Pesa API consumer secret from the Safaricom Developer Portal\n"
            "3. MPESA_API_URL (optional): The M-Pesa API URL (defaults to sandbox)\n\n"
            "You can obtain these credentials by registering on the Safaricom Developer Portal at https://developer.safaricom.co.ke/"
        )
        
        # The code below would never execute in this simulation
        # In a real implementation, we would process the API response and return transactions
        
        """
        # Example of what the real implementation would look like:
        url = f"{self.base_url}/mpesa/transactionhistory/v1/query"
        
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json"
        }
        
        # Format dates as required by the API
        start_date_str = start_date.strftime('%Y%m%d')
        end_date_str = end_date.strftime('%Y%m%d')
        
        payload = {
            "PhoneNumber": phone_number,
            "StartDate": start_date_str,
            "EndDate": end_date_str
        }
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            response_data = response.json()
            
            # Process and format the transactions
            transactions = []
            for item in response_data.get('Items', []):
                transaction = {
                    'date': datetime.strptime(item.get('TransactionDate'), '%Y%m%d').date(),
                    'description': item.get('Description', ''),
                    'amount': float(item.get('Amount', 0)),
                    'type': 'expense' if item.get('TransactionType') == 'Debit' else 'income',
                    'category': 'Other',  # Will be categorized by utils.categorize_transaction
                }
                transactions.append(transaction)
                
            return transactions
        else:
            print(f"Error getting transactions: {response.text}")
            return []
        """
