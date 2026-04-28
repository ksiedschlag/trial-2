import streamlit as st # builds the app and allows for integration
import yfinance as yf # pulls real time stock market data
import pandas as pd # Helps with data and calculation

# Initialize session state for user responses - saves user answers so that they don't reset
if 'responses' not in st.session_state:
    st.session_state.responses = ['', '', '', '', '']

# Function to display each question and get user response
def display_question(question, index):
    # st.radio returns the selected label. We store this label in session state.
    # The 'index' parameter sets the initial selection. If there's a stored response,
    # we find its index to set the initial selection correctly.
    options = ['Very uncomfortable', 'uncomfortable', 'Neutral', 'comfortable', 'very comfortable']
    current_selection_index = options.index(st.session_state.responses[index]) if st.session_state.responses[index] else 2
    st.session_state.responses[index] = st.radio(question, options, index=current_selection_index)

# List of assessment questions
questions = [
    "1. How would you feel if your investment portfolio lost 20% of value in a year?",
    "2. How comfortable are you with delaying financial rewards today in exchange for potentially greater rewards in the future? ",
    "3. How comfortable are you with keeping an investment even when the market is experiencing volatility?  .",
    "4. How would you feel if you had a 50/50 chance of doubling your money or losing it all?",
    "5. How comfortable are you making financial decisions when the outcome is uncertain?"
]

# Display all questions
st.title('Risk Tolerance Assessment')
for i, question in enumerate(questions):
    display_question(question, i)

# Calculate total score based on user responses
# Scoring: Higher score means higher risk tolerance.
# 'Very uncomfortable' (low risk tolerance) -> 0 points
# 'uncomfortable' -> 1 point
# 'Neutral' -> 2 points
# 'comfortable' -> 3 points
# 'very comfortable' (high risk tolerance) -> 4 points
score_for_option = {
    'Very uncomfortable': 0,
    'uncomfortable': 1,
    'Neutral': 2,
    'comfortable': 3,
    'very comfortable': 4
}
total_score = 0
for response_label in st.session_state.responses:
    total_score += score_for_option.get(response_label, 0) # Add score, default 0 if not selected yet

# Define risk profiles and their investment criteria
risk_profiles = {
    'Low': {
        'goal': 'Preserve capital and achieve a modest return.',
        'allocation': '20% Stocks, 80% Bonds',
        'rationale': 'Low-risk tolerance, focusing on capital preservation.',
        'summary': 'Invest primarily in bonds and stable assets.',
        'stock_criteria': {
            'volatility_threshold': 0.01, # Max daily return std dev (e.g., 1% daily std dev)
            'avg_return_threshold': 0.0005, # Min average daily return (e.g., 0.05% daily avg)
            'min_price_change_percent': 2 # Min price growth over last year (e.g., 2%)
        },
        'recommended_investments': [
            {'ticker': 'BND', 'name': 'Vanguard Total Bond Market ETF', 'description': 'Broad bond market exposure for stability'},
            {'ticker': 'AGG', 'name': 'iShares Core U.S. Aggregate Bond ETF', 'description': 'Investment-grade bonds with low volatility'},
            {'ticker': 'KO', 'name': 'Coca-Cola', 'description': 'Dividend-paying defensive stock'},
            {'ticker': 'PG', 'name': 'Procter & Gamble', 'description': 'Stable consumer staples with consistent dividends'},
            {'ticker': 'JNJ', 'name': 'Johnson & Johnson', 'description': 'Healthcare leader with strong dividend history'},
        ]
    },
    'Medium': {
        'goal': 'Achieve balanced growth while managing risk.',
        'allocation': '50% Stocks, 50% Bonds',
        'rationale': 'Moderate risk tolerance, seeks growth with some safety.',
        'summary': 'Mix of stocks and bonds for balanced portfolio.',
        'stock_criteria': {
            'volatility_threshold': 0.02,
            'avg_return_threshold': 0.001,
            'min_price_change_percent': 5
        },
        'recommended_investments': [
            {'ticker': 'VOO', 'name': 'Vanguard S&P 500 ETF', 'description': 'Diversified large-cap stock exposure'},
            {'ticker': 'VTI', 'name': 'Vanguard Total Stock Market ETF', 'description': 'Complete U.S. stock market coverage'},
            {'ticker': 'BND', 'name': 'Vanguard Total Bond Market ETF', 'description': 'Balanced bond allocation'},
            {'ticker': 'MSFT', 'name': 'Microsoft', 'description': 'Tech leader with strong fundamentals'},
            {'ticker': 'AAPL', 'name': 'Apple', 'description': 'Established tech company with solid growth'},
        ]
    },
    'High': {
        'goal': 'Maximize growth potential and returns.',
        'allocation': '80% Stocks, 20% Bonds',
        'rationale': 'High-risk tolerance, accepting volatility for higher returns.',
        'summary': 'Aggressive approach with a focus on stock investments.',
        'stock_criteria': {
            'volatility_threshold': 0.03,
            'avg_return_threshold': 0.0015,
            'min_price_change_percent': 10
        },
        'recommended_investments': [
            {'ticker': 'QQQ', 'name': 'Invesco QQQ Trust (Nasdaq-100)', 'description': 'Growth-focused tech-heavy index'},
            {'ticker': 'VUG', 'name': 'Vanguard U.S. Growth ETF', 'description': 'High-growth stocks with higher volatility'},
            {'ticker': 'TSLA', 'name': 'Tesla', 'description': 'High-growth tech company with significant upside potential'},
            {'ticker': 'NVDA', 'name': 'NVIDIA', 'description': 'AI and semiconductor leader with strong growth'},
            {'ticker': 'AMD', 'name': 'Advanced Micro Devices', 'description': 'Semiconductor company with high growth potential'},
        ]
    }
}

