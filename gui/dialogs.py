"""
Dialogs Module
Contains dialog windows for editing watchlist and risk buttons
"""
import tkinter as tk
from tkinter import ttk
from gui.styles import *

def edit_watchlist_dialog(root, config, save_config, watchlist_buttons, switch_ticker_func, toast):
    """Open modern dialog to edit watchlist"""
    current_watchlist = config.get("watchlist", ["AAPL", "TSLA", "NVDA", "MSFT", "GOOGL", "AMZN", "META", "SPY", "QQQ", "IWM"])
    
    # Create modern dialog window
    dialog = tk.Toplevel(root)
    dialog.title("Edit Watchlist")
    dialog.configure(bg=bg_color)
    dialog.resizable(False, False)
    
    # Set size and center the dialog on screen
    window_width = 450
    window_height = 400
    screen_width = dialog.winfo_screenwidth()
    screen_height = dialog.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    dialog.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    dialog.transient(root)
    dialog.grab_set()
    
    # Title
    title_label = tk.Label(
        dialog,
        text="Edit Watchlist",
        font=("Segoe UI", 16, "bold"),
        fg=accent_color,
        bg=bg_color
    )
    title_label.pack(pady=(20, 10))
    
    # Subtitle
    subtitle_label = tk.Label(
        dialog,
        text="Enter up to 10 ticker symbols",
        font=("Segoe UI", 9),
        fg="#D8DEE9",
        bg=bg_color
    )
    subtitle_label.pack(pady=(0, 20))
    
    # Input frame with grid for 10 entries (centered)
    input_frame = tk.Frame(dialog, bg=bg_color)
    input_frame.pack(pady=10, expand=True)
    
    # Configure grid to center content
    input_frame.grid_columnconfigure(0, weight=1)
    input_frame.grid_columnconfigure(1, weight=1)
    
    entries = []
    for i in range(10):
        row = i % 5
        col = i // 5
        
        entry = ttk.Entry(input_frame, font=FONT_MEDIUM, width=12, justify='center')
        entry.grid(row=row, column=col, padx=8, pady=6)
        entry.insert(0, current_watchlist[i] if i < len(current_watchlist) else "")
        entries.append(entry)
    
    # Button frame
    button_frame = tk.Frame(dialog, bg=bg_color)
    button_frame.pack(pady=(10, 20))
    
    def save_watchlist():
        """Save the watchlist and update UI"""
        new_watchlist = []
        for entry in entries:
            ticker = entry.get().strip().upper()
            new_watchlist.append(ticker)
        
        # Update config
        config["watchlist"] = new_watchlist
        save_config(config)
        
        # Update button labels
        for i, (btn, old_ticker) in enumerate(watchlist_buttons):
            new_ticker = new_watchlist[i]
            btn.config(
                text=new_ticker if new_ticker else f"W{i+1}",
                fg="white" if new_ticker else "#4C566A",
                bg=button_color if new_ticker else "#3B4252",
                cursor='hand2' if new_ticker else 'arrow',
                command=lambda t=new_ticker: switch_ticker_func(t) if t else None
            )
            watchlist_buttons[i] = (btn, new_ticker)
        
        toast.show("Success", "Watchlist updated successfully", "success")
        dialog.destroy()
    
    def cancel_edit():
        """Close dialog without saving"""
        dialog.destroy()
    
    # Save button (modern style)
    save_btn = tk.Button(
        button_frame,
        text="Save",
        font=FONT_MEDIUM + ("bold",),
        fg="white",
        bg="#A3BE8C",  # Green
        activebackground="#8FBCBB",
        activeforeground="white",
        bd=0,
        relief='flat',
        cursor='hand2',
        command=save_watchlist,
        padx=30,
        pady=10,
        width=10
    )
    save_btn.pack(side='left', padx=5)
    
    # Cancel button (modern style)
    cancel_btn = tk.Button(
        button_frame,
        text="Cancel",
        font=FONT_MEDIUM,
        fg=fg_color,
        bg="#4C566A",
        activebackground="#5E81AC",
        activeforeground="white",
        bd=0,
        relief='flat',
        cursor='hand2',
        command=cancel_edit,
        padx=30,
        pady=10,
        width=10
    )
    cancel_btn.pack(side='left', padx=5)
    
    # Focus first entry
    entries[0].focus_set()
    
    # Bind Enter key to save
    dialog.bind('<Return>', lambda e: save_watchlist())
    dialog.bind('<Escape>', lambda e: cancel_edit())

