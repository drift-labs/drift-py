import numpy as np

def generateGBM(T, mu, sigma, S0, dt):
    '''
    Generate a geometric brownian motion time series. Shamelessly copy pasted from here: https://stackoverflow.com/a/13203189

    Params: 

    T: time horizon 
    mu: drift
    sigma: percentage volatility
    S0: initial price
    dt: size of time steps

    Returns: 

    t: time array
    S: time series
    '''
    N = round(T/dt)
    t = np.linspace(0, T, N)
    W = np.random.standard_normal(size = N) 
    W = np.cumsum(W)*np.sqrt(dt) ### standard brownian motion ###
    X = (mu-0.5*sigma**2)*t + sigma*W 
    S = S0*np.exp(X) ### geometric brownian motion ###
    return t, S

def liquidate(Trader, markets):
    '''
    Check if the trader's cross margin ratio is in the liquidation zone, and if yes
    liquidate their position following the Drift logic of liquidation.
    '''
    ratio = Trader.getMarginRatio(markets)
    if ratio < 0.0625:
        for pos in Trader.positions:
            Market = markets[pos.marketID]
            size = pos.size
            quote_out = Market.swapBaseIn(0.25*size)
            Trader.margin += quote_out
        Trader.margin = Trader.margin*0.975
    if ratio < 0.05:
        for i in range(len(Trader.positions)):
            Trader.close(i, markets)
        Trader.margin = 0        