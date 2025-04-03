import pandas as pd
import os
import json
from datetime import datetime

class DataManager:
    """Class to manage transaction data storage and retrieval"""
    
    def __init__(self, username=None, data_dir="data"):
        """Initialize the data manager with a username for storage
        
        Args:
            username (str): Username for per-user storage (if None, uses shared storage)
            data_dir (str): Base directory for data storage
        """
        self.username = username
        self.data_dir = data_dir
        self.file_path = self._get_file_path()
        self.ensure_data_file_exists()
    
    def _get_file_path(self):
        """Get the file path for the current user
        
        Returns:
            str: Path to the user's transaction data file
        """
        if self.username:
            # Use user-specific file
            return os.path.join(self.data_dir, f"transactions_{self.username}.csv")
        else:
            # Use shared file (for backward compatibility)
            return os.path.join(self.data_dir, "transactions.csv")
    
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
                'category', 'source', 'user_id'
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
                
                # Filter by username if set
                if self.username and 'user_id' in df.columns:
                    df = df[df['user_id'] == self.username]
            
            return df
        except Exception as e:
            print(f"Error reading transactions: {e}")
            # Return an empty DataFrame with the correct columns
            return pd.DataFrame(columns=[
                'date', 'description', 'amount', 'type', 
                'category', 'source', 'user_id'
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
            
            # Add user_id to transaction if not present
            if 'user_id' not in transaction and self.username:
                transaction['user_id'] = self.username
                
            # Read existing transactions
            df = self.get_transactions()
            
            # Convert to DataFrame and append
            new_df = pd.DataFrame([transaction])
            
            # Read all transactions (without user filtering)
            try:
                all_df = pd.read_csv(self.file_path)
            except:
                all_df = pd.DataFrame(columns=new_df.columns)
                
            # Combine and save
            combined_df = pd.concat([all_df, new_df], ignore_index=True)
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
            # Read all transactions
            all_df = pd.read_csv(self.file_path)
            
            # Ensure we're only updating the user's own transactions
            if self.username and 'user_id' in all_df.columns:
                if transaction_idx not in all_df.index or all_df.loc[transaction_idx, 'user_id'] != self.username:
                    print("Unauthorized attempt to update transaction")
                    return False
            
            # Update the category
            all_df.loc[transaction_idx, 'category'] = new_category
            
            # Save back to CSV
            all_df.to_csv(self.file_path, index=False)
            
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
            # Read all transactions
            all_df = pd.read_csv(self.file_path)
            
            # Ensure we're only deleting the user's own transactions
            if self.username and 'user_id' in all_df.columns:
                if transaction_idx not in all_df.index or all_df.loc[transaction_idx, 'user_id'] != self.username:
                    print("Unauthorized attempt to delete transaction")
                    return False
            
            # Remove the transaction
            all_df = all_df.drop(transaction_idx)
            
            # Save back to CSV
            all_df.to_csv(self.file_path, index=False)
            
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
            
        # Convert dates to pandas datetime format for consistent comparison
        start_date_pd = pd.to_datetime(start_date)
        end_date_pd = pd.to_datetime(end_date)
        
        # Ensure df['date'] is pandas datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Filter by date range
        mask = (df['date'] >= start_date_pd) & (df['date'] <= end_date_pd)
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
