class Position():
    '''
    '''
    def __init__(self, traderID, marketID, notional, base_asset_amount, side) -> None:
        self.marketID = marketID
        self.traderID = traderID
        # Initial net value of the position in quote asset
        self.initial_notional = notional
        # Base asset amount in the position
        self.size = base_asset_amount
        self.side = side

    def getUnrealizedPnL(self, Market):
        '''
        '''
        # Check that the position belongs to the correct market
        assert self.marketID == Market.ID
        current_quote = Market.quote_reserves
        current_base = Market.base_reserves
        notional = abs(Market.swapBaseIn(self.size)[0])
        if self.side == "short":
            return self.initial_notional - notional
        Market.quote_reserves = current_quote
        Market.base_reserves = current_base
        return notional - self.initial_notional

    def getNotional(self, Market):
        '''
        '''
        return abs(Market.swapBaseIn(self.size)[0])

