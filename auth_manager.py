import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import os
import bcrypt
from datetime import datetime, timedelta

class AuthManager:
    """Class to manage user authentication and authorization"""
    
    def __init__(self, config_path="auth_config.yaml"):
        """Initialize the authentication manager with a config file path
        
        Args:
            config_path (str): Path to the YAML configuration file
        """
        self.config_path = config_path
        self.credentials = self._load_credentials()
        
    def _load_credentials(self):
        """Load user credentials from the YAML file
        
        Returns:
            dict: User credentials configuration
        """
        # Create default config if not exists
        if not os.path.exists(self.config_path):
            self._create_default_config()
            
        # Load the file
        with open(self.config_path, 'r') as file:
            return yaml.load(file, Loader=SafeLoader)
            
    def _save_credentials(self):
        """Save the current credentials to the YAML file"""
        with open(self.config_path, 'w') as file:
            yaml.dump(self.credentials, file)
            
    def _create_default_config(self):
        """Create a default configuration file with a demo user"""
        # Generate password for demo user
        hasher = stauth.Hasher()
        hashed_password = hasher.hash('password')
        
        # Default configuration with a demo user
        default_config = {
            'credentials': {
                'usernames': {
                    'demo': {
                        'name': 'Demo User',
                        'password': hashed_password,
                        'phone_number': '254712345678',
                        'email': 'demo@example.com'
                    }
                }
            },
            'cookie': {
                'expiry_days': 30,
                'key': 'finance_tracker_auth',
                'name': 'finance_tracker_auth'
            },
            'preauthorized': {
                'emails': []
            }
        }
        
        # Write to file
        with open(self.config_path, 'w') as file:
            yaml.dump(default_config, file)
            
    def setup_auth(self):
        """Set up the authentication system and handle login/logout
        
        Returns:
            tuple: (authenticator, authentication_status, username)
        """
        # Create authenticator
        authenticator = stauth.Authenticate(
            self.credentials['credentials'],
            self.credentials['cookie']['name'],
            self.credentials['cookie']['key'],
            self.credentials['cookie']['expiry_days'],
            self.credentials['preauthorized']['emails']
        )
        
        # Get authentication status - using 'main' location for v0.2.2
        name, authentication_status, username = authenticator.login('Login', 'main')
        
        return authenticator, authentication_status, username
        
    def register_user(self, username, name, password, email, phone_number):
        """Register a new user in the system
        
        Args:
            username (str): Username for login
            name (str): Display name
            password (str): Plain text password (will be hashed)
            email (str): User email
            phone_number (str): User phone number
            
        Returns:
            bool: True if registration successful, False otherwise
        """
        # Check if username already exists
        if username in self.credentials['credentials']['usernames']:
            return False
            
        # Hash the password - for v0.2.2, Hasher takes a list of passwords
        hashed_password = stauth.Hasher([password]).generate()[0]
        
        # Add user to credentials
        self.credentials['credentials']['usernames'][username] = {
            'name': name,
            'password': hashed_password,
            'email': email,
            'phone_number': phone_number
        }
        
        # Save updated credentials
        self._save_credentials()
        
        return True
        
    def get_user_info(self, username):
        """Get user information
        
        Args:
            username (str): Username to look up
            
        Returns:
            dict: User information or None if not found
        """
        if username in self.credentials['credentials']['usernames']:
            return self.credentials['credentials']['usernames'][username]
        return None
        
    def update_user_info(self, username, info_dict):
        """Update user information
        
        Args:
            username (str): Username to update
            info_dict (dict): Dictionary of info to update
            
        Returns:
            bool: True if update successful, False otherwise
        """
        if username not in self.credentials['credentials']['usernames']:
            return False
            
        # Update user info
        for key, value in info_dict.items():
            if key != 'password':  # Passwords need special handling
                self.credentials['credentials']['usernames'][username][key] = value
                
        # Save updated credentials
        self._save_credentials()
        
        return True
        
    def change_password(self, username, new_password):
        """Change a user's password
        
        Args:
            username (str): Username to update
            new_password (str): New password (will be hashed)
            
        Returns:
            bool: True if update successful, False otherwise
        """
        if username not in self.credentials['credentials']['usernames']:
            return False
            
        # Hash the new password - for v0.2.2, Hasher takes a list of passwords
        hashed_password = stauth.Hasher([new_password]).generate()[0]
        
        # Update password
        self.credentials['credentials']['usernames'][username]['password'] = hashed_password
        
        # Save updated credentials
        self._save_credentials()
        
        return True
        
    def get_user_phone_number(self, username):
        """Get a user's phone number
        
        Args:
            username (str): Username to look up
            
        Returns:
            str: User's phone number or None if not found
        """
        user_info = self.get_user_info(username)
        if user_info and 'phone_number' in user_info:
            return user_info['phone_number']
        return None
        
    def is_admin(self, username):
        """Check if the user is an admin
        
        Args:
            username (str): Username to check
            
        Returns:
            bool: True if the user is an admin, False otherwise
        """
        user_info = self.get_user_info(username)
        if user_info and 'role' in user_info and user_info['role'] == 'admin':
            return True
        return False