# visualize-portfolio
plots a custom crypto portfolio 


There's a few global variables that you can edit.

CURR is the currency that you want to measure in. For more info check https://www.coingecko.com/api/documentations/v3#/simple/get_simple_price

DIRECT is where it will save your txt files generated by the script. If left with none it will save it in the directory that you're running the script from

SHOW is the maximum values it will show. Note that when the plot is updated so are the txt files. So the first tick that you run it won't show any lines plotted.

MARKET_FILE is just the name of the txt file for the market data.

OWN if set to true it will show your portfolio and the first instance you run the script you will have to input the symbol for your coin and the number of coins you own.
OWN is there so if you want to make a hypothetical portolio and not lose the values you have for your own portfolio you can.

REFRESH is how often the plot is refreshed in milliseconds

COINS is only set when OWN is False. It has to be populated as a list of tickers

AMOUNT is only set when OWN is False. It is the amount of money in your hypothetical portfolio

other things you can change that aren't global variables...

if you run the function make_market_owned(True) you can add tickers into your portfolio without having to redo the creation.





