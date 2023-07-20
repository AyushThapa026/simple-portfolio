import yfinance as yf

owned_stocks = {}
stock_data = {} # keep hold of at least 1 month of data, larger periods of time can be queried

stock_save_file = open("stocks.txt", "r+")

for line in stock_save_file:
    stock_info = line.split()
    stock_name = stock_info[0]
    share_amount = stock_info[1]

    print(stock_info)
    owned_stocks[stock_name] = {}
    owned_stocks[stock_name]["Shares"] = int(share_amount)

while True:
    print("What would you like to do? (Type [HELP] for a list of commands): ", end="")
    response = input().split()
    
    command = response[0]

    if (command == 'HELP'):
        print("ADD [STOCK_NAME] [SHARES] - This command will add a stock to your portfolio with the given number of shares")
        print("UPDATE [STOCK_NAME] [SHARES] - This command will update a stock in your portfolio with the given number of shares")
        print("REMOVE [STOCK_NAME] - This command will remove a stock from your portfolio")
        print("PROFIT [STOCK_NAME] - This command will print the percent difference from open to close today")
        print("EXIT - Terminates the application")
    elif (command == "ADD"):
        stock_name = response[1]
        share_amount = response[2]
        if not (stock_name and share_amount):
            print("Invalid input")
        elif (owned_stocks.get(stock_name) == None):
            owned_stocks[stock_name] = {"Shares": share_amount}
        else:
            print("Stock already exists in portfolio")
    elif (command == "UPDATE"):
        stock_name = response[1]
        share_amount = response[2]
        if not (stock_name and share_amount):
            print("Invalid input")
        elif (owned_stocks[stock_name] == None):
            print("You don't own that stock.")
        elif (owned_stocks[stock_name] != None):
            owned_stocks[stock_name] = share_amount
    elif (command == "REMOVE"):
        stock_name = response[1]
        if not stock_name:
            print("Invalid input")
        else:
            owned_stocks[stock_name] = None
    elif (command == "HISTORY"):
        stock_name = response[1]
        if not stock_name:
            print("Invalid input")
        else:
            stock = yf.Ticker(stock_name)
            hist = stock.history(period="2d")
            
            previous_close_price = hist["Close"][0]
            close_price = hist["Close"][1]
            percentage = ((close_price - previous_close_price) / previous_close_price) * 100
            percentage = round(percentage, 3)

            if (percentage > 0):
                print("+" + str(percentage) + "%")
            else:
                print(str(percentage) + "%")
    elif (command == "EXIT"):
        for stock, stock_info in owned_stocks.items():
            line = stock + " " + str(stock_info["Shares"]) + "\n"
            stock_save_file.write(line)

        stock_save_file.close()
        break