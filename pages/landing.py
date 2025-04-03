import streamlit as st
from financial_tips import get_general_tip, get_tips_by_category
from tip_widget import tip_widget_button, display_tip_widget

def app():
    # Custom CSS for better styling of the landing page
    st.markdown("""
    <style>
    /* Hide sidebar completely */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* Main container styling */
    .block-container {
        max-width: 100% !important;
        padding: 0 !important;
    }
    
    .appview-container .main .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }
    
    /* Hero section */
    .hero-container {
        text-align: center;
        padding: 5rem 1rem;
        background: linear-gradient(135deg, #1E3A8A 0%, #1E88E5 100%);
        color: white;
        margin-bottom: 3rem;
    }
    
    .hero-title {
        font-size: 4.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 0px 2px 4px rgba(0,0,0,0.2);
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        margin-bottom: 2rem;
        font-weight: 300;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* Feature section */
    .feature-section {
        padding: 3rem 1rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin-bottom: 3rem;
    }
    
    .feature-card {
        background-color: white;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        padding: 2rem;
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1.5rem;
        color: #1E88E5;
    }
    
    .feature-title {
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
        color: #1E3A8A;
    }
    
    .feature-text {
        font-size: 1.1rem;
        color: #4B5563;
        line-height: 1.6;
    }
    
    /* CTA section */
    .cta-container {
        text-align: center;
        padding: 4rem 1rem;
        background-color: #F3F4F6;
        margin-bottom: 3rem;
    }
    
    .cta-title {
        font-size: 2.5rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        color: #1E3A8A;
    }
    
    .cta-text {
        font-size: 1.2rem;
        margin-bottom: 2rem;
        color: #4B5563;
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.7;
    }
    
    /* Cultural context section */
    .context-section {
        text-align: center;
        padding: 3rem 1rem;
        max-width: 1000px;
        margin: 0 auto;
    }
    
    .context-title {
        color: #1E3A8A;
        font-size: 1.8rem;
        margin-bottom: 1.5rem;
    }
    
    .context-text {
        color: #4B5563;
        font-size: 1.1rem;
        line-height: 1.7;
    }
    
    /* Footer styling */
    .footer-container {
        text-align: center;
        padding: 3rem 1rem;
        background-color: #1E3A8A;
        color: white;
        margin-top: 2rem;
    }
    
    .footer-text {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.8);
    }
    
    /* Responsive styling */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.8rem;
        }
        
        .hero-subtitle {
            font-size: 1.2rem;
        }
        
        .feature-grid {
            grid-template-columns: 1fr;
        }
        
        .cta-title {
            font-size: 2rem;
        }
        
        .cta-text {
            font-size: 1.1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Hide the main menu and footer
    st.markdown(
        """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Top Navigation
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("# Eropia umkhondo")
    with col2:
        # Check if user is logged in
        if "username" in st.session_state:
            # Show logout button
            if st.button("Logout", key="nav_logout", use_container_width=True):
                # Clear session state and go back to landing
                for key in list(st.session_state.keys()):
                    if key != "current_page":
                        del st.session_state[key]
                st.rerun()
        else:
            # Show login/register buttons if not logged in
            cols = st.columns(2)
            with cols[0]:
                if st.button("Login", key="nav_login", use_container_width=True):
                    st.session_state.current_page = "login"
                    st.rerun()
            with cols[1]:
                if st.button("Register", key="nav_register", use_container_width=True):
                    st.session_state.current_page = "register"
                    st.rerun()
    
    # Hero Section
    st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">Eropia umkhondo</h1>
        <p class="hero-subtitle">Track your money, build your future. A simple and powerful financial tracker combining personal and M-Pesa transactions.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature Section
    st.markdown("""
    <div class="feature-section">
        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-icon">📊</div>
                <h3 class="feature-title">Visual Analytics</h3>
                <p class="feature-text">See where your money goes with intuitive charts and reports that help you understand your spending habits.</p>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">📱</div>
                <h3 class="feature-title">M-Pesa Integration</h3>
                <p class="feature-text">Automatically import your M-Pesa transactions to keep track of all your mobile money activities.</p>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">🔒</div>
                <h3 class="feature-title">Secure & Private</h3>
                <p class="feature-text">Your financial data stays private and secure. We use industry-standard security practices to protect your information.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # CTA Section
    if "username" in st.session_state:
        # Different CTA for logged-in users
        st.markdown("""
        <div class="cta-container">
            <h2 class="cta-title">Continue Your Financial Journey</h2>
            <p class="cta-text">Welcome back! Ready to check your latest transactions and financial insights?</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Original CTA for non-logged-in users
        st.markdown("""
        <div class="cta-container">
            <h2 class="cta-title">Start Your Financial Journey Today</h2>
            <p class="cta-text">Join thousands of users who have taken control of their finances with Eropia umkhondo. It's free to start!</p>
        </div>
        """, unsafe_allow_html=True)
    
    # CTA Buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Check if user is logged in
        if "username" in st.session_state:
            # Show dashboard button
            if st.button("Go to Dashboard", key="cta_dashboard_btn", use_container_width=True):
                st.session_state.current_page = "dashboard"
                st.rerun()
        else:
            # Show login/register buttons if not logged in
            col_left, col_right = st.columns(2)
            with col_left:
                if st.button("Create Account", key="cta_create_account_btn", use_container_width=True):
                    st.session_state.current_page = "register"
                    st.rerun()
            with col_right:
                if st.button("Login", key="cta_login_btn", use_container_width=True):
                    st.session_state.current_page = "login"
                    st.rerun()
    
    # Financial Tip Section
    st.markdown("""
    <div class="context-section">
        <h3 class="context-title">Interactive Financial Tips</h3>
        <p style="text-align: center; font-size: 1.1rem; color: #4B5563; margin-bottom: 1.5rem;">
            Discover personalized financial advice to improve your money management skills
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create a container for the tips widget with custom styling
    st.markdown("""
    <style>
    .tips-container {
        background-color: #f8f9fa;
        border-radius: 16px;
        padding: 30px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        margin: 20px 0;
        border: 1px solid #e0e5ec;
    }
    .tips-container h4 {
        color: #1E3A8A;
        margin-bottom: 20px;
        font-size: 1.4rem;
        text-align: center;
    }
    </style>
    <div class="tips-container">
    """, unsafe_allow_html=True)
    
    # Add helpful text based on login status
    if "username" in st.session_state:
        st.markdown("""
        <p style="text-align: center; margin-bottom: 20px; font-size: 1.1rem;">
            Your personal financial tips are based on your transaction history and spending patterns.
        </p>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <p style="text-align: center; margin-bottom: 20px; font-size: 1.1rem;">
            Create an account to receive personalized tips based on your financial behavior.
        </p>
        """, unsafe_allow_html=True)
    
    # Center the tip widget button
    col1, col2, col3 = st.columns([2, 3, 2])
    with col2:
        # Use custom styling for the button to make it more prominent
        st.markdown("""
        <style>
        [data-testid="stButton"] button {
            background-color: #1E88E5;
            color: white;
            padding: 10px 20px;
            font-size: 1.1rem;
            font-weight: bold;
            border-radius: 10px;
            border: none;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        [data-testid="stButton"] button:hover {
            background-color: #1565C0;
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
            transform: translateY(-2px);
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Display the interactive tip widget button
        tip_widget_button(location="main")
    
    # Close the container div
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Display the financial tips popup widget if it's toggled on
    display_tip_widget()
    
    # Cultural Context Section
    st.markdown("""
    <div class="context-section">
        <h3 class="context-title">About "Eropia umkhondo"</h3>
        <p class="context-text">
            "Eropia" is a Maasai word meaning "money" or "wealth", and "umkhondo" comes from Zulu meaning "track" or "trail". 
            Together, they represent our mission to help you track your money across different cultures and financial systems,
            bringing traditional values of saving and wise resource management into the digital age.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer-container">
        <p class="footer-text">© 2025 Eropia umkhondo - Your personal finance journey</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    app()