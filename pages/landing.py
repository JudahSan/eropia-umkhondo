import streamlit as st

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
    
    # Top Navigation - with responsive design
    st.markdown("""
    <style>
    /* CSS for responsive navigation */
    .nav-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem;
        background-color: rgba(255, 255, 255, 0.95);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        position: sticky;
        top: 0;
        z-index: 100;
    }
    
    .nav-logo {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1E3A8A;
    }
    
    .nav-buttons {
        display: flex;
        gap: 12px;
    }
    
    .nav-icon-button {
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #1E88E5;
        color: white;
        border: none;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 1.1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    
    .nav-icon-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    .nav-icon-button.login {
        background-color: #1E88E5;
    }
    
    .nav-icon-button.register {
        background-color: #2E7D32;
    }
    
    /* Hide Streamlit elements for the buttons */
    div[data-testid="stHorizontalBlock"] {
        height: 0;
        visibility: hidden;
    }
    
    @media (max-width: 768px) {
        .nav-logo {
            font-size: 1.2rem;
        }
    }
    </style>
    
    <div class="nav-container">
        <div class="nav-logo">Eropia umkhondo</div>
        <div class="nav-buttons">
            <button class="nav-icon-button login" id="login-btn" title="Login">👤</button>
            <button class="nav-icon-button register" id="register-btn" title="Register">➕</button>
        </div>
    </div>
    
    <script>
        // Add event listeners to the buttons
        document.getElementById('login-btn').addEventListener('click', function() {
            // This will be picked up by the hidden button
            document.querySelector('button[data-testid="element-1"]').click();
        });
        
        document.getElementById('register-btn').addEventListener('click', function() {
            // This will be picked up by the hidden button
            document.querySelector('button[data-testid="element-2"]').click();
        });
    </script>
    """, unsafe_allow_html=True)
    
    # Hidden buttons that will be triggered by the JavaScript code
    col1, col2 = st.columns(2)
    with col1:
        if st.button("", key="1", help="Hidden login button"):
            st.session_state.current_page = "login"
            st.rerun()
    with col2:
        if st.button("", key="2", help="Hidden register button"):
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
    st.markdown("""
    <div class="cta-container">
        <h2 class="cta-title">Start Your Financial Journey Today</h2>
        <p class="cta-text">Join thousands of users who have taken control of their finances with Eropia umkhondo. It's free to start!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # CTA Buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        col_left, col_right = st.columns(2)
        with col_left:
            if st.button("Create Account", key="cta_create_account_btn", use_container_width=True):
                st.session_state.current_page = "register"
                st.rerun()
        with col_right:
            if st.button("Login", key="cta_login_btn", use_container_width=True):
                st.session_state.current_page = "login"
                st.rerun()
    
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