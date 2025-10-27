# IB Order Panel

A professional trading panel application for Interactive Brokers (IB) with a modern GUI interface.

## ⚠️ Disclaimer

**This software is for educational and informational purposes only. Trading stocks, options, and other financial instruments involves substantial risk of loss and is not suitable for every investor. The use of this software does not guarantee profits and you may lose money. Past performance is not indicative of future results.**

**By using this software, you acknowledge that:**
- You are solely responsible for your trading decisions
- The authors and contributors are not liable for any financial losses
- You should thoroughly test any automated trading software in a paper trading account first
- You understand the risks involved in trading financial markets

**USE AT YOUR OWN RISK.**

## Features

- 🔌 **IB Gateway/TWS Integration** - Connect to Interactive Brokers via API
- 📊 **Real-time Account Data** - Monitor buying power, P&L, and positions
- 📈 **Customizable Watchlist** - Track your favorite symbols
- ⚡ **Keyboard Shortcuts** - Fast order entry with hotkeys
- 🎯 **Risk Management** - Position sizing based on risk percentage
- 🎨 **Modern UI** - Clean, intuitive interface built with tkinter
- 💾 **Configuration Persistence** - Save your settings and preferences
- 🔔 **Toast Notifications** - Non-blocking status updates

## File Structure

```
tws order/
├── main.py                 # Main entry point
├── config.py              # Configuration management module
├── toast.py               # Toast notification system module
├── ib_connector.py        # IB connection and trading logic module
├── gui/                   # GUI package
│   ├── __init__.py       # Package initialization file
│   ├── styles.py         # Style configuration module
│   ├── main_window.py    # Main window module
│   ├── trading_tab.py    # Trading interface module
│   ├── settings_tab.py   # Settings interface module
│   └── dialogs.py        # Dialogs module
└── tws_panel_config.json # Configuration file
```

## Module Description

### Core Modules

- **main.py** - Application entry point
  - Initialize configuration
  - Create IB connector
  - Create main window
  - Start application

- **config.py** - Configuration management
  - `load_config()` - Load configuration
  - `save_config()` - Save configuration
  - Manage port, hotkeys, watchlist, risk buttons and other settings

- **toast.py** - Toast notification system
  - `ToastNotification` class
  - Non-blocking notification display
  - Supports four types: info, success, warning, error

- **ib_connector.py** - IB connector
  - `IBConnector` class
  - Manage connection to Interactive Brokers
  - Handle all trading-related logic
  - Get account information, market data, place orders, etc.

### GUI Modules

- **gui/styles.py** - Style configuration
  - Define all color and font constants
  - `configure_styles()` - Configure all ttk styles
  - `configure_combobox_options()` - Configure combobox styles

- **gui/main_window.py** - Main window
  - `MainWindow` class
  - Create main window and tabs
  - Manage clock display and always-on-top functionality
  - Bind hotkeys

- **gui/trading_tab.py** - Trading interface
  - `TradingTab` class
  - Account information display
  - Watchlist
  - Order entry and submission
  - Automatic position size calculation

- **gui/settings_tab.py** - Settings interface
  - `SettingsTab` class
  - Connection settings
  - Hotkey configuration
  - Connection status check

- **gui/dialogs.py** - Dialogs
  - `edit_watchlist_dialog()` - Edit watchlist dialog
  - `edit_risk_buttons_dialog()` - Edit risk buttons dialog

## Prerequisites

- Python 3.7 or higher
- Interactive Brokers account (paper or live)
- TWS (Trader Workstation) or IB Gateway installed and running

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ib-order-panel.git
cd ib-order-panel
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure the application**
```bash
# Copy the example configuration file
cp tws_panel_config.example.json tws_panel_config.json

# Edit the configuration file with your preferences
# The default port is 7496 (paper trading)
# Use 7497 for live trading
```

4. **Enable API in TWS/IB Gateway**
   - Open TWS or IB Gateway
   - Go to File → Global Configuration → API → Settings
   - Enable "Enable ActiveX and Socket Clients"
   - Note the Socket port (default: 7496 for paper, 7497 for live)

## Usage

### Starting the Application

```bash
python main.py
```

### Configuration

The configuration file `tws_panel_config.json` contains:
- **port** - IB Gateway/TWS connection port (7496 for paper, 7497 for live)
- **risk_percent** - Default risk percentage for position sizing
- **hotkey_refresh** - Hotkey to refresh account data
- **hotkey_place_order** - Hotkey to place orders
- **watchlist** - List of symbols to monitor

### Default Hotkeys

- **Enter** - Refresh account data
- **F1** - Place order

You can customize these in the Settings tab.

## Development Guidelines

### Adding New Features
- Add new trading logic to `ib_connector.py`
- Add new UI components to the appropriate file under `gui/`
- Update configuration handling in `config.py`

### Modifying UI
- Edit the corresponding files under `gui/` directory
- Update styles uniformly in `gui/styles.py`

### Code Structure
- Keep modules focused on single responsibilities
- Use the existing toast notification system for user feedback
- Follow the established naming conventions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [ib_insync](https://github.com/erdewit/ib_insync) library
- Interactive Brokers API documentation

## Support

For issues, questions, or contributions, please open an issue on GitHub.

---

**Remember:** Always test with paper trading first before using with real money!
