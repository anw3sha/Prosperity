from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string
import jsonpickle
import pandas as pd

class Trader:

    def run(self, state: TradingState):
        # Only method required. It takes all buy and sell orders for all symbols as an input, and outputs a list of orders to be sent
        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))
        result = {}
        for product in state.order_depths:
            order_depth: OrderDepth = state.order_depths[product]
            orders: List[Order] = []
            if product == 'AMETHYSTS':
                acceptable_price = 10000

                print("Acceptable price : " + str(acceptable_price))
                print("Buy Order depth : " + str(len(order_depth.buy_orders)) + ", Sell order depth : " + str(len(order_depth.sell_orders)))
        
                if len(order_depth.sell_orders) != 0:
                    best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
                    if int(best_ask) < acceptable_price:
                        print("BUY", str(-best_ask_amount) + "x", best_ask)
                        orders.append(Order(product, best_ask, -best_ask_amount))
        
                if len(order_depth.buy_orders) != 0:
                    best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
                    if int(best_bid) > acceptable_price:
                        print("SELL", str(best_bid_amount) + "x", best_bid)
                        orders.append(Order(product, best_bid, -best_bid_amount))
            
            elif product == 'STARFRUIT':
                try:
                    trader_data = jsonpickle.decode(state.traderData)
                except:
                    trader_data = {}
                time = state.timestamp
                if time < 10000:
                    acceptable_price = 5035                                                                                                                                                                                                                                                        
                else:
                    acceptable_price = 5060

                    print("Acceptable price : " + str(acceptable_price))
                    print("Buy Order depth : " + str(len(order_depth.buy_orders)) + ", Sell order depth : " + str(len(order_depth.sell_orders)))
        
                    if len(order_depth.sell_orders) != 0:
                        best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
                        if int(best_ask) < acceptable_price:
                            print("BUY", str(-best_ask_amount) + "x", best_ask)
                            orders.append(Order(product, best_ask, -best_ask_amount))
        
                    if len(order_depth.buy_orders) != 0:
                        best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
                        if int(best_bid) > acceptable_price:
                            print("SELL", str(best_bid_amount) + "x", best_bid)
                            orders.append(Order(product, best_bid, -best_bid_amount))

            else:
                # for starfruit, it's a more complex strategy (because it changes frequently and acts more like a common stock)
                # the price range seems to be around 5000 but fluctuates a lot
                # variance: 1043.4868407835816
                # let's use a moving average to determine the median price and make a market around that
                # we will store {"previous": previous_average} in traderData and use that to calculate the new average
                alpha = 0.9
                try:
                    trader_data = jsonpickle.decode(state.traderData)
                except:
                    trader_data = {}
                
                # if we don't have previous data, initialize it to the first price
                if product not in trader_data:
                    trader_data[product] = list(order_depth.sell_orders.keys())[0]
                
                guess = trader_data[product] * (1 - alpha) + alpha * ((list(order_depth.sell_orders.keys())[0] + list(order_depth.buy_orders.keys())[0]) / 2)
                
                # our market will be around the guess with 10% margin
                acceptable_buy = guess * 0.99
                acceptable_sell = guess * 1.01

                if len(order_depth.sell_orders) != 0:
                    best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
                    if int(best_ask) < acceptable_buy:
                        print("BUY", str(-best_ask_amount) + "x", best_ask)
                        orders.append(Order(product, best_ask, -best_ask_amount))
        
                if len(order_depth.buy_orders) != 0:
                    best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
                    if int(best_bid) > acceptable_sell:
                        print("SELL", str(best_bid_amount) + "x", best_bid)
                        orders.append(Order(product, best_bid, -best_bid_amount))
                
            
            result[product] = orders
    
    
        traderData = "SAMPLE" # jsonpickle.encode(trader_data) # String value holding Trader state data required. It will be delivered as TradingState.traderData on next execution.
        
        conversions = 1
        return result, conversions, traderData