"""
Main Window Module
Contains the main application window with tabs
"""
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import pytz
from gui.styles import *
from gui.trading_tab import TradingTab
from gui.settings_tab import SettingsTab

class MainWindow:
    """Main application window"""
    
    def __init__(self, config, save_config_func, ib_connector, toast):
        self.config = config
        self.save_config = save_config_func
        self.ib = ib_connector
        self.toast = toast
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("IB Order Panel")
        self.root.geometry("540x820")
        self.root.resizable(False, False)
        self.root.configure(bg=bg_color, padx=5, pady=5)
        
        # Configure styles
        self.style = ttk.Style(self.root)
        self.style.theme_use("clam")
        configure_styles(self.style)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=0, pady=0)
        
        # Create trading tab
        self.trading_tab = TradingTab(self.notebook, config, save_config_func, ib_connector, toast)
        self.notebook.add(self.trading_tab.frame, text='Trading')
        
        # Create settings tab
        self.settings_tab = SettingsTab(self.notebook, config, save_config_func, ib_connector, toast)
        self.notebook.add(self.settings_tab.frame, text='Settings')
        
        # Configure combobox options
        configure_combobox_options(self.root)
        
        # Add ET Time Display
        self._build_time_display()
        
        # Add Pin Button
        self._build_pin_button()
        
        # Set up hotkeys
        self.settings_tab.set_bind_hotkeys_callback(self.bind_hotkeys)
        
        # Schedule initial tasks
        self.root.after(500, self.settings_tab.update_connection_status)
        self.root.after(600, self.bind_hotkeys)
        self.root.after(100, self.trading_tab.refresh_account_basic)
    
    def _build_time_display(self):
        """Build ET time display in top-right corner"""
        self.et_time_label = tk.Label(
            self.root,
            text="",
            font=("Segoe UI", 10),
            fg=fg_color,
            bg=bg_color,
            padx=5,
            pady=2
        )
        self.et_time_label.place(relx=1.0, x=-90, y=5, anchor="ne")
        self._update_et_time()
    
    def _update_et_time(self):
        """Update the ET time display"""
        et_tz = pytz.timezone('America/New_York')
        et_time = datetime.now(et_tz)
        time_str = et_time.strftime("%H:%M:%S ET")
        self.et_time_label.config(text=time_str)
        self.root.after(1000, self._update_et_time)
    
    def _build_pin_button(self):
        """Build always-on-top pin button"""
        self.topmost_var = tk.BooleanVar(value=True)
        
        self.pin_btn = tk.Button(
            self.root,
            text="📍",
            font=("Segoe UI", 12),
            fg=accent_color,
            bg=bg_color,
            activebackground=bg_color,
            activeforeground="#81A1C1",
            bd=0,
            relief='flat',
            cursor='hand2',
            command=self._toggle_topmost,
            padx=5,
            pady=2
        )
        self.pin_btn.place(relx=1.0, x=-5, y=-5, anchor="ne")
        
        # Set initial topmost state
        self.root.attributes('-topmost', True)
    
    def _toggle_topmost(self):
        """Toggle always-on-top state"""
        self.topmost_var.set(not self.topmost_var.get())
        self.root.attributes('-topmost', self.topmost_var.get())
        
        # Update button appearance
        if self.topmost_var.get():
            self.pin_btn.config(fg=accent_color, text="📍")
        else:
            self.pin_btn.config(fg="#4C566A", text="📌")
    
    def bind_hotkeys(self):
        """Bind hotkeys to functions"""
        # Unbind previous hotkeys
        for key in ['<F1>', '<F2>', '<F3>', '<F4>', '<F5>', '<F6>', '<F7>', '<F8>', 
                    '<F9>', '<F10>', '<F11>', '<F12>', '<Control-r>', '<Alt-p>']:
            try:
                self.root.unbind(key)
            except:
                pass
        
        # Bind new hotkeys
        try:
            refresh_key = self.config.get("hotkey_refresh", "F5")
            if not refresh_key.startswith('<'):
                refresh_key = f"<{refresh_key}>"
            
            def refresh_handler(e):
                self.trading_tab.refresh_account_info()
                return "break"
            
            self.root.bind(refresh_key, refresh_handler)
            print(f"Bound {refresh_key} to Refresh")
        except Exception as e:
            print(f"Failed to bind refresh hotkey: {e}")
        
        try:
            place_order_key = self.config.get("hotkey_place_order", "F9")
            if not place_order_key.startswith('<'):
                place_order_key = f"<{place_order_key}>"
            
            def place_order_handler(e):
                self.trading_tab.submit_order()
                return "break"
            
            self.root.bind(place_order_key, place_order_handler)
            print(f"Bound {place_order_key} to Place Order")
        except Exception as e:
            print(f"Failed to bind place order hotkey: {e}")
    
    def run(self):
        """Run the application main loop"""
        self.root.mainloop()



