import numpy as np

from Position import Position

class Market():
    '''
    A market is composed of a vAMM with two assets, a price feed, a funding function, 
    a liquidation engine.
    '''
    def __init__(self, k0, initial_mark, index, marketID) -> None:
        self.base_reserves = np.sqrt(k0)
        self.quote_reserves = np.sqrt(k0)
        self.pegMultiplier = initial_mark
        self.k = k0
        self.index = index
        self.global_collateral = 0
        # List of open positions on this market
        self.positions = []
        self.ID = marketID

    def swapBaseIn(self, amountInBase):
        '''
        The amount in may be negative. 
        Return the net amount to give to the trader. If the result is negative, 
        take that amount from the trader's portfolio.
        '''
        #We can't remove more than what's in the virtual pool.
        # scaled_amount_in_base = amountInBase/self.pegMultiplier
        assert -amountInBase < self.base_reserves 
        newQuote = (self.k)/(self.base_reserves + amountInBase)
        deltaQuote = newQuote - self.quote_reserves
        self.quote_reserves = newQuote
        self.base_reserves += amountInBase
        assert self.base_reserves > 0 and self.quote_reserves > 0
        effective_price_in_quote = abs(deltaQuote*self.pegMultiplier/amountInBase)
        return deltaQuote*self.pegMultiplier, effective_price_in_quote

    def swapQuoteIn(self, amountInQuote):
        '''
        The amount in may be negative.
        '''
        unpegged_quote_amount = amountInQuote/self.pegMultiplier
        assert -unpegged_quote_amount < self.quote_reserves
        newBase = (self.k)/(self.quote_reserves + unpegged_quote_amount)
        deltaBase = newBase - self.base_reserves 
        self.base_reserves = newBase
        self.quote_reserves += unpegged_quote_amount
        assert self.base_reserves > 0 and self.quote_reserves > 0
        effective_price_in_quote = abs(amountInQuote/deltaBase)
        return deltaBase, effective_price_in_quote

    def getSpot(self):
        '''
        Return the spot price denominated in the quote asset (Y)
        '''
        return self.pegMultiplier*(self.quote_reserves/self.base_reserves)

    def openPosition(self, traderID, quoteOpenSize):
        '''
        '''
        if quoteOpenSize < 0:
            # If we remove some quote from the reserves, we add some base 
            # = delta_base is positive 
            # = *(-1) the trader gets a net negative base asset amount
            size, _ = self.swapQuoteIn(quoteOpenSize)
            size = -size
            pos = Position(traderID, self.ID, abs(quoteOpenSize), size, "short")
            self.positions.append(pos)
            return pos 
        size, _ = self.swapQuoteIn(quoteOpenSize)
        size = -size
        pos = Position(traderID, self.ID, quoteOpenSize, size, "long")
        self.positions.append(pos)
        return pos

    def closePosition(self, traderID):
        '''
        '''
        index= 0
        for i in range(len(self.positions)): 
            pos = self.positions[i]
            if pos.traderID == traderID:
                # Close  the position in the market
                _, _ = self.swapBaseIn(pos.size)
                index = i 
                break
        print("debug")
        self.positions.pop(index)
        return 