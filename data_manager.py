import pandas as pd
import os
import json
from datetime import datetime

class DataManager:
    """Class to manage transaction data storage and retrieval"""
    
    def __init__(self, file_path="data/transactions.csv"):
        """Initialize the data manager with a file path for storage"""
        self.file_path = file_path
        self.ensure_data_file_exists()
    
    def ensure_data_file_exists(self):
        """Create data directory and file if they don't exist"""
        directory = os.path.dirname(self.file_path)
        
        # Create directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # Create file with headers if it doesn't exist
        if not os.path.exists(self.file_path):
            # Create an empty DataFrame with the required columns
            empty_df = pd.DataFrame(columns=[
                'date', 'description', 'amount', 'type', 
                'category', 'source'
            ])
            empty_df.to_csv(self.file_path, index=False)
    
    def get_transactions(self):
        """Get all transactions as a pandas DataFrame"""
        try:
            # Read the CSV file
            df = pd.read_csv(self.file_path)
            
            # Convert date strings to datetime objects
            if not df.empty:
                df['date'] = pd.to_datetime(df['date'])
            
            return df
        except Exception as e:
            print(f"Error reading transactions: {e}")
            # Return an empty DataFrame with the correct columns
            return pd.DataFrame(columns=[
                'date', 'description', 'amount', 'type', 
                'category', 'source'
            ])
    
    def add_transaction(self, transaction):
        """Add a new transaction to the CSV file
        
        Args:
            transaction (dict): A dictionary containing transaction details
        """
        try:
            # Convert transaction date to string if it's a datetime object
            if isinstance(transaction['date'], datetime):
                transaction['date'] = transaction['date'].strftime('%Y-%m-%d')
                
            # Read existing transactions
            df = self.get_transactions()
            
            # Convert to DataFrame and append
            new_df = pd.DataFrame([transaction])
            
            # Combine and save
            combined_df = pd.concat([df, new_df], ignore_index=True)
            combined_df.to_csv(self.file_path, index=False)
            
            return True
        except Exception as e:
            print(f"Error adding transaction: {e}")
            return False
    
    def update_transaction_category(self, transaction_idx, new_category):
        """Update the category of a specific transaction
        
        Args:
            transaction_idx (int): The index of the transaction to update
            new_category (str): The new category to assign
        """
        try:
            # Read existing transactions
            df = self.get_transactions()
            
            # Update the category
            df.loc[transaction_idx, 'category'] = new_category
            
            # Save back to CSV
            df.to_csv(self.file_path, index=False)
            
            return True
        except Exception as e:
            print(f"Error updating transaction: {e}")
            return False
    
    def delete_transaction(self, transaction_idx):
        """Delete a transaction by its index
        
        Args:
            transaction_idx (int): The index of the transaction to delete
        """
        try:
            # Read existing transactions
            df = self.get_transactions()
            
            # Remove the transaction
            df = df.drop(transaction_idx)
            
            # Save back to CSV
            df.to_csv(self.file_path, index=False)
            
            return True
        except Exception as e:
            print(f"Error deleting transaction: {e}")
            return False
    
    def get_transactions_by_date_range(self, start_date, end_date):
        """Get transactions within a specific date range
        
        Args:
            start_date (datetime): Start date for filtering
            end_date (datetime): End date for filtering
            
        Returns:
            DataFrame: Filtered transactions
        """
        df = self.get_transactions()
        
        if df.empty:
            return df
            
        # Filter by date range
        mask = (df['date'] >= start_date) & (df['date'] <= end_date)
        return df[mask]
    
    def get_transactions_by_category(self, category):
        """Get transactions for a specific category
        
        Args:
            category (str): Category to filter by
            
        Returns:
            DataFrame: Filtered transactions
        """
        df = self.get_transactions()
        
        if df.empty:
            return df
            
        # Filter by category
        return df[df['category'] == category]
