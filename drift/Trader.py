class Trader():
    '''
    A trader has some amount of collateral and interacts with a market to 
    open and close positions. They can also be liquidated if their position
    is not collateralized enough. 
    '''
    def __init__(self, traderID, quote_portfolio) -> None:
        self.positions = []
        self.quote_portfolio = quote_portfolio
        self.margin = 0
        self.ID = traderID

    def addMargin(self, amount):
        '''
        '''
        self.margin =+ amount

    def getTotalNotional(self):
        total_notional = 0
        for pos in self.positions:
            total_notional += abs(pos.size)
        return total_notional 

    def openPosition(self, Market, size):
        '''
        '''
        # Total cross-margin leverage must be lower than 10x
        assert (abs(size) + self.getTotalNotional())/self.margin < 10
        pos = Market.openPosition(self.ID, size)
        self.positions.append(pos)
        return pos

    def closePosition(self, pos_index, markets):
        '''
        Takes in the position index in the positions array of the trader 
        and dictionary of markets whose keys are their ID and removes the 
        position from both the relevant market and the trader's portfolio, 
        adding the trader's pnl to their margin account.
        '''
        pos = self.positions[pos_index]
        Market = markets[pos.marketID]
        pnl = pos.getUnrealizedPnL(Market)
        Market.closePosition(pos.traderID)
        self.margin += pnl 
        self.positions.pop(pos_index)

    def getMarginRatio(self, markets):
        '''
        Given a dictionary of markets where each index is the market ID, 
        return the cross margin ratio of the trader across all of these 
        markets.
        '''
        total_collateral = self.margin
        notional = 0
        for pos in self.positions: 
            total_collateral += pos.getUnrealizedPnL(markets[pos.marketID]) 
            notional += pos.getNotional(markets[pos.marketID])
