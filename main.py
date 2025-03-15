import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats
import pandas as pd

def fetch_and_analyze_stock_data(stock_symbol1, stock_symbol2, start_date, end_date):
    """
    Fetches stock data for the given symbols and date range, plots them, and analyzes hedge relations.

    :param stock_symbol1: First stock ticker symbol (e.g., 'AAPL')
    :param stock_symbol2: Second stock ticker symbol (e.g., 'MSFT')
    :param start_date: Start date for the data (e.g., '2020-01-01')
    :param end_date: End date for the data (e.g., '2023-01-01')
    """
    try:
        # Fetch stock data using yfinance
        stock_data1 = yf.download(stock_symbol1, start=start_date, end=end_date)
        stock_data2 = yf.download(stock_symbol2, start=start_date, end=end_date)

        if stock_data1.empty:
            print(f"No data found for {stock_symbol1} in the given date range.")
            return

        if stock_data2.empty:
            print(f"No data found for {stock_symbol2} in the given date range.")
            return

        # Align data on dates
        combined_data = pd.DataFrame(stock_data1['Close']).rename(columns={'Close': stock_symbol1}).join(
            pd.DataFrame(stock_data2['Close']).rename(columns={'Close': stock_symbol2}), how='inner'
        )
        # Calculate daily returns
        returns1 = combined_data[stock_symbol1].pct_change().dropna()
        returns2 = combined_data[stock_symbol2].pct_change().dropna()

        # Perform correlation analysis
        correlation, _ = scipy.stats.pearsonr(returns1, returns2)

        # Perform linear regression for hedge ratio
        slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(returns1, returns2)

        # Plot the closing prices
        plt.figure(figsize=(12, 6))
        plt.plot(combined_data[stock_symbol1], label=f'{stock_symbol1} Closing Price', color='blue')
        plt.plot(combined_data[stock_symbol2], label=f'{stock_symbol2} Closing Price', color='orange')
        plt.title(f'{stock_symbol1} and {stock_symbol2} Stock Prices ({start_date} to {end_date})')
        plt.xlabel('Date')
        plt.ylabel('Closing Price (USD)')
        plt.legend()
        plt.grid()
        plt.show()

        # Display hedge analysis results
        print(f"Correlation between {stock_symbol1} and {stock_symbol2}: {correlation:.2f}")
        print(f"Hedge Ratio (Slope of regression line): {slope:.2f}")
        print(f"P-Value of regression: {p_value:.2e}")

        # Assess hedge relationship
        hedge_relationship = "YES" if abs(correlation) > 0.7 and p_value < 0.05 else "NO"
        print("\nHedge Relationship Analysis:")
        print(f"- Strong Correlation (|correlation| > 0.7): {'YES' if abs(correlation) > 0.7 else 'NO'}")
        print(f"- Statistically Significant (p-value < 0.05): {'YES' if p_value < 0.05 else 'NO'}")
        print(f"- Overall Hedge Relationship: {hedge_relationship}")

        # Scatter plot of returns
        plt.figure(figsize=(8, 6))
        plt.scatter(returns1, returns2, alpha=0.5, label='Daily Returns')
        plt.plot(returns1, slope * returns1 + intercept, color='red', label='Regression Line')
        plt.title(f'Returns Correlation between {stock_symbol1} and {stock_symbol2}')
        plt.xlabel(f'{stock_symbol1} Daily Returns')
        plt.ylabel(f'{stock_symbol2} Daily Returns')
        plt.legend()
        plt.grid()
        plt.show()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Get user input for stock symbols and date range
    stock_symbol1 = input("Enter the first stock ticker symbol (e.g., 'AAPL'): ").strip().upper()
    stock_symbol2 = input("Enter the second stock ticker symbol (e.g., 'MSFT'): ").strip().upper()
    start_date = input("Enter the start date (YYYY-MM-DD): ").strip()
    end_date = input("Enter the end date (YYYY-MM-DD): ").strip()

    if start_date.lower() == 'full':
        start_date = '1900-01-01'
    if end_date.lower() == 'full':
        end_date = '2100-01-01'

    # Fetch, analyze, and display the stock data
    fetch_and_analyze_stock_data(stock_symbol1, stock_symbol2, start_date, end_date)