def edit_risk_buttons_dialog(root, config, save_config, risk_buttons, set_risk_func, toast):
    """Open dialog to edit risk percentage buttons"""
    current_percentages = config.get("risk_buttons", [0.25, 0.5, 1.5])
    
    # Create modern dialog window
    dialog = tk.Toplevel(root)
    dialog.title("Edit Risk Buttons")
    dialog.configure(bg=bg_color)
    dialog.resizable(False, False)
    
    # Set size and center the dialog on screen
    window_width = 350
    window_height = 300
    screen_width = dialog.winfo_screenwidth()
    screen_height = dialog.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    dialog.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    dialog.transient(root)
    dialog.grab_set()
    
    # Title
    title_label = tk.Label(
        dialog,
        text="Edit Risk Buttons",
        font=("Segoe UI", 16, "bold"),
        fg=accent_color,
        bg=bg_color
    )
    title_label.pack(pady=(20, 10))
    
    # Subtitle
    subtitle_label = tk.Label(
        dialog,
        text="Enter 3 risk percentages",
        font=("Segoe UI", 9),
        fg="#D8DEE9",
        bg=bg_color
    )
    subtitle_label.pack(pady=(0, 20))
    
    # Input frame
    input_frame = tk.Frame(dialog, bg=bg_color)
    input_frame.pack(pady=10, expand=True)
    
    entries = []
    for i in range(3):
        label = tk.Label(
            input_frame,
            text=f"Button {i+1}:",
            font=("Segoe UI", 10),
            fg=fg_color,
            bg=bg_color
        )
        label.grid(row=i, column=0, padx=(0, 10), pady=8, sticky='e')
        
        entry = ttk.Entry(input_frame, font=FONT_MEDIUM, width=10, justify='center')
        entry.grid(row=i, column=1, pady=8)
        entry.insert(0, f"{current_percentages[i]:.2f}" if i < len(current_percentages) else "1.0")
        entries.append(entry)
        
        percent_label = tk.Label(
            input_frame,
            text="%",
            font=("Segoe UI", 10),
            fg=fg_color,
            bg=bg_color
        )
        percent_label.grid(row=i, column=2, padx=(5, 0), pady=8, sticky='w')
    
    # Button frame
    button_frame = tk.Frame(dialog, bg=bg_color)
    button_frame.pack(pady=(10, 20))
    
    def save_percentages():
        """Save the percentages and update buttons"""
        try:
            new_percentages = []
            for entry in entries:
                value = float(entry.get().strip())
                if value <= 0:
                    toast.show("Error", "Percentages must be positive numbers", "error")
                    return
                new_percentages.append(value)
            
            # Update config
            config["risk_buttons"] = new_percentages
            save_config(config)
            
            # Update button labels and commands
            for i, btn in enumerate(risk_buttons):
                if i < len(new_percentages):
                    percent = new_percentages[i]
                    btn.config(
                        text=f"{percent:.2f}%",
                        command=lambda p=percent: set_risk_func(p)
                    )
            
            toast.show("Success", "Risk buttons updated successfully", "success")
            dialog.destroy()
        except ValueError:
            toast.show("Error", "Please enter valid numbers", "error")
    
    def cancel_edit():
        """Close dialog without saving"""
        dialog.destroy()
    
    # Save button
    save_btn = tk.Button(
        button_frame,
        text="Save",
        font=FONT_MEDIUM + ("bold",),
        fg="white",
        bg="#A3BE8C",
        activebackground="#8FBCBB",
        activeforeground="white",
        bd=0,
        relief='flat',
        cursor='hand2',
        command=save_percentages,
        padx=30,
        pady=10,
        width=10
    )
    save_btn.pack(side='left', padx=5)
    
    # Cancel button
    cancel_btn = tk.Button(
        button_frame,
        text="Cancel",
        font=FONT_MEDIUM,
        fg=fg_color,
        bg="#4C566A",
        activebackground="#5E81AC",
        activeforeground="white",
        bd=0,
        relief='flat',
        cursor='hand2',
        command=cancel_edit,
        padx=30,
        pady=10,
        width=10
    )
    cancel_btn.pack(side='left', padx=5)
    
    # Focus first entry
    entries[0].focus_set()
    
    # Bind Enter key to save
    dialog.bind('<Return>', lambda e: save_percentages())
    dialog.bind('<Escape>', lambda e: cancel_edit())



