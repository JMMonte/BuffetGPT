from investment_bot import InvestmentBot

def print_menu():
    print("Please choose an option:")
    print("1. Make an investment")
    print("2. View performance of the portfolio")
    print("3. Exit")

def main():
    investment_bot = InvestmentBot()
    
    while True:
        print_menu()
        choice = input("Enter the number of your choice: ")
        
        if choice == "1":
            investment_bot.run_strategy()
            print("Investment strategy executed.")
        elif choice == "2":
            investment_bot.display_performance()
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
