import APIKeys 
import CrytpoTradingBot 

def main():
    currencyPairs = 'ETH-USD'
    coinbase = CrytpoTradingBot.CrytpoTradingBot(APIKeys.api_key, APIKeys.api_secret, currencyPairs)
    coinbase.start()

if __name__ == "__main__":
     main() # Add ability to pass in currency pairs we want to trade etc.