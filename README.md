# Eropia umkhondo - Money Tracker

A financial tracking application that visualizes personal and M-Pesa transaction data.

## About

"Eropia" is a Maasai word meaning "money" or "wealth", and "umkhondo" comes from Zulu meaning "track" or "trail". Together, they represent our mission to help you track your money across different cultures and financial systems.

## Features

- 📊 Visual Analytics: See where your money goes with intuitive charts and reports
- 📱 M-Pesa Integration: Automatically import your M-Pesa transactions
- 🔒 Secure & Private: Your financial data stays private and secure
- 📊 Interactive Dashboards: View your spending patterns with interactive charts
- 📋 Transaction Management: Add, edit, and categorize your transactions
- 📱 Mobile Responsive: Use on any device with a responsive design

## Installation

1. Clone the repository
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file based on `.env.example` and add your M-Pesa API credentials

## Usage

Run the Streamlit app:

```
streamlit run app.py
```

### Demo User

You can log in with the following demo credentials:
- Username: demo
- Password: password

## M-Pesa API Integration

To use the M-Pesa integration:

1. Register on the [Safaricom Developer Portal](https://developer.safaricom.co.ke/)
2. Create a new app to get API credentials
3. Add your credentials to the `.env` file:
   ```
   MPESA_CONSUMER_KEY=your_consumer_key
   MPESA_CONSUMER_SECRET=your_consumer_secret
   MPESA_API_URL=https://sandbox.safaricom.co.ke
   ```

## Testing

Run the tests with pytest:

```bash
# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run tests for a specific module
pytest tests/test_utils.py

# Run tests with coverage report
pytest --cov=.
```

## Directory Structure

```
├── app.py                  # Main application file
├── auth_manager.py         # User authentication management
├── data_manager.py         # Transaction data management
├── mpesa_api.py            # M-Pesa API integration
├── utils.py                # Utility functions
├── visualization.py        # Data visualization functions
├── .env                    # Environment variables (create from .env.example)
├── .streamlit/             # Streamlit configuration
│   └── config.toml
├── auth_config.yaml        # Authentication configuration
├── data/                   # Transaction data storage
│   └── transactions.csv
└── pages/                  # Streamlit pages
    ├── dashboard.py        # Dashboard page
    ├── landing.py          # Landing page
    ├── login.py            # Login page
    └── register.py         # Registration page
└── tests/                  # Test files
    ├── test_auth_manager.py
    ├── test_data_manager.py
    └── test_utils.py
```

## License

MIT License