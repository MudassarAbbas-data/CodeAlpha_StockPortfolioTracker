import csv
import os
from datetime import datetime

STOCK_PRICES = {
    "AAPL":  182.50,
    "TSLA":  248.00,
    "GOOGL": 175.30,
    "MSFT":  415.20,
    "AMZN":  192.80,
    "META":  508.90,
    "NVDA":  875.40,
}

def show_available_stocks():
    print("\n" + "=" * 40)
    print(f"  {'SYMBOL':<8} {'COMPANY':<12} {'PRICE (USD)':>12}")
    print("-" * 40)
    names = {
        "AAPL": "Apple", "TSLA": "Tesla", "GOOGL": "Google",
        "MSFT": "Microsoft", "AMZN": "Amazon", "META": "Meta", "NVDA": "NVIDIA"
    }
    for symbol, price in STOCK_PRICES.items():
        print(f"  {symbol:<8} {names[symbol]:<12} ${price:>10.2f}")
    print("=" * 40)

def get_portfolio():
    portfolio = {}
    print("\n📈 Enter your stock holdings.")
    print("Type 'done' when finished.\n")
    while True:
        symbol = input("Stock symbol (e.g. AAPL): ").upper().strip()
        if symbol == "DONE":
            break
        if symbol not in STOCK_PRICES:
            print(f"  ⚠️  '{symbol}' not found. Available: {', '.join(STOCK_PRICES.keys())}")
            continue
        try:
            qty = int(input(f"  How many shares of {symbol}? "))
            if qty <= 0:
                print("  ⚠️  Quantity must be a positive number.")
                continue
        except ValueError:
            print("  ⚠️  Please enter a whole number.")
            continue
        if symbol in portfolio:
            portfolio[symbol] += qty
        else:
            portfolio[symbol] = qty
        print(f"  ✅ Added {qty} shares of {symbol}.\n")
    return portfolio

def calculate_portfolio(portfolio):
    results = []
    total = 0.0
    for symbol, qty in portfolio.items():
        price = STOCK_PRICES[symbol]
        value = price * qty
        total += value
        results.append({"symbol": symbol, "quantity": qty, "price": price, "value": value})
    return results, total

def display_portfolio(results, total):
    print("\n" + "=" * 55)
    print("  📊 PORTFOLIO SUMMARY")
    print("=" * 55)
    print(f"  {'STOCK':<8} {'QTY':>6} {'PRICE':>12} {'VALUE':>14}")
    print("-" * 55)
    for row in results:
        print(f"  {row['symbol']:<8} {row['quantity']:>6} "
              f"${row['price']:>10.2f}  ${row['value']:>12.2f}")
    print("-" * 55)
    print(f"  {'TOTAL INVESTMENT':>28}  ${total:>12.2f}")
    print("=" * 55)

def save_to_csv(results, total):
    filename = f"portfolio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Stock", "Quantity", "Price (USD)", "Value (USD)"])
        for row in results:
            writer.writerow([row["symbol"], row["quantity"],
                             f"{row['price']:.2f}", f"{row['value']:.2f}"])
        writer.writerow([])
        writer.writerow(["Total Investment", "", "", f"{total:.2f}"])
    print(f"\n💾 Portfolio saved to: {filename}")

def main():
    print("\n💼 Welcome to Stock Portfolio Tracker!")
    print("This tool calculates the total value of your stock holdings.")
    show_available_stocks()
    portfolio = get_portfolio()
    if not portfolio:
        print("\n⚠️  No stocks entered. Exiting.")
        return
    results, total = calculate_portfolio(portfolio)
    display_portfolio(results, total)
    save = input("\nSave portfolio to CSV? (yes/no): ").lower().strip()
    if save in ("yes", "y"):
        save_to_csv(results, total)
    print("\nThank you for using Stock Portfolio Tracker! 📈")

if __name__ == "__main__":
    main()
    