# Determine risk profile based on total score (0-20 scale)
# Lower score -> Lower risk tolerance -> 'Low' profile
# Higher score -> Higher risk tolerance -> 'High' profile
if total_score <= 6: # Scores 0-6
    profile = 'Low'
elif total_score <= 13: # Scores 7-13
    profile = 'Medium'
else: # Scores 14-20
    profile = 'High'

st.title('📊 Risk Tolerance Assessment')
tab1, tab2, tab3 = st.tabs(["📋 Assessment", "📈 Results", "🔍 Stock Analyzer"])

# TAB 1: Assessment
with tab1:
    st.header("Answer the Following Questions")
    st.write("Please rate your comfort level with each scenario:")
    st.write("")
    
    for i, question in enumerate(questions):
        display_question(question, i)
    
    st.info(f"Current Score: **{total_score}/20**")

# TAB 2: Results
with tab2:
    st.header(f"Your Risk Profile: {profile}")
    
    # Create columns for profile summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Risk Score", f"{total_score}/20", "Assessment Complete")
    with col2:
        st.metric("🎯 Profile", profile, "Determined")
    with col3:
        st.metric("💼 Allocation", risk_profiles[profile]['allocation'].split()[0], "Stocks")
st.markdown("---")
    

# Display results
st.header(f"Your Risk Profile: {profile}")
st.write(f"**Goal:** {risk_profiles[profile]['goal']}")
st.write(f"**Recommended Asset Allocation:** {risk_profiles[profile]['allocation']}")
st.write(f"**Rationale:** {risk_profiles[profile]['rationale']}")
st.write(f"**Summary:** {risk_profiles[profile]['summary']}")

# Display recommended investments for the user's risk profile
st.subheader(f"📈 Recommended Investments for {profile} Risk Profile")
st.write(f"Based on your risk tolerance, here are investments suitable for your profile:")

recommendations_df = pd.DataFrame(risk_profiles[profile]['recommended_investments'])
st.table(recommendations_df)

# TAB 3: Stock Investment Recommendation
with tab3:
    st.header('🔍 Stock Investment Recommendation')
    st.write("Analyze any stock to see if it aligns with your risk profile:")
    st.write("")

