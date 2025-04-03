import os
import pandas as pd
from datetime import datetime, date

class BudgetManager:
    """Class to manage budget planning and tracking"""
    
    def __init__(self, username=None, data_dir="data"):
        """Initialize the budget manager with a username for storage
        
        Args:
            username (str): Username for per-user storage (if None, uses shared storage)
            data_dir (str): Base directory for data storage
        """
        self.username = username
        self.data_dir = data_dir
        self.ensure_budget_file_exists()
        
    def _get_file_path(self):
        """Get the file path for the current user's budget
        
        Returns:
            str: Path to the user's budget data file
        """
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            
        if self.username:
            filename = f"budget_{self.username}.csv"
        else:
            filename = "budget.csv"
            
        return os.path.join(self.data_dir, filename)
        
    def ensure_budget_file_exists(self):
        """Create budget file if it doesn't exist"""
        budget_file = self._get_file_path()
        
        if not os.path.exists(budget_file):
            # Create default columns for budget file
            df = pd.DataFrame(columns=[
                'category', 
                'amount', 
                'period',  # 'monthly', 'yearly', 'weekly'
                'start_date',
                'end_date',
                'created_at',
                'modified_at'
            ])
            
            df.to_csv(budget_file, index=False)
    
    def get_budgets(self):
        """Get all budget items as a pandas DataFrame"""
        budget_file = self._get_file_path()
        
        try:
            df = pd.read_csv(budget_file, parse_dates=['start_date', 'end_date', 'created_at', 'modified_at'])
            return df
        except pd.errors.EmptyDataError:
            # Return empty DataFrame with correct columns
            return pd.DataFrame(columns=[
                'category', 
                'amount', 
                'period',
                'start_date',
                'end_date',
                'created_at',
                'modified_at'
            ])
    
    def add_budget(self, budget_item):
        """Add a new budget item to the CSV file
        
        Args:
            budget_item (dict): A dictionary containing budget details
                Required keys: category, amount, period
                Optional keys: start_date, end_date
        """
        if not all(k in budget_item for k in ['category', 'amount', 'period']):
            raise ValueError("Budget item must contain category, amount, and period")
        
        today = datetime.now().date()
        
        # Set default dates if not provided
        if 'start_date' not in budget_item or not budget_item['start_date']:
            budget_item['start_date'] = today
            
        if 'end_date' not in budget_item or not budget_item['end_date']:
            # Set default end date based on period
            if budget_item['period'] == 'monthly':
                # One month from start
                if isinstance(budget_item['start_date'], str):
                    start = datetime.strptime(budget_item['start_date'], '%Y-%m-%d').date()
                else:
                    start = budget_item['start_date']
                
                # Simple approximation: +30 days
                end_date = date(start.year + (start.month + 1) // 12, 
                                (start.month + 1) % 12 or 12, 
                                min(start.day, 28))
                budget_item['end_date'] = end_date
            elif budget_item['period'] == 'yearly':
                # One year from start
                if isinstance(budget_item['start_date'], str):
                    start = datetime.strptime(budget_item['start_date'], '%Y-%m-%d').date()
                else:
                    start = budget_item['start_date']
                    
                end_date = date(start.year + 1, start.month, min(start.day, 28))
                budget_item['end_date'] = end_date
            elif budget_item['period'] == 'weekly':
                # 7 days from start
                if isinstance(budget_item['start_date'], str):
                    start = datetime.strptime(budget_item['start_date'], '%Y-%m-%d').date()
                else:
                    start = budget_item['start_date']
                    
                from datetime import timedelta
                budget_item['end_date'] = start + timedelta(days=7)
            else:
                budget_item['end_date'] = today  # Default to today
        
        # Add timestamps
        budget_item['created_at'] = datetime.now()
        budget_item['modified_at'] = datetime.now()
        
        # Convert to DataFrame
        new_df = pd.DataFrame([budget_item])
        
        # Append to existing data
        all_df = self.get_budgets()
        combined_df = pd.concat([all_df, new_df], ignore_index=True)
        
        # Save to file
        combined_df.to_csv(self._get_file_path(), index=False)
    
    def update_budget(self, budget_idx, updates):
        """Update a budget item
        
        Args:
            budget_idx (int): Index of the budget item to update
            updates (dict): Dictionary of fields to update
        """
        df = self.get_budgets()
        
        if budget_idx >= len(df):
            raise IndexError(f"Budget index {budget_idx} out of range")
        
        # Apply updates
        for key, value in updates.items():
            if key in df.columns:
                df.at[budget_idx, key] = value
        
        # Update modified timestamp
        df.at[budget_idx, 'modified_at'] = datetime.now()
        
        # Save to file
        df.to_csv(self._get_file_path(), index=False)
    
    def delete_budget(self, budget_idx):
        """Delete a budget item by its index
        
        Args:
            budget_idx (int): The index of the budget item to delete
        """
        df = self.get_budgets()
        
        if budget_idx >= len(df):
            raise IndexError(f"Budget index {budget_idx} out of range")
        
        # Drop the row
        df = df.drop(budget_idx).reset_index(drop=True)
        
        # Save to file
        df.to_csv(self._get_file_path(), index=False)
    
    def get_active_budgets(self, as_of_date=None):
        """Get all active budgets as of a specific date
        
        Args:
            as_of_date (date, optional): Date to check. Defaults to today.
        
        Returns:
            DataFrame: Active budgets
        """
        if as_of_date is None:
            as_of_date = datetime.now().date()
            
        if isinstance(as_of_date, str):
            as_of_date = datetime.strptime(as_of_date, '%Y-%m-%d').date()
            
        df = self.get_budgets()
        
        if df.empty:
            return df
        
        # Filter for active budgets (where start_date <= as_of_date <= end_date)
        return df[(df['start_date'].dt.date <= as_of_date) & 
                 (df['end_date'].dt.date >= as_of_date)]
    
    def get_budget_by_category(self, category, active_only=True, as_of_date=None):
        """Get budget for a specific category
        
        Args:
            category (str): Category to filter by
            active_only (bool): If True, only returns active budgets
            as_of_date (date, optional): Date to check for active budgets. Defaults to today.
            
        Returns:
            DataFrame: Filtered budgets
        """
        if active_only:
            df = self.get_active_budgets(as_of_date)
        else:
            df = self.get_budgets()
            
        if df.empty:
            return df
            
        return df[df['category'] == category]
    
    def calculate_budget_progress(self, data_manager, as_of_date=None):
        """Calculate budget progress based on actual transactions
        
        Args:
            data_manager (DataManager): Data manager instance to get transactions
            as_of_date (date, optional): Date to check. Defaults to today.
            
        Returns:
            DataFrame: Budget progress with actual spending and percentage used
        """
        if as_of_date is None:
            as_of_date = datetime.now().date()
            
        if isinstance(as_of_date, str):
            as_of_date = datetime.strptime(as_of_date, '%Y-%m-%d').date()
            
        # Get active budgets
        budgets = self.get_active_budgets(as_of_date)
        
        if budgets.empty:
            return pd.DataFrame(columns=['category', 'budget_amount', 'actual_amount', 'remaining', 'percentage_used'])
        
        # Get all transactions from data manager
        transactions = data_manager.get_transactions()
        
        if transactions.empty:
            # If no transactions, return budgets with zero actual spending
            result = []
            for _, budget in budgets.iterrows():
                result.append({
                    'category': budget['category'],
                    'budget_amount': budget['amount'],
                    'actual_amount': 0,
                    'remaining': budget['amount'],
                    'percentage_used': 0
                })
            return pd.DataFrame(result)
        
        # Calculate actual spending for each budget
        result = []
        for _, budget in budgets.iterrows():
            # Filter transactions by category and date range
            category_transactions = transactions[
                (transactions['category'] == budget['category']) &
                (transactions['date'] >= budget['start_date']) &
                (transactions['date'] <= budget['end_date'])
            ]
            
            # Calculate spending (only expenses count against budget)
            if category_transactions.empty:
                actual_amount = 0
            else:
                # Filter for expenses (where amount is negative)
                expense_transactions = category_transactions[category_transactions['type'] == 'expense']
                actual_amount = expense_transactions['amount'].sum() if not expense_transactions.empty else 0
            
            # Calculate remaining budget and percentage
            remaining = budget['amount'] - actual_amount
            percentage_used = (actual_amount / budget['amount']) * 100 if budget['amount'] > 0 else 0
            
            result.append({
                'category': budget['category'],
                'budget_amount': budget['amount'],
                'actual_amount': actual_amount,
                'remaining': remaining,
                'percentage_used': percentage_used
            })
            
        return pd.DataFrame(result)