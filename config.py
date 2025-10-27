"""
Configuration Management Module
Handles loading and saving of application settings
"""
import json
import os

CONFIG_FILE = "tws_panel_config.json"

def load_config():
    """Load saved configuration"""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return {
        "risk_percent": "1.0", 
        "port": "4001", 
        "hotkey_refresh": "F5", 
        "hotkey_place_order": "F9",
        "watchlist": ["AAPL", "TSLA", "NVDA", "MSFT", "GOOGL", "AMZN", "META", "SPY", "QQQ", "IWM"],
        "risk_buttons": [0.25, 0.5, 1.5]
    }

def save_config(config):
    """Save configuration to file"""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)
    except:
        pass

