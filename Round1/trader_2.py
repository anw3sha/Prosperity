from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import numpy as np

class Trader:

    def calculate_acceptable_price(self, historical_prices, sensitivity=2):
        """
        Calculate acceptable buy and sell prices based on historical prices.
        `sensitivity` is the number of standard deviations from the mean.
        """
        mean_price = np.mean(historical_prices)
        std_dev = np.std(historical_prices)
        acceptable_buy_price = mean_price - (sensitivity * std_dev)
        acceptable_sell_price = mean_price + (sensitivity * std_dev)
        return acceptable_buy_price, acceptable_sell_price

    def run(self, state: TradingState):
        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))
        result = {}

        for product in state.order_depths:
            order_depth: OrderDepth = state.order_depths[product]
            orders: List[Order] = []

            # Use historical prices to calculate acceptable buy and sell prices
            if product == 'AMETHYSTS':
                # Special handling for AMETHYSTS
                acceptable_buy_price = 10000
                acceptable_sell_price = 10000
            else:
                # Use historical prices to calculate acceptable buy and sell prices
                historical_prices = self.get_historical_prices(state, product)
                acceptable_buy_price, acceptable_sell_price = self.calculate_acceptable_price(historical_prices)


            print("Acceptable buy price : " + str(acceptable_buy_price))
            print("Acceptable sell price : " + str(acceptable_sell_price))
            print("Buy Order depth : " + str(len(order_depth.buy_orders)) + ", Sell order depth : " + str(len(order_depth.sell_orders)))

            if len(order_depth.sell_orders) != 0:
                best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
                if int(best_ask) < acceptable_sell_price:
                    print("BUY", str(-best_ask_amount) + "x", best_ask)
                    orders.append(Order(product, best_ask, -best_ask_amount))
    
            if len(order_depth.buy_orders) != 0:
                best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
                if int(best_bid) > acceptable_buy_price:
                    print("SELL", str(best_bid_amount) + "x", best_bid)
                    orders.append(Order(product, best_bid, -best_bid_amount))
            
            result[product] = orders

        traderData = "SAMPLE"  # Update this value with the appropriate state to carry forward
        conversions = 1  # Update this value if applicable to your strategy
        return result, conversions, traderData


    def get_historical_prices(self, state, product):
        """
        Assume state.observations is a dictionary like:
        {
            'STARFRUIT': [price1, price2, price3, ...],
            'AMETHYSTS': [price1, price2, price3, ...],
            ...
        }
        """
        return state.observations.get(product, [])
