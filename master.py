import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mdates

def get_stock_data(ticker, start_date, end_date):
    # Download stock data using yfinance
    stock_data = yf.download(ticker, start=start_date, end=end_date)

    # Ensure the data is not empty
    if stock_data.empty:
        return pd.DataFrame()

    # Remove weekends and holidays
    stock_data = stock_data[stock_data.index.to_series().dt.dayofweek < 5]

    return stock_data

def get_company_name(ticker):
    # Use yfinance to get information about the ticker
    ticker_info = yf.Ticker(ticker)
    
    # Attempt to extract the company name using alternative methods
    company_name = (
        ticker_info.info.get('longName') or
        ticker_info.info.get('shortName') or
        ticker_info.info.get('displayName') or
        f"Company for {ticker}"
    )
    
    return company_name

def print_and_plot_stock_data(data, company_name, ticker):
    # Set the display options to show two decimal points
    pd.set_option('display.float_format', '{:.2f}'.format)

    # Calculate the percentage difference on the day
    data['Percent_Difference'] = data['Close'].pct_change() * 100

    # Replace NaN values with 0 in the Percent_Difference column
    data['Percent_Difference'].fillna(0, inplace=True)

    # Print the informative text
    print(f"Below is the price information for {company_name} ({ticker}):")

    # Print the data with pipes as column separators, fixed column width, and the new column
    print(data.to_string(index=True, col_space=12))

    # Plotting
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 12), gridspec_kw={'height_ratios': [2, 1, 1]})

    # Format data for candlestick chart
    ohlc = data[['Open', 'High', 'Low', 'Close']].copy()
    ohlc.reset_index(inplace=True)
    ohlc['Date'] = ohlc['Date'].map(mdates.date2num)

    # Plot candlestick chart
    candlestick_ohlc(ax1, ohlc.values, width=0.6, colorup='g', colordown='r', alpha=0.8)
    ax1.xaxis_date()
    ax1.set_title(f"Stock Prices for {company_name} ({ticker})")
    ax1.legend(['Open', 'High', 'Low', 'Close'])
    ax1.grid(True)

    # Plot volume as a bar chart with adjusted y-axis ticks
    ax2.bar(data.index, data['Volume'], color='purple', width=0.6)
    ax2.set_ylabel('Volume', color='purple')
    ax2.tick_params('y', colors='purple')
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    ax2.grid(True)

    # Plot percentage difference on a separate subplot as a bar chart with colors
    ax3.bar(data.index, data['Percent_Difference'], color=['r' if x < 0 else 'g' for x in data['Percent_Difference']])
    ax3.set_ylabel('% Difference', color='b')
    ax3.tick_params('y', colors='b')
    ax3.grid(True)

    # Draw a horizontal line at y=0
    ax3.axhline(0, color='black', linewidth=0.8)

    plt.tight_layout()
    plt.savefig(f'{ticker}_candlestick_plot.png')
    plt.show()

# Get user input for the stock ticker
ticker = input("Enter the stock ticker symbol: ").upper()

# Get the company name from the ticker information
company_name = get_company_name(ticker)

# Set the end date to today
end_date = datetime.today().strftime('%Y-%m-%d')

# Set the start date to 60 days ago
start_date = (datetime.today() - timedelta(days=60)).strftime('%Y-%m-%d')

# Get stock data
stock_data = get_stock_data(ticker, start_date, end_date)

# Print the retrieved data with two decimal points, pipes as separators, fixed column width, and % difference column
print_and_plot_stock_data(stock_data, company_name, ticker)

