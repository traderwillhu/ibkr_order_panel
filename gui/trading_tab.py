"""
Trading Tab Module
Contains the main trading interface
"""
import tkinter as tk
from tkinter import ttk
from gui.styles import *

class TradingTab:
    """Trading interface tab"""
    
    def __init__(self, parent, config, save_config_func, ib_connector, toast):
        self.parent = parent
        self.config = config
        self.save_config = save_config_func
        self.ib = ib_connector
        self.toast = toast
        
        # Create main frame
        self.frame = tk.Frame(parent, bg=bg_color, padx=20, pady=15)
        
        # Labels that will be updated
        self.label_net_liq = None
        self.label_cash = None
        self.label_buying_power = None
        self.label_current_price = None
        self.label_position_pct = None
        self.label_position_value = None
        self.label_trade_position = None
        self.label_total_position = None
        
        # Entry fields
        self.entry_ticker = None
        self.entry_qty = None
        self.entry_risk = None
        self.entry_entry = None
        self.entry_stop = None
        
        # Buttons
        self.submit_btn = None
        self.watchlist_buttons = []
        self.risk_buttons = []
        
        # Variables
        self.action_var = tk.StringVar(value='BUY')
        self.order_type_var = tk.StringVar(value='Market + 3 Stops')
        self.use_lod_var = tk.BooleanVar(value=False)
        self.use_hod_var = tk.BooleanVar(value=False)
        
        # Build the interface
        self._build_interface()
    
    def _build_interface(self):
        """Build the trading interface"""
        root = self.frame
        
        # ========== Account Info Section ==========
        account_frame = ttk.Frame(root)
        account_frame.grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky="ew")
        
        # Account content frame
        account_content_frame = tk.Frame(account_frame, bg=entry_bg)
        account_content_frame.pack(fill='both', expand=True, padx=8, pady=8)
        
        # Configure grid columns
        account_content_frame.grid_columnconfigure(0, weight=1)
        account_content_frame.grid_columnconfigure(1, weight=0)
        
        # Left side: Account info labels
        account_info_frame = tk.Frame(account_content_frame, bg=entry_bg)
        account_info_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
        
        self.label_net_liq = ttk.Label(account_info_frame, text="Net Liquidation: Loading...", style="AccountInfo.TLabel")
        self.label_net_liq.pack(pady=2, anchor="w")
        
        self.label_cash = ttk.Label(account_info_frame, text="Cash Balance: Loading...", style="AccountInfo.TLabel")
        self.label_cash.pack(pady=2, anchor="w")
        
        self.label_buying_power = ttk.Label(account_info_frame, text="Buying Power: Loading...", style="AccountInfo.TLabel")
        self.label_buying_power.pack(pady=2, anchor="w")
        
        # Separator line
        separator1 = ttk.Separator(account_info_frame, orient='horizontal')
        separator1.pack(fill='x', pady=5)
        
        self.label_current_price = ttk.Label(account_info_frame, text="Current Price: N/A", style="AccountInfo.TLabel")
        self.label_current_price.pack(pady=2, anchor="w")
        
        self.label_position_pct = ttk.Label(account_info_frame, text="Current Position %: N/A", style="AccountInfo.TLabel")
        self.label_position_pct.pack(pady=2, anchor="w")
        
        self.label_position_value = ttk.Label(account_info_frame, text="Current Value: N/A", style="AccountInfo.TLabel")
        self.label_position_value.pack(pady=2, anchor="w")
        
        # Separator line
        separator2 = ttk.Separator(account_info_frame, orient='horizontal')
        separator2.pack(fill='x', pady=5)
        
        # Trade calculation info
        self.label_trade_position = ttk.Label(account_info_frame, text="Trade Position %: N/A", style="TradeInfo.TLabel")
        self.label_trade_position.pack(pady=2, anchor="w")
        
        # Total position after trade
        self.label_total_position = ttk.Label(account_info_frame, text="Total After Trade: N/A", style="TotalInfo.TLabel")
        self.label_total_position.pack(pady=2, anchor="w")
        
        # Right side: Watchlist section
        self._build_watchlist(account_content_frame)
        
        # Button Frame for Refresh and Place Order
        button_frame_account = tk.Frame(account_frame, bg=entry_bg)
        button_frame_account.pack(pady=6, padx=8)
        
        # Refresh Button
        refresh_btn = ttk.Button(button_frame_account, text="Refresh", command=self.refresh_account_info)
        refresh_btn.pack(side="left", padx=5)
        
        # Place Order Button
        self.submit_btn = ttk.Button(button_frame_account, text="Place Order", command=self.submit_order)
        self.submit_btn.pack(side="left", padx=5)
        
        # ========== Input Fields ==========
        self.entry_ticker = self._add_input("Ticker Symbol:", "AAPL", 2)
        self.entry_qty = self._add_input("Order Quantity:", "99", 3)
        
        # Risk % with quick percentage buttons
        self._build_risk_input(4)
        
        self.entry_entry = self._add_input("Entry Price:", "200", 5)
        
        # Stop Price with LOD/HOD checkbox
        self._build_stop_input(6)
        
        # Action Selection
        ttk.Label(root, text="Action:").grid(row=7, column=0, sticky="e", pady=10, padx=(0,10))
        action_frame = tk.Frame(root, bg=bg_color)
        action_frame.grid(row=7, column=1, sticky="w", pady=10)
        ttk.Radiobutton(action_frame, text="Buy", variable=self.action_var, value='BUY', style="TRadiobutton").pack(side="left", padx=15)
        ttk.Radiobutton(action_frame, text="Sell (Short)", variable=self.action_var, value='SELL', style="TRadiobutton").pack(side="left", padx=15)
        
        # Order Type Dropdown
        ttk.Label(root, text="Order Type:").grid(row=8, column=0, sticky="e", pady=10, padx=(0,10))
        order_type_combo = ttk.Combobox(root, textvariable=self.order_type_var, state='readonly',
            values=[
                'Market + 3 Stops',
                'Market + 1 Stop',
                '3 Stops Only',
                'Market Order',
                'Limit Order',
                'Stop Order'
            ],
            font=FONT_LARGE)
        order_type_combo.grid(row=8, column=1, sticky="ew", pady=10)
        
        root.grid_columnconfigure(1, weight=1)
    
    def _add_input(self, label_text, default_val, row):
        """Helper to add input field"""
        ttk.Label(self.frame, text=label_text).grid(row=row, column=0, sticky="e", pady=8, padx=(0,10))
        entry = ttk.Entry(self.frame, font=FONT_LARGE)
        entry.insert(0, default_val)
        entry.grid(row=row, column=1, sticky="ew", pady=8)
        return entry
    
    def _build_risk_input(self, row):
        """Build risk percentage input with quick buttons"""
        ttk.Label(self.frame, text="Risk %:").grid(row=row, column=0, sticky="e", pady=8, padx=(0,10))
        risk_frame = tk.Frame(self.frame, bg=bg_color)
        risk_frame.grid(row=row, column=1, sticky="ew", pady=8)
        
        self.entry_risk = ttk.Entry(risk_frame, font=FONT_LARGE, width=12)
        self.entry_risk.insert(0, self.config.get("risk_percent", "1.0"))
        self.entry_risk.pack(side="left", padx=(0, 10))
        
        # Save risk % when it changes
        self.entry_risk.bind('<FocusOut>', self._save_risk_percent)
        self.entry_risk.bind('<Return>', self._save_risk_percent)
        
        # Quick percentage buttons
        risk_percentages = self.config.get("risk_buttons", [0.25, 0.5, 1.5])
        for percent in risk_percentages:
            btn = tk.Button(
                risk_frame,
                text=f"{percent:.2f}%",
                font=("Segoe UI", 9, "bold"),
                fg="white",
                bg=button_color,
                activebackground="#81A1C1",
                activeforeground="white",
                bd=0,
                relief='flat',
                cursor='hand2',
                command=lambda p=percent: self._set_risk_percent(p),
                padx=6,
                pady=2
            )
            btn.pack(side="left", padx=2)
            self.risk_buttons.append(btn)
        
        # Edit risk buttons button
        edit_risk_btn = tk.Button(
            risk_frame,
            text="⚙️",
            font=("Segoe UI", 9),
            fg=fg_color,
            bg=bg_color,
            activebackground="#434C5E",
            activeforeground=accent_color,
            bd=0,
            relief='flat',
            cursor='hand2',
            command=self._edit_risk_buttons,
            padx=4,
            pady=0
        )
        edit_risk_btn.pack(side="left", padx=(5, 0))
    
    def _build_stop_input(self, row):
        """Build stop price input with LOD/HOD checkboxes"""
        ttk.Label(self.frame, text="Stop Price:").grid(row=row, column=0, sticky="e", pady=8, padx=(0,10))
        stop_frame = tk.Frame(self.frame, bg=bg_color)
        stop_frame.grid(row=row, column=1, sticky="ew", pady=8)
        
        self.entry_stop = ttk.Entry(stop_frame, font=FONT_LARGE, width=12)
        self.entry_stop.insert(0, "190")
        self.entry_stop.pack(side="left", padx=(0, 10))
        
        use_lod_check = ttk.Checkbutton(
            stop_frame,
            text="LOD",
            variable=self.use_lod_var,
            command=self._update_stop_with_lod,
            style="TCheckbutton"
        )
        use_lod_check.pack(side="left", padx=3)
        
        use_hod_check = ttk.Checkbutton(
            stop_frame,
            text="HOD",
            variable=self.use_hod_var,
            command=self._update_stop_with_hod,
            style="TCheckbutton"
        )
        use_hod_check.pack(side="left", padx=3)
    
    def _build_watchlist(self, parent):
        """Build watchlist section"""
        watchlist_container = tk.Frame(parent, bg=entry_bg)
        watchlist_container.grid(row=0, column=1, sticky='ne', pady=(40, 0))
        
        # Watchlist title and edit button
        watchlist_header = tk.Frame(watchlist_container, bg=entry_bg)
        watchlist_header.pack(fill='x', pady=(0, 8))
        
        watchlist_title = tk.Label(
            watchlist_header,
            text="Watchlist",
            font=("Segoe UI", 10, "bold"),
            fg=accent_color,
            bg=entry_bg
        )
        watchlist_title.pack(side='left', padx=(0, 5))
        
        edit_watchlist_btn = tk.Button(
            watchlist_header,
            text="Edit",
            font=("Segoe UI", 9, "bold"),
            fg="white",
            bg=button_color,
            activebackground="#81A1C1",
            activeforeground="white",
            bd=0,
            relief='flat',
            cursor='hand2',
            command=self._edit_watchlist,
            padx=8,
            pady=2
        )
        edit_watchlist_btn.pack(side='left')
        
        # Watchlist buttons frame
        watchlist_frame = tk.Frame(watchlist_container, bg=entry_bg)
        watchlist_frame.pack()
        
        # Get watchlist from config
        watchlist = self.config.get("watchlist", ["AAPL", "TSLA", "NVDA", "MSFT", "GOOGL", "AMZN", "META", "SPY", "QQQ", "IWM"])
        
        # Create 10 watchlist buttons in 2 columns, 5 rows
        for i in range(10):
            ticker = watchlist[i] if i < len(watchlist) else ""
            row = i % 5
            col = i // 5
            
            btn = tk.Button(
                watchlist_frame,
                text=ticker if ticker else f"W{i+1}",
                font=("Segoe UI", 9, "bold"),
                fg="white" if ticker else "#4C566A",
                bg=button_color if ticker else "#3B4252",
                activebackground="#81A1C1",
                activeforeground="white",
                bd=0,
                relief='flat',
                cursor='hand2' if ticker else 'arrow',
                padx=8,
                pady=4,
                width=6,
                highlightthickness=0,
                command=lambda t=ticker: self._switch_ticker(t) if t else None
            )
            btn.grid(row=row, column=col, padx=2, pady=2)
            self.watchlist_buttons.append((btn, ticker))
    
    def _switch_ticker(self, ticker_symbol):
        """Switch to a ticker and refresh automatically"""
        if ticker_symbol:
            self.entry_ticker.delete(0, tk.END)
            self.entry_ticker.insert(0, ticker_symbol)
            self.refresh_account_info()
    
    def _set_risk_percent(self, percent):
        """Set risk percentage and refresh"""
        self.entry_risk.delete(0, tk.END)
        self.entry_risk.insert(0, f"{percent:.2f}")
        self.config["risk_percent"] = f"{percent:.2f}"
        self.save_config(self.config)
        self.refresh_account_info()
    
    def _save_risk_percent(self, event=None):
        """Save risk percentage to config"""
        try:
            risk_value = self.entry_risk.get()
            float(risk_value)  # Validate it's a number
            self.config["risk_percent"] = risk_value
            self.save_config(self.config)
        except:
            pass
    
    def _update_stop_with_lod(self):
        """Mark using LOD"""
        if self.use_lod_var.get():
            self.use_hod_var.set(False)
    
    def _update_stop_with_hod(self):
        """Mark using HOD"""
        if self.use_hod_var.get():
            self.use_lod_var.set(False)
    
    def _edit_watchlist(self):
        """Open dialog to edit watchlist"""
        from gui.dialogs import edit_watchlist_dialog
        edit_watchlist_dialog(self.frame.master.master, self.config, self.save_config, 
                            self.watchlist_buttons, self._switch_ticker, self.toast)
    
    def _edit_risk_buttons(self):
        """Open dialog to edit risk buttons"""
        from gui.dialogs import edit_risk_buttons_dialog
        edit_risk_buttons_dialog(self.frame.master.master, self.config, self.save_config,
                                self.risk_buttons, self._set_risk_percent, self.toast)
    
    def refresh_account_basic(self):
        """Quick refresh of basic account info (no blocking)"""
        try:
            if not self.ib.is_connected():
                return
            account_values = self.ib.get_account_values()
            
            net_liquidation = "N/A"
            cash_balance = "N/A"
            buying_power = "N/A"
            
            for value in account_values:
                if value.tag == 'NetLiquidation' and value.currency == 'USD':
                    net_liquidation = f"${float(value.value):,.2f}"
                elif value.tag == 'CashBalance' and value.currency == 'USD':
                    cash_balance = f"${float(value.value):,.2f}"
                elif value.tag == 'BuyingPower' and value.currency == 'USD':
                    buying_power = f"${float(value.value):,.2f}"
            
            self.label_net_liq.config(text=f"Net Liquidation: {net_liquidation}")
            self.label_cash.config(text=f"Cash Balance: {cash_balance}")
            self.label_buying_power.config(text=f"Buying Power: {buying_power}")
        except:
            pass
    
    def refresh_account_info(self):
        """Full refresh of account and position info"""
        try:
            if not self.ib.is_connected():
                self.toast.show("Not Connected", "Please connect to IB Gateway first.", "warning")
                return
            
            account_values = self.ib.get_account_values()
            
            net_liquidation = "N/A"
            net_liq_value = 0.0
            cash_balance = "N/A"
            buying_power = "N/A"
            
            for value in account_values:
                if value.tag == 'NetLiquidation' and value.currency == 'USD':
                    net_liq_value = float(value.value)
                    net_liquidation = f"${net_liq_value:,.2f}"
                elif value.tag == 'CashBalance' and value.currency == 'USD':
                    cash_balance = f"${float(value.value):,.2f}"
                elif value.tag == 'BuyingPower' and value.currency == 'USD':
                    buying_power = f"${float(value.value):,.2f}"
            
            self.label_net_liq.config(text=f"Net Liquidation: {net_liquidation}")
            self.label_cash.config(text=f"Cash Balance: {cash_balance}")
            self.label_buying_power.config(text=f"Buying Power: {buying_power}")
            
            # Get position info for the ticker
            ticker = self.entry_ticker.get().strip().upper()
            if ticker:
                self._refresh_ticker_info(ticker, net_liq_value)
            else:
                self._clear_ticker_info()
                
        except Exception as e:
            self.toast.show("Error", f"Failed to retrieve account info: {str(e)}", "error")
    
    def _refresh_ticker_info(self, ticker, net_liq_value):
        """Refresh ticker-specific information"""
        try:
            # Show loading status
            self.label_current_price.config(text=f"Current Price ({ticker}): Loading...")
            self.frame.update()
            
            # Get current price
            current_price = self.ib.get_market_data(ticker)
            
            # Get position
            positions = self.ib.get_positions()
            position_qty = 0
            position_value = 0.0
            position_pct = 0.0
            
            for pos in positions:
                if pos.contract.symbol == ticker:
                    position_qty = pos.position
                    if current_price:
                        position_value = abs(position_qty * current_price)
                        if net_liq_value > 0:
                            position_pct = (position_value / net_liq_value) * 100
                    break
            
            # Update current price label
            if current_price:
                self.label_current_price.config(text=f"Current Price ({ticker}): ${current_price:.2f}")
            else:
                self.label_current_price.config(text=f"Current Price ({ticker}): N/A")
                self.label_trade_position.config(text=f"Trade Position %: N/A")
                self.label_total_position.config(text=f"Total After Trade: N/A")
            
            # Update position labels
            if position_qty != 0:
                self.label_position_pct.config(text=f"Current Position %: {position_pct:.2f}% ")
                self.label_position_value.config(text=f"Current Value: ${position_value:,.2f} ({position_qty:+.0f} shares)")
            else:
                self.label_position_pct.config(text=f"Current Position %: 0.00% (no position)")
                self.label_position_value.config(text=f"Current Value: $0.00")
            
            # Auto-update LOD/HOD if selected
            if self.use_lod_var.get() or self.use_hod_var.get():
                lod, hod = self.ib.get_lod_hod(ticker)
                if self.use_lod_var.get() and lod:
                    self.entry_stop.delete(0, tk.END)
                    self.entry_stop.insert(0, f"{lod:.2f}")
                elif self.use_hod_var.get() and hod:
                    self.entry_stop.delete(0, tk.END)
                    self.entry_stop.insert(0, f"{hod:.2f}")
            
            # Auto-calculate quantity based on risk %
            if current_price:
                self._calculate_position_size(current_price, net_liq_value, position_qty)
                
        except Exception as e:
            import traceback
            print(f"Error getting position info for {ticker}: {str(e)}")
            print(traceback.format_exc())
            self._clear_ticker_info(ticker)
    
    def _calculate_position_size(self, current_price, net_liq_value, position_qty):
        """Calculate position size based on risk percentage"""
        try:
            risk_pct = float(self.entry_risk.get())
            stop_price = float(self.entry_stop.get())
            action = self.action_var.get()
            
            if 0 < risk_pct <= 100 and net_liq_value > 0:
                # Calculate risk per share
                if action == 'BUY':
                    risk_per_share = current_price - stop_price
                else:  # SELL
                    risk_per_share = stop_price - current_price
                
                if risk_per_share > 0:
                    # Calculate quantity
                    risk_amount = net_liq_value * (risk_pct / 100)
                    quantity = int(risk_amount / risk_per_share)
                    
                    if quantity > 0:
                        # Update the quantity field
                        self.entry_qty.delete(0, tk.END)
                        self.entry_qty.insert(0, str(quantity))
                        
                        # Calculate and display trade position percentage
                        trade_value = quantity * current_price
                        trade_pct = (trade_value / net_liq_value) * 100
                        self.label_trade_position.config(
                            text=f"Trade Position %: {trade_pct:.2f}% (${trade_value:,.2f})"
                        )
                        
                        # Calculate total position after trade
                        if action == 'BUY':
                            total_qty = position_qty + quantity
                        else:  # SELL
                            total_qty = position_qty - quantity
                        
                        total_value = abs(total_qty) * current_price
                        total_pct = (total_value / net_liq_value) * 100 if net_liq_value > 0 else 0
                        
                        self.label_total_position.config(
                            text=f"Total After Trade: {total_pct:.2f}% (${total_value:,.2f})"
                        )
                    else:
                        self.label_trade_position.config(text=f"Trade Position %: N/A")
                        self.label_total_position.config(text=f"Total After Trade: N/A")
                else:
                    self.label_trade_position.config(text=f"Trade Position %: N/A (Invalid parameters)")
                    self.label_total_position.config(text=f"Total After Trade: N/A")
        except:
            self.label_trade_position.config(text=f"Trade Position %: N/A")
            self.label_total_position.config(text=f"Total After Trade: N/A")
    
    def _clear_ticker_info(self, ticker=""):
        """Clear ticker-specific information"""
        price_text = f"Current Price ({ticker}): N/A" if ticker else "Current Price: N/A"
        self.label_current_price.config(text=price_text)
        self.label_position_pct.config(text=f"Current Position %: N/A")
        self.label_position_value.config(text=f"Current Value: N/A")
        self.label_trade_position.config(text=f"Trade Position %: N/A")
        self.label_total_position.config(text=f"Total After Trade: N/A")
    
    def submit_order(self):
        """Submit order to IB"""
        try:
            if not self.ib.is_connected():
                self.toast.show("Not Connected", "Please connect to IB Gateway first.", "error")
                return
            
            # Disable button and show placing order status
            self.submit_btn.config(state='disabled', text='Placing Order...')
            self.frame.update()
            
            ticker = self.entry_ticker.get().strip().upper()
            qty = int(self.entry_qty.get())
            stop_price = float(self.entry_stop.get())
            entry_price = float(self.entry_entry.get())
            action = self.action_var.get()
            order_type = self.order_type_var.get()
            
            success, message = self.ib.submit_order(ticker, qty, stop_price, entry_price, action, order_type)
            
            if success:
                self.toast.show("Success", message, "success", 5000)
            else:
                self.toast.show("Order Error", message, "error")
                
        except Exception as e:
            self.toast.show("Error", str(e), "error")
        finally:
            # Restore button state
            self.submit_btn.config(state='normal', text='Place Order')



