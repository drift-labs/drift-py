from Trader import Trader 
from Market import Market
from Position import Position 


# Create a market
k0 = 1e6
initial_mark = 2000
index = 2000
marketID = 1
market = Market(k0, initial_mark, index, marketID)

# The reserves should do a round trip if we swap quote 
# and base back to back

initial_quote = market.quote_reserves
initial_base = market.base_reserves
base_obtained = -market.swapQuoteIn(0.1)[0]
_, _ = market.swapBaseIn(base_obtained)
assert initial_quote == market.quote_reserves
assert initial_base == market.base_reserves


# The spot price should do a round trip if we take equal 
# long and short positions back to back

initial_spot = market.getSpot()
trader1 = Trader(1, 1000)
trader1.addMargin(100)
trader1.openPosition(market, -10)
trader1.openPosition(market, 10)
end_spot = market.getSpot()

print("Initial spot: ", initial_spot)
print("End spot = ", end_spot)

assert initial_spot == end_spot

# Two small swaps in one direction back to back should have gradually 
# lower/greater effective prices

_, effective_price_1 = market.swapQuoteIn(1)
print("Effective price 1: ", effective_price_1)
_, effective_price_2 = market.swapQuoteIn(1)
print("Effective price 2: ", effective_price_2)

assert effective_price_1 < effective_price_2

_, effective_price_1 = market.swapBaseIn(0.1)
print("Effective price 1: ", effective_price_1)
_, effective_price_2 = market.swapBaseIn(0.1)
print("Effective price 2: ", effective_price_2)

assert effective_price_1 > effective_price_2

# Opening an epsilon long position followed by a 10% drop in price 
# should lead to ~10% losses

trader1.openPosition(market, 0.1)
market.pegMultiplier = market.pegMultiplier*0.9
profit = trader1.positions[-1].getUnrealizedPnL(market)
print("Profit in quote asset: ", profit)
print("Profit in %: ", 100*round(profit/0.1,1), "%")

assert round(profit/0.1,2) == -0.1


# Create a trader with some margin and a short position

# trader1 = Trader(1, 1000)
# trader2 = Trader(2, 1000)
# trader1.addMargin(100)
# trader2.addMargin(100)
# print("Initial spot: ", market.getSpot())
# trader1.openPosition(market, -10)
# # print(trader.positions[0])
# print("Spot after trader 1 position: ", market.getSpot())
# trader2.openPosition(market, -10)
# print("Spot after trader 2 position: ", market.getSpot())
# print(market.positions)
# for pos in market.positions:
#     if pos.traderID == 1:
#         print("Trader 1 position pnl: ", pos.getUnrealizedPnL(market)) 
#         break


