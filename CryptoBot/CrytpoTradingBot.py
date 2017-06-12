import sys
import Coinbase
import threading

class CrytpoTradingBot(threading.Thread):
    
    def __init__(self, api_key, api_secret, currency_pairs):              

        self.coinbase = Coinbase.Coinbase(api_key, api_secret, currency_pairs) #instantiate the account object              
        
        self.initBuyPrice = self.coinbase.GetBuyPrice() # Buy price at init
                        
        self.buyAmount = 5 # Amount to buy
        self.initDropWait = -1 # Wait until price drops this much before buying in
        self.minProfit = 0  # Profit to make before selling
        self.stopLoss = 200 # Exit and re-evaluate if account loses this much

    def start(self):        
        while True: # Trade until stop loss is hit 
            self.coinbase.GetSpread() # Display spread
            self.trade()     
    
    def trade(self): # Simple trading logic. More advance logic in TradingAlgorithms.py.   
        if len(self.coinbase.buys) == 0: # If the account isn't holding crypto attemp to buy some crypto           
            if self.initBuyPrice - self.coinbase.GetBuyPrice() >= self.initDropWait: # If we have reached the initDropWait threshold
                self.coinbase.Buy(self.buyAmount) # Make the purchase
        else:
            for index, buy in enumerate(self.coinbase.buys):                
                if (self.coinbase.GetSellPrice() * self.buyAmount) > (buy + self.minProfit): # If we have reached the profit threshold
                    self.coinbase.Sell(self.buyAmount)  # Make the sale
                    self.coinbase.buys.remove(buy) # Remove buy from list
                elif buy - (self.coinbase.GetSellPrice() * self.buyAmount) > self.stopLoss: # If the stop loss has been hit
                    self.coinbase.Sell(self.buyAmount) # Sell our crypto  
                    #self.coinbase.buys.remove(buy) 
                    sys.exit(0) # Stop and re-evaluate trading algorithm         

            for index, sell in enumerate(self.coinbase.sells):                
                if (self.coinbase.GetBuyPrice() * self.buyAmount) - sell > self.initDropWait: # If the price has dropped by initDropWait since last the sale               
                    self.coinbase.Buy(self.buyAmount) # Buy back in
                    self.coinbase.sells.remove(sell)  # Remove sale from list           
          
