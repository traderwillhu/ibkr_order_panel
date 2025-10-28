"""
IB Connector Module
Handles connection to Interactive Brokers and trading operations
"""
from ib_insync import *
import time

class IBConnector:
    """Interactive Brokers Connection Manager"""
    
    def __init__(self):
        self.ib = IB()
        self.toast = None  # Will be set by main application
    
    def connect(self, port=4001):
        """Connect to IB Gateway/TWS"""
        try:
            if self.ib.isConnected():
                print("Disconnecting existing connection...")
                self.ib.disconnect()
                time.sleep(0.5)
            
            print(f"Connecting to IB Gateway on port {port}...")
            self.ib.connect('127.0.0.1', port, clientId=1, timeout=10)
            print("Connected successfully!")
            return True
        except Exception as e:
            print(f"Warning: Could not connect to IB Gateway: {e}")
            print("The program will continue, but trading functions will not work until connected.")
            return False
    
    def is_connected(self):
        """Check if connected to IB"""
        return self.ib.isConnected()
    
    def disconnect(self):
        """Disconnect from IB"""
        if self.ib.isConnected():
            self.ib.disconnect()
    
    def get_account_values(self):
        """Get account values"""
        if not self.ib.isConnected():
            return None
        return self.ib.accountValues()
    
    def get_positions(self):
        """Get current positions"""
        if not self.ib.isConnected():
            return []
        return self.ib.positions()
    
    def get_market_data(self, ticker, timeout=5):
        """
        Get market data for a ticker
        Returns: current_price or None
        """
        try:
            contract = Stock(ticker, 'SMART', 'USD')
            self.ib.qualifyContracts(contract)
            
            # Cancel any existing market data for this contract first (silently)
            try:
                for ticker_obj in self.ib.tickers():
                    if ticker_obj.contract.symbol == ticker:
                        self.ib.cancelMktData(ticker_obj.contract)
                        self.ib.sleep(0.1)
            except:
                pass
            
            # Request fresh market data
            self.ib.reqMktData(contract, '', False, False)
            self.ib.sleep(1)  # Give initial time for data to start flowing
            
            # Wait for valid market data
            current_price = None
            for i in range(10):
                ticker_data = self.ib.ticker(contract)
                
                if ticker_data.marketPrice() and ticker_data.marketPrice() > 0:
                    current_price = ticker_data.marketPrice()
                    break
                elif ticker_data.last and ticker_data.last > 0:
                    current_price = ticker_data.last
                    break
                elif ticker_data.close and ticker_data.close > 0:
                    current_price = ticker_data.close
                    break
                
                self.ib.sleep(0.5)
            
            # If still no price, try one last time
            if not current_price:
                ticker_data = self.ib.ticker(contract)
                if ticker_data.marketPrice() and ticker_data.marketPrice() > 0:
                    current_price = ticker_data.marketPrice()
                elif ticker_data.last and ticker_data.last > 0:
                    current_price = ticker_data.last
                elif ticker_data.close and ticker_data.close > 0:
                    current_price = ticker_data.close
            
            self.ib.cancelMktData(contract)
            return current_price
        except Exception as e:
            print(f"Error getting market data for {ticker}: {e}")
            return None
    
    def get_lod_hod(self, ticker):
        """
        Get Low of Day (LOD) and High of Day (HOD) for a ticker
        Returns: (lod, hod) or (None, None)
        """
        try:
            contract = Stock(ticker, 'SMART', 'USD')
            self.ib.qualifyContracts(contract)
            bars = self.ib.reqHistoricalData(
                contract,
                endDateTime='',
                durationStr='1 D',
                barSizeSetting='1 min',
                whatToShow='TRADES',
                useRTH=True,
                formatDate=1
            )
            if bars:
                lod = min(bar.low for bar in bars)
                hod = max(bar.high for bar in bars)
                return lod, hod
            return None, None
        except Exception as e:
            print(f"Error getting LOD/HOD for {ticker}: {e}")
            return None, None
    
    def submit_order(self, ticker, qty, stop_price, entry_price, action, order_type):
        """
        Submit an order to IB
        Returns: (success, message)
        """
        try:
            if not self.ib.isConnected():
                return False, "Not connected to IB Gateway"
            
            contract = Stock(ticker, 'SMART', 'USD')
            self.ib.qualifyContracts(contract)

            if order_type == 'Market + 3 Stops':
                market_order = MarketOrder(action, qty)
                trade = self.ib.placeOrder(contract, market_order)
                while trade.isActive():
                    self.ib.sleep(1)

                if trade.orderStatus.status != 'Filled':
                    return False, "Market order was not filled."

                avg_fill_price = trade.orderStatus.avgFillPrice
                price_diff = avg_fill_price - stop_price if action == 'BUY' else stop_price - avg_fill_price

                stop_prices = [
                    round(stop_price + price_diff * 2 / 3, 2) if action == 'BUY' else round(stop_price - price_diff * 2 / 3, 2),
                    round(stop_price + price_diff * 1 / 3, 2) if action == 'BUY' else round(stop_price - price_diff * 1 / 3, 2),
                    round(stop_price, 2)
                ]
                stop_sizes = [qty // 3, qty // 3, qty - 2 * (qty // 3)]

                for sp, sq in zip(stop_prices, stop_sizes):
                    stop_order = StopOrder('SELL' if action == 'BUY' else 'BUY', sq, sp, tif='GTC')
                    self.ib.placeOrder(contract, stop_order)
                    self.ib.sleep(0.5)

                return True, f"{action} {qty} shares of {ticker} at ${avg_fill_price:.2f}. 3 stop-loss orders submitted."

            elif order_type == '3 Stops Only':
                price_diff = entry_price - stop_price if action == 'BUY' else stop_price - entry_price
                stop_prices = [
                    round(stop_price + price_diff * 2 / 3, 2) if action == 'BUY' else round(stop_price - price_diff * 2 / 3, 2),
                    round(stop_price + price_diff * 1 / 3, 2) if action == 'BUY' else round(stop_price - price_diff * 1 / 3, 2),
                    round(stop_price, 2)
                ]
                stop_sizes = [qty // 3, qty // 3, qty - 2 * (qty // 3)]

                for sp, sq in zip(stop_prices, stop_sizes):
                    stop_order = StopOrder('SELL' if action == 'BUY' else 'BUY', sq, sp, tif='GTC')
                    self.ib.placeOrder(contract, stop_order)
                    self.ib.sleep(0.5)

                return True, f"3 stop-loss orders for {qty} shares of {ticker} submitted."

            elif order_type == 'Limit Order':
                order = LimitOrder(action, qty, entry_price)
                self.ib.placeOrder(contract, order)
                return True, f"Limit order to {action} {qty} shares of {ticker} at ${entry_price:.2f} submitted."

            elif order_type == 'Stop Order':
                order = StopOrder(action, qty, stop_price)
                self.ib.placeOrder(contract, order)
                return True, f"Stop order to {action} {qty} shares of {ticker} at stop ${stop_price:.2f} submitted."

            elif order_type == 'Market + 1 Stop':
                market_order = MarketOrder(action, qty)
                trade = self.ib.placeOrder(contract, market_order)
                while trade.isActive():
                    self.ib.sleep(1)

                if trade.orderStatus.status != 'Filled':
                    return False, "Market order was not filled."

                avg_fill_price = trade.orderStatus.avgFillPrice
                stop_order = StopOrder('SELL' if action == 'BUY' else 'BUY', qty, stop_price, tif='GTC')
                self.ib.placeOrder(contract, stop_order)

                return True, f"{action} {qty} shares of {ticker} at ${avg_fill_price:.2f}. 1 stop-loss order submitted at ${stop_price:.2f}."

            elif order_type == 'Market + 3 Stops + OCO':
                # Place market order
                market_order = MarketOrder(action, qty)
                trade = self.ib.placeOrder(contract, market_order)
                while trade.isActive():
                    self.ib.sleep(1)

                if trade.orderStatus.status != 'Filled':
                    return False, "Market order was not filled."

                avg_fill_price = trade.orderStatus.avgFillPrice
                price_diff = avg_fill_price - stop_price if action == 'BUY' else stop_price - avg_fill_price

                # Calculate the 3 stop prices
                stop_prices = [
                    round(stop_price + price_diff * 2 / 3, 2) if action == 'BUY' else round(stop_price - price_diff * 2 / 3, 2),
                    round(stop_price + price_diff * 1 / 3, 2) if action == 'BUY' else round(stop_price - price_diff * 1 / 3, 2),
                    round(stop_price, 2)
                ]
                # Calculate sizes: 1/3 for OCO, remaining 2/3 divided between the other stops
                oco_qty = qty // 3
                remaining_qty = qty - oco_qty
                stop_sizes = [remaining_qty // 2, remaining_qty - remaining_qty // 2]

                # Calculate 2R price (target price for limit sell)
                if action == 'BUY':
                    target_price = round(avg_fill_price + 2 * price_diff, 2)
                    oco_stop_price = stop_prices[0]  # Highest stop (closest to entry)
                else:
                    target_price = round(avg_fill_price - 2 * price_diff, 2)
                    oco_stop_price = stop_prices[0]  # Highest stop
                
                # Create OCO group ID (unique identifier for the OCO pair)
                oca_group = f"OCO_{int(time.time() * 1000)}"

                # Create limit sell order (target at 2R)
                limit_order = LimitOrder('SELL' if action == 'BUY' else 'BUY', oco_qty, target_price, tif='GTC')
                limit_order.ocaGroup = oca_group
                limit_order.ocaType = 1  # One-Cancels-Other
                
                # Create stop order (highest stop)
                oco_stop_order = StopOrder('SELL' if action == 'BUY' else 'BUY', oco_qty, oco_stop_price, tif='GTC')
                oco_stop_order.ocaGroup = oca_group
                oco_stop_order.ocaType = 1  # One-Cancels-Other

                # Place OCO orders
                self.ib.placeOrder(contract, limit_order)
                self.ib.sleep(0.2)
                self.ib.placeOrder(contract, oco_stop_order)
                self.ib.sleep(0.5)

                # Place the remaining 2 stop orders for the rest of the position
                for i in range(1, 3):  # Only the second and third stops
                    stop_order = StopOrder('SELL' if action == 'BUY' else 'BUY', stop_sizes[i-1], stop_prices[i], tif='GTC')
                    self.ib.placeOrder(contract, stop_order)
                    self.ib.sleep(0.5)

                return True, f"{action} {qty} shares of {ticker} at ${avg_fill_price:.2f}. OCO (Limit@${target_price:.2f}/Stop@${oco_stop_price:.2f}) + 2 stops submitted."

            elif order_type == 'Market Order':
                market_order = MarketOrder(action, qty)
                trade = self.ib.placeOrder(contract, market_order)
                while trade.isActive():
                    self.ib.sleep(1)

                if trade.orderStatus.status != 'Filled':
                    return False, "Market order was not filled."

                avg_fill_price = trade.orderStatus.avgFillPrice
                return True, f"{action} {qty} shares of {ticker} at market price ${avg_fill_price:.2f} submitted."

            else:
                return False, "Unknown order type selected."

        except Exception as e:
            return False, str(e)



