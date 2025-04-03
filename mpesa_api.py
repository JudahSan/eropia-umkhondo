import requests
import base64
import json
import os
import time
import uuid
import hashlib
from datetime import datetime, timedelta
from dotenv import load_dotenv
from utils import categorize_transaction

# Load environment variables from .env file if present
load_dotenv()

class MPesaAPI:
    """Class to interact with the M-Pesa Daraja API for transaction data
    
    This class provides methods to interact with the M-Pesa Daraja API,
    including authentication, transaction fetching, C2B integration, 
    and transaction status queries.
    """
    
    def __init__(self, username=None, auth_manager=None):
        """Initialize the M-Pesa API client with credentials
        
        Args:
            username (str): Username for the current user
            auth_manager (AuthManager): Authentication manager instance
        """
        # Get API credentials from environment variables
        self.consumer_key = os.getenv("MPESA_CONSUMER_KEY", "")
        self.consumer_secret = os.getenv("MPESA_CONSUMER_SECRET", "")
        self.business_short_code = os.getenv("MPESA_BUSINESS_SHORT_CODE", "")
        self.passkey = os.getenv("MPESA_PASSKEY", "")
        self.callback_url = os.getenv("MPESA_CALLBACK_URL", "https://example.com/callback")
        self.base_url = os.getenv("MPESA_API_URL", "https://sandbox.safaricom.co.ke")
        
        # Authentication token cache
        self.auth_token = None
        self.token_expiry = None
        
        # User-specific data
        self.username = username
        self.auth_manager = auth_manager
        
        # Transaction storage - in a real system, this would be a database
        self._transaction_store = {}
    
    def get_auth_token(self):
        """Get OAuth authentication token from M-Pesa API
        
        Returns:
            str: Authentication token
        """
        # Check if we have a valid cached token
        if self.auth_token and self.token_expiry and datetime.now() < self.token_expiry:
            return self.auth_token
        
        # In a sandbox environment or demo mode, we can simulate a valid token
        if os.getenv("MPESA_DEMO_MODE", "false").lower() == "true":
            self.auth_token = f"SimulatedToken{uuid.uuid4().hex[:8]}"
            self.token_expiry = datetime.now() + timedelta(seconds=3599)
            return self.auth_token
            
        # For real API connections, authenticate with the Daraja API
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
    
    def _validate_credentials(self):
        """Validate that required credentials are set
        
        Raises:
            ValueError: If required credentials are missing
        """
        if not self.consumer_key or not self.consumer_secret:
            raise ValueError("M-Pesa API credentials not configured. Please set MPESA_CONSUMER_KEY and MPESA_CONSUMER_SECRET environment variables.")
        
        if not self.business_short_code:
            raise ValueError("M-Pesa business short code not configured. Please set MPESA_BUSINESS_SHORT_CODE environment variable.")
            
        auth_token = self.get_auth_token()
        if not auth_token:
            raise ValueError("Failed to authenticate with M-Pesa API")
    
    def _validate_phone_access(self, phone_number):
        """Security check to ensure user can only access their own phone numbers
        
        Args:
            phone_number (str): The phone number to validate access for
            
        Raises:
            ValueError: If the user is not authorized to access this phone number
        """
        if self.username and self.auth_manager:
            # Get the user's registered phone number
            user_phone = self.auth_manager.get_user_phone_number(self.username)
            
            # If phone numbers don't match and user is not admin, deny access
            if user_phone and user_phone != phone_number and not self.auth_manager.is_admin(self.username):
                raise ValueError("You can only access transactions for your registered phone number.")
    
    def _format_phone_number(self, phone_number):
        """Format a phone number to the expected format for M-Pesa API
        
        Args:
            phone_number (str): The raw phone number
            
        Returns:
            str: The formatted phone number
        """
        # Remove any non-digit characters
        digits_only = ''.join([c for c in phone_number if c.isdigit()])
        
        # Ensure it starts with the country code (254 for Kenya)
        if digits_only.startswith('0'):
            # Replace leading 0 with 254
            digits_only = '254' + digits_only[1:]
        elif not digits_only.startswith('254'):
            # Add country code if it doesn't exist
            digits_only = '254' + digits_only
        
        return digits_only
    
    def _generate_timestamp(self):
        """Generate a timestamp in the format required by M-Pesa API
        
        Returns:
            str: Timestamp in format YYYYMMDDHHmmss
        """
        return datetime.now().strftime('%Y%m%d%H%M%S')
    
    def _generate_password(self, timestamp):
        """Generate the password required for M-Pesa API transactions
        
        Args:
            timestamp (str): Timestamp in the required format
            
        Returns:
            str: Base64 encoded password
        """
        password_str = f"{self.business_short_code}{self.passkey}{timestamp}"
        return base64.b64encode(password_str.encode()).decode('utf-8')
    
    def register_c2b_url(self, confirmation_url=None, validation_url=None):
        """Register validation and confirmation URLs for C2B transactions
        
        Args:
            confirmation_url (str, optional): URL to receive confirmation after payment
            validation_url (str, optional): URL to validate payment before processing
            
        Returns:
            dict: Registration response
        """
        self._validate_credentials()
        
        if confirmation_url is None:
            confirmation_url = f"{self.callback_url}/confirmation"
        
        if validation_url is None:
            validation_url = f"{self.callback_url}/validation"
        
        url = f"{self.base_url}/mpesa/c2b/v1/registerurl"
        
        headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "ShortCode": self.business_short_code,
            "ResponseType": "Completed",  # "Completed" or "Cancelled"
            "ConfirmationURL": confirmation_url,
            "ValidationURL": validation_url
        }
        
        # In demo mode, simulate a successful registration
        if os.getenv("MPESA_DEMO_MODE", "false").lower() == "true":
            return {
                "ConversationID": f"AG_20230101_1234{uuid.uuid4().hex[:6]}",
                "OriginatorCoversationID": f"10819-{uuid.uuid4().hex[:10]}-1",
                "ResponseDescription": "Success. Request accepted for processing"
            }
        
        # For real API connections
        try:
            response = requests.post(url, json=payload, headers=headers)
            return response.json()
        except Exception as e:
            print(f"Error registering C2B URLs: {e}")
            return {"error": str(e)}
    
    def simulate_c2b_payment(self, phone_number, amount, reference=None, command_id="CustomerPayBillOnline"):
        """Simulate a C2B payment (only works in sandbox environment)
        
        Args:
            phone_number (str): Customer phone number
            amount (float): Payment amount
            reference (str, optional): Payment reference
            command_id (str, optional): Command ID, defaults to CustomerPayBillOnline
            
        Returns:
            dict: Simulation response
        """
        self._validate_credentials()
        self._validate_phone_access(phone_number)
        
        phone_number = self._format_phone_number(phone_number)
        
        if reference is None:
            reference = f"REF{uuid.uuid4().hex[:8]}"
        
        url = f"{self.base_url}/mpesa/c2b/v1/simulate"
        
        headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "ShortCode": self.business_short_code,
            "CommandID": command_id,
            "Amount": str(int(amount)),
            "Msisdn": phone_number,
            "BillRefNumber": reference
        }
        
        # In demo mode, simulate a successful payment
        if os.getenv("MPESA_DEMO_MODE", "false").lower() == "true":
            transaction_id = f"OEI2{uuid.uuid4().hex[:6]}"
            
            # Create a new transaction record
            now = datetime.now()
            transaction = {
                'id': transaction_id,
                'date': now.date(),
                'time': now.strftime('%H:%M:%S'),
                'description': f"Payment to {self.business_short_code} Reference: {reference}",
                'amount': float(amount),
                'type': 'expense',
                'category': categorize_transaction(f"M-PESA Payment Reference: {reference}"),
                'phone_number': phone_number,
                'status': 'completed',
                'reference': reference
            }
            
            # Store the transaction
            self._transaction_store[transaction_id] = transaction
            
            return {
                "ConversationID": f"AG_20230101_1234{uuid.uuid4().hex[:6]}",
                "OriginatorCoversationID": f"10819-{uuid.uuid4().hex[:10]}-1",
                "ResponseDescription": "Accept the service request successfully.",
                "transactionId": transaction_id
            }
        
        # For real API connections
        try:
            response = requests.post(url, json=payload, headers=headers)
            return response.json()
        except Exception as e:
            print(f"Error simulating C2B payment: {e}")
            return {"error": str(e)}
    
    def lipa_na_mpesa_online(self, phone_number, amount, description="Payment", reference=None, transaction_type="CustomerPayBillOnline"):
        """Initiate a Lipa Na M-Pesa Online payment (STK Push)
        
        Args:
            phone_number (str): Customer phone number
            amount (float): Payment amount
            description (str, optional): Transaction description
            reference (str, optional): Payment reference
            transaction_type (str, optional): Transaction type
            
        Returns:
            dict: STK Push response
        """
        self._validate_credentials()
        self._validate_phone_access(phone_number)
        
        phone_number = self._format_phone_number(phone_number)
        
        if reference is None:
            reference = f"REF{uuid.uuid4().hex[:8]}"
        
        timestamp = self._generate_timestamp()
        password = self._generate_password(timestamp)
        
        url = f"{self.base_url}/mpesa/stkpush/v1/processrequest"
        
        headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "BusinessShortCode": self.business_short_code,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": transaction_type,
            "Amount": str(int(amount)),
            "PartyA": phone_number,
            "PartyB": self.business_short_code,
            "PhoneNumber": phone_number,
            "CallBackURL": f"{self.callback_url}/stk_callback",
            "AccountReference": reference,
            "TransactionDesc": description
        }
        
        # In demo mode, simulate a successful STK push
        if os.getenv("MPESA_DEMO_MODE", "false").lower() == "true":
            checkout_request_id = f"ws_CO_0101{uuid.uuid4().hex[:10]}"
            
            # Create a new transaction record
            now = datetime.now()
            transaction_id = f"OEI2{uuid.uuid4().hex[:6]}"
            transaction = {
                'id': transaction_id,
                'date': now.date(),
                'time': now.strftime('%H:%M:%S'),
                'description': description,
                'amount': float(amount),
                'type': 'expense',
                'category': categorize_transaction(description),
                'phone_number': phone_number,
                'status': 'pending',
                'reference': reference,
                'checkout_request_id': checkout_request_id
            }
            
            # Store the transaction
            self._transaction_store[transaction_id] = transaction
            
            return {
                "MerchantRequestID": f"{uuid.uuid4().hex[:10]}",
                "CheckoutRequestID": checkout_request_id,
                "ResponseCode": "0",
                "ResponseDescription": "Success. Request accepted for processing",
                "CustomerMessage": "Success. Request accepted for processing",
                "transactionId": transaction_id
            }
        
        # For real API connections
        try:
            response = requests.post(url, json=payload, headers=headers)
            return response.json()
        except Exception as e:
            print(f"Error initiating STK push: {e}")
            return {"error": str(e)}
    
    def query_stk_status(self, checkout_request_id):
        """Query the status of an STK Push transaction
        
        Args:
            checkout_request_id (str): The CheckoutRequestID from STK push response
            
        Returns:
            dict: Status response
        """
        self._validate_credentials()
        
        timestamp = self._generate_timestamp()
        password = self._generate_password(timestamp)
        
        url = f"{self.base_url}/mpesa/stkpushquery/v1/query"
        
        headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "BusinessShortCode": self.business_short_code,
            "Password": password,
            "Timestamp": timestamp,
            "CheckoutRequestID": checkout_request_id
        }
        
        # In demo mode, check our local transaction store
        if os.getenv("MPESA_DEMO_MODE", "false").lower() == "true":
            # Find transaction by checkout_request_id
            for tx_id, tx in self._transaction_store.items():
                if tx.get('checkout_request_id') == checkout_request_id:
                    # Simulate transaction completion
                    self._transaction_store[tx_id]['status'] = 'completed'
                    
                    return {
                        "ResponseCode": "0",
                        "ResponseDescription": "The service request is processed successfully.",
                        "MerchantRequestID": f"{uuid.uuid4().hex[:10]}",
                        "CheckoutRequestID": checkout_request_id,
                        "ResultCode": "0",
                        "ResultDesc": "The service request is processed successfully."
                    }
            
            # Checkout request not found
            return {
                "ResponseCode": "1032",
                "ResponseDescription": "Request cancelled by user"
            }
        
        # For real API connections
        try:
            response = requests.post(url, json=payload, headers=headers)
            return response.json()
        except Exception as e:
            print(f"Error querying STK status: {e}")
            return {"error": str(e)}
    
    def query_transaction_status(self, transaction_id, identifier_type="1"):
        """Query the status of a transaction
        
        Args:
            transaction_id (str): Transaction ID to query
            identifier_type (str, optional): Type of identifier
                1: MSISDN
                2: Till Number
                3: Organization shortcode
                4: Transaction ID
            
        Returns:
            dict: Status response
        """
        self._validate_credentials()
        
        url = f"{self.base_url}/mpesa/transactionstatus/v1/query"
        
        headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "Initiator": "testapi",  # This should be the username of the M-Pesa API operator
            "SecurityCredential": self._generate_security_credential(),
            "CommandID": "TransactionStatusQuery",
            "TransactionID": transaction_id,
            "PartyA": self.business_short_code,
            "IdentifierType": identifier_type,
            "ResultURL": f"{self.callback_url}/result",
            "QueueTimeOutURL": f"{self.callback_url}/timeout",
            "Remarks": "Transaction status query",
            "Occasion": "Transaction status query"
        }
        
        # In demo mode, check our local transaction store
        if os.getenv("MPESA_DEMO_MODE", "false").lower() == "true":
            if transaction_id in self._transaction_store:
                tx = self._transaction_store[transaction_id]
                
                return {
                    "Result": {
                        "ResultType": 0,
                        "ResultCode": 0,
                        "ResultDesc": "The service request is processed successfully.",
                        "OriginatorConversationID": f"{uuid.uuid4().hex[:10]}",
                        "ConversationID": f"{uuid.uuid4().hex[:10]}",
                        "TransactionID": transaction_id,
                        "ResultParameters": {
                            "ResultParameter": [
                                {"Key": "TransactionAmount", "Value": tx['amount']},
                                {"Key": "TransactionReceipt", "Value": transaction_id},
                                {"Key": "TransactionCompletedDateTime", "Value": f"{tx['date']} {tx['time']}"},
                                {"Key": "ReceiverPartyPublicName", "Value": "SAFARICOM PLC - MPESA"},
                                {"Key": "B2CChargesPaidAccountAvailableFunds", "Value": ""},
                                {"Key": "B2CRecipientIsRegisteredCustomer", "Value": "Y"},
                                {"Key": "TransactionStatus", "Value": tx['status'].upper()}
                            ]
                        }
                    }
                }
            else:
                return {
                    "ErrorCode": "404.001.03",
                    "ErrorMessage": "Transaction not found"
                }
        
        # For real API connections
        try:
            response = requests.post(url, json=payload, headers=headers)
            return response.json()
        except Exception as e:
            print(f"Error querying transaction status: {e}")
            return {"error": str(e)}
    
    def _generate_security_credential(self):
        """Generate security credential by encrypting the password with the M-Pesa public key
        
        Returns:
            str: Base64 encoded security credential
        """
        # In a real implementation, this would use a certificate to encrypt
        # For demo purposes, we'll just return a dummy credential
        return "Dummy-Security-Credential"
    
    def process_c2b_callback(self, callback_data):
        """Process a C2B callback request from M-Pesa API
        
        Args:
            callback_data (dict): Callback data from M-Pesa API
            
        Returns:
            dict: Processing result
        """
        transaction_id = callback_data.get("TransID")
        
        if not transaction_id:
            return {"error": "Missing transaction ID"}
        
        # Extract transaction details
        transaction = {
            'id': transaction_id,
            'date': datetime.now().date(),  # Callback should include date
            'time': datetime.now().strftime('%H:%M:%S'),  # Callback should include time
            'description': f"Payment to {callback_data.get('BusinessShortCode')} Reference: {callback_data.get('BillRefNumber')}",
            'amount': float(callback_data.get('TransAmount', 0)),
            'type': 'expense',
            'category': categorize_transaction(f"M-PESA Payment Reference: {callback_data.get('BillRefNumber')}"),
            'phone_number': callback_data.get('MSISDN'),
            'status': 'completed',
            'reference': callback_data.get('BillRefNumber')
        }
        
        # Store the transaction
        self._transaction_store[transaction_id] = transaction
        
        return {"success": True, "transactionId": transaction_id}
    
    def process_stk_callback(self, callback_data):
        """Process an STK Push callback request from M-Pesa API
        
        Args:
            callback_data (dict): Callback data from M-Pesa API
            
        Returns:
            dict: Processing result
        """
        body = callback_data.get("Body", {})
        result = body.get("stkCallback", {})
        checkout_request_id = result.get("CheckoutRequestID")
        
        if not checkout_request_id:
            return {"error": "Missing checkout request ID"}
        
        # Find transaction by checkout_request_id
        for tx_id, tx in self._transaction_store.items():
            if tx.get('checkout_request_id') == checkout_request_id:
                # Update transaction status
                if result.get("ResultCode") == 0:
                    self._transaction_store[tx_id]['status'] = 'completed'
                else:
                    self._transaction_store[tx_id]['status'] = 'failed'
                
                return {"success": True, "transactionId": tx_id}
        
        # Transaction not found, create a new one from callback data
        if result.get("ResultCode") == 0:
            # Extract item from callback metadata
            metadata = result.get("CallbackMetadata", {}).get("Item", [])
            amount = next((item.get("Value") for item in metadata if item.get("Name") == "Amount"), 0)
            mpesa_receipt = next((item.get("Value") for item in metadata if item.get("Name") == "MpesaReceiptNumber"), "")
            phone = next((item.get("Value") for item in metadata if item.get("Name") == "PhoneNumber"), "")
            
            transaction = {
                'id': mpesa_receipt,
                'date': datetime.now().date(),
                'time': datetime.now().strftime('%H:%M:%S'),
                'description': f"STK Push Payment",
                'amount': float(amount),
                'type': 'expense',
                'category': 'Other',
                'phone_number': phone,
                'status': 'completed',
                'reference': '',
                'checkout_request_id': checkout_request_id
            }
            
            # Store the transaction
            self._transaction_store[mpesa_receipt] = transaction
            
            return {"success": True, "transactionId": mpesa_receipt}
        
        return {"success": False, "error": f"Transaction failed with code {result.get('ResultCode')}"}
    
    def get_transactions(self, phone_number, start_date, end_date):
        """Get M-Pesa transactions for a specific phone number and date range
        
        Args:
            phone_number (str): The phone number
            start_date (date): Start date for transaction query
            end_date (date): End date for transaction query
            
        Returns:
            list: List of transaction dictionaries
        """
        self._validate_credentials()
        self._validate_phone_access(phone_number)
        
        phone_number = self._format_phone_number(phone_number)
        
        # In a real implementation, this would call the M-Pesa API's Transaction History
        # or query a database of stored transactions
        
        # In demo mode, return our local transaction store
        if os.getenv("MPESA_DEMO_MODE", "true").lower() == "true":
            # Filter transactions for the given phone number and date range
            filtered_transactions = []
            
            # If no real transactions, generate sample data
            if not self._transaction_store:
                # Generate sample transactions for the demo
                self._generate_sample_transactions(phone_number, start_date)
            
            for tx_id, tx in self._transaction_store.items():
                # Convert date to datetime.date if it's a string
                tx_date = tx['date'] if hasattr(tx['date'], 'year') else datetime.strptime(tx['date'], '%Y-%m-%d').date()
                tx_phone = tx.get('phone_number', '')
                
                if (tx_phone == phone_number or not tx_phone) and start_date <= tx_date <= end_date:
                    # Format to match the expected output
                    filtered_transactions.append({
                        'date': tx_date,
                        'description': tx['description'],
                        'amount': float(tx['amount']),
                        'type': tx['type'],
                        'category': tx['category']
                    })
            
            # If still no transactions, return sample transactions
            if not filtered_transactions:
                return self._generate_sample_transactions(phone_number, start_date)
                
            return filtered_transactions
        
        # For real API connection, implement the Transaction History API call
        # This is a placeholder for the real implementation
        url = f"{self.base_url}/mpesa/transactionhistory/v1/query"
        
        headers = {
            "Authorization": f"Bearer {self.auth_token}",
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
        
        try:
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
                        'category': categorize_transaction(item.get('Description', ''))
                    }
                    transactions.append(transaction)
                    
                return transactions
            else:
                print(f"Error getting transactions: {response.text}")
                return self._generate_sample_transactions(phone_number, start_date)
        except Exception as e:
            print(f"Exception getting transactions: {e}")
            return self._generate_sample_transactions(phone_number, start_date)
    
    def _generate_sample_transactions(self, phone_number, start_date):
        """Generate sample transactions for demo purposes
        
        Args:
            phone_number (str): Phone number to generate transactions for
            start_date (date): Start date for transactions
            
        Returns:
            list: List of sample transaction dictionaries
        """
        sample_transactions = [
            {
                'date': start_date + timedelta(days=2),
                'description': 'M-PESA Payment to Grocery Store',
                'amount': 2500.0,
                'type': 'expense',
                'category': 'Food'
            },
            {
                'date': start_date + timedelta(days=4),
                'description': 'M-PESA Payment to Uber',
                'amount': 750.0,
                'type': 'expense',
                'category': 'Transport'
            },
            {
                'date': start_date + timedelta(days=7),
                'description': 'M-PESA Payment to KPLC',
                'amount': 3200.0,
                'type': 'expense',
                'category': 'Utilities'
            },
            {
                'date': start_date + timedelta(days=10),
                'description': 'Salary from Employer via M-PESA',
                'amount': 45000.0,
                'type': 'income',
                'category': 'Salary'
            },
            {
                'date': start_date + timedelta(days=15),
                'description': 'M-PESA Payment to Netflix',
                'amount': 1100.0,
                'type': 'expense',
                'category': 'Entertainment'
            },
            {
                'date': start_date + timedelta(days=20),
                'description': 'M-PESA Payment to Pharmacy',
                'amount': 850.0,
                'type': 'expense',
                'category': 'Healthcare'
            },
            {
                'date': start_date + timedelta(days=25),
                'description': 'M-PESA Payment to Landlord',
                'amount': 18000.0,
                'type': 'expense',
                'category': 'Housing'
            }
        ]
        
        # Store samples in the transaction store for future reference
        for idx, tx in enumerate(sample_transactions):
            tx_id = f"DEMO{uuid.uuid4().hex[:8]}"
            self._transaction_store[tx_id] = {
                'id': tx_id,
                'date': tx['date'],
                'time': '09:00:00',
                'description': tx['description'],
                'amount': tx['amount'],
                'type': tx['type'],
                'category': tx['category'],
                'phone_number': phone_number,
                'status': 'completed',
                'reference': f"REF{idx+100}"
            }
        
        return sample_transactions