# --- New Section: Stock Investment Recommendation ---
st.subheader('Stock Investment Recommendation')
stock_ticker = st.text_input("Enter a stock ticker symbol (e.g., AAPL, MSFT, GOOGL):", key="stock_ticker_input").upper()

if stock_ticker:
    with st.spinner(f'Fetching data for {stock_ticker}...'):
        try:
            # Fetch data for the last year
            stock_data = yf.download(stock_ticker, period="1y", progress=False)

            if not stock_data.empty:
                st.write(f"\nAnalyzing **{stock_ticker}** (last 1 year):")

                # Get close prices
                close_prices = stock_data['Close']

                # Convert DataFrame column to Series if needed
                if isinstance(close_prices, pd.DataFrame):
                    close_prices = close_prices.squeeze()

                # Calculate daily returns
                stock_data['Daily Return'] = close_prices.pct_change()

                # Calculate volatility and average return
                volatility = float(stock_data['Daily Return'].std())
                avg_daily_return = float(stock_data['Daily Return'].mean())

                # Calculate total price change
                initial_price = float(close_prices.iloc[0])
                final_price = float(close_prices.iloc[-1])
                price_change_percent = ((final_price - initial_price) / initial_price) * 100

                st.write(f"- Daily Volatility (Std Dev of Daily Returns): **{volatility:.4f}**")
                st.write(f"- Average Daily Return: **{avg_daily_return:.4f}**")
                st.write(f"- Total Price Change: **{price_change_percent:.2f}%**")

                # Get criteria for the determined risk profile
                profile_criteria = risk_profiles[profile]['stock_criteria']

                invest_decision_factors = []

                # Check volatility
                if volatility <= profile_criteria['volatility_threshold']:
                    invest_decision_factors.append(True)
                    st.write(f"  ✅ Volatility ({volatility:.4f}) is within your **{profile}** risk tolerance (max {profile_criteria['volatility_threshold']:.4f}).")
                else:
                    invest_decision_factors.append(False)
                    st.write(f"  ❌ Volatility ({volatility:.4f}) is higher than your **{profile}** risk tolerance (max {profile_criteria['volatility_threshold']:.4f}).")

                # Check average daily return
                if avg_daily_return >= profile_criteria['avg_return_threshold']:
                    invest_decision_factors.append(True)
                    st.write(f"  ✅ Average daily return ({avg_daily_return:.4f}) meets your **{profile}** profile's minimum ({profile_criteria['avg_return_threshold']:.4f}).")
                else:
                    invest_decision_factors.append(False)
                    st.write(f"  ❌ Average daily return ({avg_daily_return:.4f}) is below your **{profile}** profile's minimum ({profile_criteria['avg_return_threshold']:.4f}).")

                # Check total price change
                if price_change_percent >= profile_criteria['min_price_change_percent']:
                    invest_decision_factors.append(True)
                    st.write(f"  ✅ Total price change ({price_change_percent:.2f}%) meets your **{profile}** profile's minimum growth expectation ({profile_criteria['min_price_change_percent']:.2f}%).")
                else:
                    invest_decision_factors.append(False)
                    st.write(f"  ❌ Total price change ({price_change_percent:.2f}%) is below your **{profile}** profile's minimum growth expectation ({profile_criteria['min_price_change_percent']:.2f}%).")

                st.write("\n---")

                # Final decision
                if all(invest_decision_factors):
                    st.success(f"**Recommendation for {stock_ticker}: Consider Investing!** This stock aligns well with your **{profile}** risk profile and investment criteria.")
                else:
                    st.error(f"**Recommendation for {stock_ticker}: Do Not Invest at this time.** This stock does not fully align with your **{profile}** risk profile and investment criteria based on the criteria above.")

            else:
                st.warning(f"Could not retrieve data for ticker: **{stock_ticker}**. Please check the symbol and try again.")

        except Exception as e:
            st.error(f"An error occurred while fetching data for {stock_ticker}: {e}")
            st.info("Please ensure the ticker symbol is valid and try again. Sometimes, data for very obscure tickers may not be available via `yfinance`.")
