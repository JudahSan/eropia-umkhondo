import pytest
from auth_manager import AuthManager

def test_auth_manager_initialization(auth_manager):
    """Test that AuthManager initializes correctly"""    
    # Verify the config was loaded
    assert auth_manager.credentials is not None
    assert 'usernames' in auth_manager.credentials
    assert 'testuser' in auth_manager.credentials['usernames']

def test_get_user_info(auth_manager):
    """Test getting user information"""    
    # Test getting valid user
    user_info = auth_manager.get_user_info('testuser')
    assert user_info is not None
    assert user_info['email'] == 'testuser@example.com'
    assert user_info['name'] == 'Test User'
    
    # Test getting invalid user
    user_info = auth_manager.get_user_info('nonexistent')
    assert user_info is None

def test_get_user_phone_number(auth_manager):
    """Test getting user phone number"""    
    # Test getting valid user phone
    phone = auth_manager.get_user_phone_number('testuser')
    assert phone == '2547123456789'
    
    # Test getting invalid user phone
    phone = auth_manager.get_user_phone_number('nonexistent')
    assert phone is None

def test_is_admin(auth_manager):
    """Test admin role check"""    
    # Test regular user
    assert not auth_manager.is_admin('testuser')
    
    # Update user to admin role
    auth_manager.credentials['usernames']['testuser']['role'] = 'admin'
    assert auth_manager.is_admin('testuser')
    
    # Test nonexistent user
    assert not auth_manager.is_admin('nonexistent')