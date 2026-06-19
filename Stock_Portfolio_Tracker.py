import csv

# 1. Hardcoded stock prices as required by the task scope
STOCK_PRICES = {
    "AAPL": 180,
    "TSLA": 250,
    "GOOGL": 175,
    "MSFT": 420,
    "AMZN": 185
}

def display_available_stocks():
    print("\n--- Available Stocks and Market Prices ---")
    for stock, price in STOCK_PRICES.items():
        print(f"Symbol: {stock:6} | Price: ${price}")
    print("------------------------------------------\n")

def calculate_portfolio():
    portfolio = {}
    total_investment = 0
    
    print("=== Stock Portfolio Tracker ===")
    display_available_stocks()
    
    # 2. User Input/Output loop
    while True:
        symbol = input("Enter stock symbol to add (or type 'done' to finish): ").strip().upper()
        
        if symbol == 'DONE':
            break
            
        if symbol not in STOCK_PRICES:
            print(f"❌ '{symbol}' is not in our market database. Please try an available stock.")
            continue
            
        try:
            quantity = int(input(f"Enter quantity for {symbol}: "))
            if quantity <= 0:
                print("❌ Quantity must be greater than zero.")
                continue
        except ValueError:
            print("❌ Invalid input! Please enter a whole number for quantity.")
            continue
            
        # Update portfolio (adds quantity if stock is entered multiple times)
        portfolio[symbol] = portfolio.get(symbol, 0) + quantity
        print(f"✅ Added {quantity} shares of {symbol}.\n")

    # 3. Basic Arithmetic & Display Results
    if not portfolio:
        print("\nYour portfolio is empty. Exiting application.")
        return

    print("\n==================================")
    print("        YOUR PORTFOLIO SUMMARY    ")
    print("==================================")
    print(f"{'Stock':<10}{'Quantity':<10}{'Price':<10}{'Total Value':<10}")
    print("-" * 42)
    
    portfolio_details = []
    for symbol, quantity in portfolio.items():
        price = STOCK_PRICES[symbol]
        stock_value = quantity * price
        total_investment += stock_value
        
        print(f"{symbol:<10}{quantity:<10}${price:<9}${stock_value:<10}")
        portfolio_details.append([symbol, quantity, price, stock_value])
        
    print("-" * 42)
    print(f"Total Portfolio Value: ${total_investment}")
    print("==================================\n")

    # 4. Optional File Handling (Saving to .csv)
    save_choice = input("Do you want to save this summary to a CSV file? (yes/no): ").strip().lower()
    if save_choice in ['yes', 'y']:
        filename = "portfolio_summary.csv"
        try:
            with open(filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                # Writing Headers
                writer.writerow(["Stock Symbol", "Quantity", "Unit Price ($)", "Total Value ($)"])
                # Writing Data
                writer.writerows(portfolio_details)
                writer.writerow([])
                writer.writerow(["Total Portfolio Value", "", "", f"${total_investment}"])
            print(f"💾 Success! Portfolio saved as '{filename}' in your current directory.")
        except IOError:
            print("❌ Error saving file. Please check folder permissions.")

if __name__ == "__main__":
    calculate_portfolio()