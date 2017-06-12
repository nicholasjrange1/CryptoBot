from coinbase.wallet.client import Client
from coinbase.wallet.model import APIObject, Money

class Coinbase:
    
    def __init__(self, api_key, api_secret, currency_pairs):

        self.client = Client(api_key, api_secret) 

        self.currencyPair = currency_pairs

        self.startingBalUSD = 5000
        self.startingBalETH = 0

        self.balanceUSD = 5000
        self.balanceBTC = 0
        self.balanceETH = 0
        self.balanceLTC = 0
        self.profit = 0
        
        self.buys = []
        self.sells = []

        self.coinbaseFee = 1.49
        self.tempBuyPrice = self.GetBuyPrice() 
        self.tempSellPrice = self.GetSellPrice()
        
        print 'Starting Balances: ETH %s USD %s Profit $%s' % (self.startingBalETH,  '{0:,.2f}'.format(self.startingBalUSD), '0')
    
    def GetBuyPrice(self): # Returns Buy Price including fees       
        price = self.client._make_api_object(self.client._get('v2','prices', self.currencyPair, 'buy'), APIObject)
        return float(price["amount"]) + self.GetFee(float(price["amount"]))

    def GetSellPrice(self):  # Returns Sell Price including fees  
        price = self.client._make_api_object(self.client._get('v2','prices', self.currencyPair, 'sell'), APIObject)
        return float(price["amount"]) - self.GetFee(float(price["amount"]))

    def GetFee(self, price): # Calculates the fee for a given price
        fee = float((price / (100 / self.coinbaseFee)))
        return fee
       
    def Buy(self, amount): # Buy crypto
        total = self.GetBuyPrice() * amount
               
        if (self.balanceUSD - total) > 0: # If there is enough fiat in the account
            self.buys.append(total)
            self.balanceUSD -= total
            self.balanceETH += amount  
            self.GetCurrentBalance()            

    def Sell(self, amount): # Sell crypto
        total = self.GetSellPrice() * amount       
        self.sells.append(total)
        self.profit = float((self.balanceUSD + total) - self.startingBalUSD)
        self.balanceUSD += total
        self.balanceETH -= amount     
        self.GetCurrentBalance()  
    
    def GetCurrentBalance(self): 
        print  'Current Balances: ETH %s USD %s Profit $%s' % (self.balanceETH,  '{0:,.2f}'.format(self.balanceUSD), self.profit)    

    def GetSpread(self):
        if self.tempBuyPrice != self.GetBuyPrice() or \
           self.tempSellPrice != self.GetSellPrice(): # Print spread if Buy or Sell price has changed
            self.tempBuyPrice = self.GetBuyPrice()
            self.tempSellPrice = self.GetSellPrice()
            print '      Buy: $%s Sell: $%s' % (self.GetBuyPrice(), self.GetSellPrice())


''' ToDo's
    1. Create superclass. Going to have a few other accounts.
    2. Account can hold more than just ETH. Methods need to accomadate them.
    3. Add in api logic to go live.
'''
    
