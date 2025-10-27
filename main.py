"""
IB Order Panel - Main Entry Point
Modular version of the Interactive Brokers trading panel application
"""
from config import load_config, save_config
from toast import ToastNotification
from ib_connector import IBConnector
from gui.main_window import MainWindow

def main():
    """Main entry point for the application"""
    # Load configuration
    config = load_config()
    
    # Create IB connector
    ib_connector = IBConnector()
    
    # Initial connection
    port = int(config.get("port", "4001"))
    ib_connector.connect(port)
    
    # Create main window
    main_window = MainWindow(config, save_config, ib_connector, None)
    
    # Create toast notification system
    toast = ToastNotification(main_window.root)
    
    # Update references
    main_window.toast = toast
    ib_connector.toast = toast
    main_window.trading_tab.toast = toast
    main_window.settings_tab.toast = toast
    
    # Run the application
    try:
        main_window.run()
    finally:
        # Cleanup
        ib_connector.disconnect()

if __name__ == "__main__":
    main()

