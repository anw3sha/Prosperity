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
            try:
                trader_data = jsonpickle.decode(state.traderData)
            except:
                trader_data = {'AMETHYSTS': []}

            # Calculate the mid price of the current state
            if len(order_depth.sell_orders) != 0 and len(order_depth.buy_orders) != 0:
                total_price = sum(order_depth.sell_orders.keys()) + sum(order_depth.buy_orders.keys())
                total_orders = len(order_depth.sell_orders) + len(order_depth.buy_orders)
                mid_price = total_price / total_orders

                # Add the mid price to the list of previous mid prices
                trader_data['AMETHYSTS'].append(mid_price)

                # If there are more than 50 entries, calculate the average of the last 50 mid prices
                if len(trader_data['AMETHYSTS']) > 50:
                    acceptable_price = sum(trader_data['AMETHYSTS'][-50:]) / 50
                else:
                    acceptable_price = 10000  # Default price for the first 50 entries

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

            result[product] = orders
        
        trader_data = "SAMPLE"
        traderData = jsonpickle.encode(trader_data) # "SAMPLE" # String value holding Trader state data required. It will be delivered as TradingState.traderData on next execution.
        conversions = 1
        return result, conversions, traderData