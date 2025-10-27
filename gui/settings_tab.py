"""
Settings Tab Module
Contains the settings interface for connection and hotkeys
"""
import tkinter as tk
from tkinter import ttk
from gui.styles import *

class SettingsTab:
    """Settings interface tab"""
    
    def __init__(self, parent, config, save_config_func, ib_connector, toast):
        self.parent = parent
        self.config = config
        self.save_config = save_config_func
        self.ib = ib_connector
        self.toast = toast
        
        # Create main frame
        self.frame = tk.Frame(parent, bg=bg_color, padx=20, pady=15)
        
        # Connection status label
        self.connection_status_label = None
        
        # Hotkey labels
        self.hotkey_refresh_label = None
        self.hotkey_place_order_label = None
        
        # Hotkey capture variables
        self.capturing_refresh = tk.BooleanVar(value=False)
        self.capturing_place_order = tk.BooleanVar(value=False)
        
        # Build the interface
        self._build_interface()
    
    def _build_interface(self):
        """Build the settings interface"""
        # Connection Status Label
        self.connection_status_label = ttk.Label(
            self.frame,
            text="Connection Status: Checking...",
            font=FONT_MEDIUM,
            background=bg_color,
            foreground=fg_color
        )
        self.connection_status_label.pack(pady=(0, 15))
        
        # Connection Settings Frame
        self._build_connection_settings()
        
        # Info Section
        self._build_info_section()
        
        # Hotkey Settings Frame
        self._build_hotkey_settings()
    
    def _build_connection_settings(self):
        """Build connection settings section"""
        conn_frame = tk.LabelFrame(
            self.frame,
            text="Connection Settings",
            bg=bg_color,
            fg=accent_color,
            font=("Segoe UI", 13, "bold"),
            padx=15,
            pady=15
        )
        conn_frame.pack(fill='x', pady=5)
        
        # Port Input
        ttk.Label(conn_frame, text="Port:").grid(row=0, column=0, sticky="e", pady=10, padx=(0, 10))
        self.port_entry = ttk.Entry(conn_frame, font=FONT_LARGE, width=15)
        self.port_entry.insert(0, self.config.get("port", "4001"))
        self.port_entry.grid(row=0, column=1, sticky="w", pady=10)
        
        ttk.Label(
            conn_frame,
            text="Common ports: 4001 (Paper), 7496 (Live TWS), 4002 (Gateway)",
            font=FONT_SMALL,
            foreground="#6c6c6c"
        ).grid(row=1, column=0, columnspan=2, pady=(0, 10))
        
        # Reconnect Button
        reconnect_btn = ttk.Button(
            conn_frame,
            text="Save & Reconnect",
            command=self._reconnect_ib,
            style="Small.TButton"
        )
        reconnect_btn.grid(row=2, column=0, columnspan=2, pady=8)
        
        # Check connection status button
        check_btn = ttk.Button(
            conn_frame,
            text="Check Connection",
            command=self.update_connection_status,
            style="Small.TButton"
        )
        check_btn.grid(row=3, column=0, columnspan=2, pady=(0, 5))
    
    def _build_info_section(self):
        """Build information section"""
        info_frame = tk.LabelFrame(
            self.frame,
            text="Information",
            bg=bg_color,
            fg=accent_color,
            font=("Segoe UI", 13, "bold"),
            padx=15,
            pady=15
        )
        info_frame.pack(fill='x', pady=15)
        
        info_text = tk.Label(
            info_frame,
            text="Port Configuration:\n"
                 "• 4001 - IB Gateway (Paper Trading)\n"
                 "• 4002 - IB Gateway (Live Trading)\n"
                 "• 7496 - TWS (Paper Trading)\n"
                 "• 7497 - TWS (Live Trading)\n\n"
                 "Make sure TWS or IB Gateway is running\n"
                 "before attempting to connect.",
            bg=bg_color,
            fg=fg_color,
            font=("Segoe UI", 10),
            justify='left'
        )
        info_text.pack(anchor='w', pady=5)
    
    def _build_hotkey_settings(self):
        """Build hotkey settings section"""
        hotkey_frame = tk.LabelFrame(
            self.frame,
            text="Hotkey Settings",
            bg=bg_color,
            fg=accent_color,
            font=("Segoe UI", 13, "bold"),
            padx=15,
            pady=15
        )
        hotkey_frame.pack(fill='x', pady=15)
        
        # Refresh Hotkey
        ttk.Label(hotkey_frame, text="Refresh:").grid(row=0, column=0, sticky="e", pady=8, padx=(0, 10))
        self.hotkey_refresh_label = tk.Label(
            hotkey_frame, 
            text=self.config.get("hotkey_refresh", "F5"),
            bg=entry_bg,
            fg=fg_color,
            font=FONT_MEDIUM,
            width=15,
            relief="flat",
            borderwidth=0,
            padx=8,
            pady=5,
            cursor="hand2"
        )
        self.hotkey_refresh_label.grid(row=0, column=1, sticky="w", pady=8, padx=(0, 5))
        
        capture_refresh_btn = ttk.Button(
            hotkey_frame,
            text="Set",
            command=self._capture_refresh_key,
            style="Small.TButton"
        )
        capture_refresh_btn.grid(row=0, column=2, pady=8)
        
        # Place Order Hotkey
        ttk.Label(hotkey_frame, text="Place Order:").grid(row=1, column=0, sticky="e", pady=8, padx=(0, 10))
        self.hotkey_place_order_label = tk.Label(
            hotkey_frame,
            text=self.config.get("hotkey_place_order", "F9"),
            bg=entry_bg,
            fg=fg_color,
            font=FONT_MEDIUM,
            width=15,
            relief="flat",
            borderwidth=0,
            padx=8,
            pady=5,
            cursor="hand2"
        )
        self.hotkey_place_order_label.grid(row=1, column=1, sticky="w", pady=8, padx=(0, 5))
        
        capture_place_order_btn = ttk.Button(
            hotkey_frame,
            text="Set",
            command=self._capture_place_order_key,
            style="Small.TButton"
        )
        capture_place_order_btn.grid(row=1, column=2, pady=8)
        
        # Bind key capture to labels
        self.hotkey_refresh_label.bind('<KeyPress>', self._on_hotkey_press)
        self.hotkey_place_order_label.bind('<KeyPress>', self._on_hotkey_press)
        self.hotkey_refresh_label.bind('<Button-1>', lambda e: self._capture_refresh_key())
        self.hotkey_place_order_label.bind('<Button-1>', lambda e: self._capture_place_order_key())
        
        ttk.Label(
            hotkey_frame,
            text="Click 'Set' or the display box, then press your desired key",
            font=FONT_SMALL,
            foreground="#6c6c6c"
        ).grid(row=2, column=0, columnspan=3, pady=(0, 8))
        
        # Info note
        ttk.Label(
            hotkey_frame,
            text="Hotkeys are saved automatically",
            font=FONT_SMALL,
            foreground="#A3BE8C"
        ).grid(row=3, column=0, columnspan=3, pady=(5, 0))
    
    def _reconnect_ib(self):
        """Save port and reconnect"""
        try:
            port = self.port_entry.get().strip()
            if not port.isdigit():
                self.toast.show("Error", "Port must be a number", "error")
                return
            
            # Save to config
            self.config["port"] = port
            self.save_config(self.config)
            
            # Reconnect
            if self.ib.connect(int(port)):
                self.toast.show("Success", f"Connected to port {port}", "success", 3000)
                self.update_connection_status()
            else:
                self.toast.show("Error", f"Failed to connect to port {port}", "error")
                self.update_connection_status()
        except Exception as e:
            self.toast.show("Error", str(e), "error")
    
    def update_connection_status(self):
        """Update the connection status display"""
        if self.ib.is_connected():
            self.connection_status_label.config(
                text="Connection Status: ✓ Connected",
                foreground="#A3BE8C"
            )
        else:
            self.connection_status_label.config(
                text="Connection Status: ✗ Disconnected",
                foreground="#BF616A"
            )
    
    def _capture_refresh_key(self):
        """Start capturing refresh hotkey"""
        self.capturing_refresh.set(True)
        self.capturing_place_order.set(False)
        self.hotkey_refresh_label.config(text="Press a key...", bg="#5E81AC", fg="white")
        self.hotkey_refresh_label.focus_set()
    
    def _capture_place_order_key(self):
        """Start capturing place order hotkey"""
        self.capturing_place_order.set(True)
        self.capturing_refresh.set(False)
        self.hotkey_place_order_label.config(text="Press a key...", bg="#5E81AC", fg="white")
        self.hotkey_place_order_label.focus_set()
    
    def _on_hotkey_press(self, event):
        """Capture key press for hotkey setting"""
        # Ignore modifier keys alone
        if event.keysym in ['Control_L', 'Control_R', 'Shift_L', 'Shift_R', 'Alt_L', 'Alt_R']:
            return
        
        # Build the key string
        key_parts = []
        
        # Check modifiers
        if event.state & 0x0004:  # Control
            key_parts.append("Control")
        if event.state & 0x0001:  # Shift
            key_parts.append("Shift")
        if event.state & 0x20000:  # Alt
            key_parts.append("Alt")
        
        key_parts.append(event.keysym)
        
        # Format the key string
        if len(key_parts) == 1:
            key_string = key_parts[0]
        else:
            key_string = f"<{'-'.join(key_parts)}>"
        
        # Update the appropriate label
        if self.capturing_refresh.get():
            self.hotkey_refresh_label.config(text=key_string, bg=entry_bg, fg=fg_color)
            self.config["hotkey_refresh"] = key_string
            self.save_config(self.config)
            self.capturing_refresh.set(False)
            # Notify main window to rebind hotkeys
            if hasattr(self, 'bind_hotkeys_callback'):
                self.bind_hotkeys_callback()
        elif self.capturing_place_order.get():
            self.hotkey_place_order_label.config(text=key_string, bg=entry_bg, fg=fg_color)
            self.config["hotkey_place_order"] = key_string
            self.save_config(self.config)
            self.capturing_place_order.set(False)
            # Notify main window to rebind hotkeys
            if hasattr(self, 'bind_hotkeys_callback'):
                self.bind_hotkeys_callback()
        
        # Block event from propagating
        return "break"
    
    def set_bind_hotkeys_callback(self, callback):
        """Set callback to rebind hotkeys when changed"""
        self.bind_hotkeys_callback = callback



