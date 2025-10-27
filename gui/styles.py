"""
GUI Styles Module
Contains all styling configurations for the application
"""
from tkinter import ttk

# Fonts
FONT_LARGE = ("Segoe UI", 14)
FONT_TITLE = ("Segoe UI", 20, "bold")
FONT_MEDIUM = ("Segoe UI", 11)
FONT_SMALL = ("Segoe UI", 9)

# Colors
bg_color = "#2E3440"
fg_color = "#D8DEE9"
accent_color = "#88C0D0"
button_color = "#5E81AC"
entry_bg = "#3B4252"

def configure_styles(style):
    """Configure all ttk styles for the application"""
    
    # Base styles
    style.configure("TLabel", background=bg_color, foreground=fg_color, font=FONT_LARGE)
    style.configure("TButton", background=button_color, foreground="white", font=("Segoe UI", 14, "bold"))
    style.map("TButton", foreground=[('active', 'white')], background=[('active', '#81A1C1')])
    style.configure("Small.TButton", background=button_color, foreground="white", font=FONT_SMALL, padding=[5, 2])
    style.map("Small.TButton", foreground=[('active', 'white')], background=[('active', '#81A1C1')])
    style.configure("TEntry", fieldbackground=entry_bg, foreground=fg_color, font=FONT_LARGE)

    # Notebook (Tabs) Style
    style.configure("TNotebook", background=bg_color, borderwidth=0)
    style.configure("TNotebook.Tab", 
                    background=entry_bg, 
                    foreground=fg_color, 
                    padding=[20, 6],
                    font=("Segoe UI", 9, "bold"))
    style.map("TNotebook.Tab", 
              background=[('selected', button_color), ('!selected', entry_bg)], 
              foreground=[('selected', 'white'), ('!selected', fg_color)],
              padding=[('selected', [20, 6]), ('!selected', [20, 6])],
              font=[('selected', ("Segoe UI", 9, "bold")), ('!selected', ("Segoe UI", 9, "bold"))])

    # Frame styles
    style.configure("TFrame", background=entry_bg)
    style.configure("BG.TFrame", background=bg_color)
    style.configure("AccountInfo.TLabel", background=entry_bg, foreground=accent_color, font=("Segoe UI", 10))
    style.configure("TradeInfo.TLabel", background=entry_bg, foreground="#A3BE8C", font=("Segoe UI", 10, "bold"))
    style.configure("TotalInfo.TLabel", background=entry_bg, foreground="#EBCB8B", font=("Segoe UI", 10, "bold"))

    # Combobox Style
    style.configure("TCombobox",
                    fieldbackground=entry_bg,
                    background=entry_bg,
                    foreground=fg_color,
                    arrowcolor=accent_color,
                    bordercolor=entry_bg,
                    lightcolor=entry_bg,
                    darkcolor=entry_bg,
                    borderwidth=1,
                    relief='flat')
    style.map("TCombobox",
              fieldbackground=[('readonly', entry_bg), ('disabled', entry_bg)],
              foreground=[('readonly', fg_color), ('disabled', '#4C566A')],
              arrowcolor=[('disabled', '#4C566A'), ('!disabled', accent_color)],
              selectbackground=[('readonly', accent_color)],
              selectforeground=[('readonly', bg_color)])

    # Checkbox Style
    style.configure("TCheckbutton", 
                    background=bg_color, 
                    foreground=fg_color, 
                    font=("Segoe UI", 12),
                    borderwidth=0,
                    relief='flat',
                    focuscolor='none',
                    highlightthickness=0)
    style.map("TCheckbutton",
              background=[('active', bg_color), ('!active', bg_color), ('selected', bg_color), ('!selected', bg_color)],
              foreground=[('active', accent_color), ('selected', accent_color), ('!selected', fg_color)],
              indicatorcolor=[('selected', accent_color), ('!selected', '#4C566A')],
              indicatorrelief=[('pressed', 'flat'), ('!pressed', 'flat')])

    # Radiobutton Style  
    style.configure("TRadiobutton",
                    background=bg_color,
                    foreground=fg_color,
                    font=FONT_LARGE,
                    borderwidth=0,
                    relief='flat',
                    focuscolor='none',
                    highlightthickness=0)
    style.map("TRadiobutton",
              background=[('active', bg_color), ('!active', bg_color), ('selected', bg_color), ('!selected', bg_color)],
              foreground=[('active', accent_color), ('selected', accent_color), ('!selected', fg_color)],
              indicatorcolor=[('selected', accent_color), ('!selected', '#4C566A')])

def configure_combobox_options(root):
    """Configure combobox dropdown styling"""
    root.option_add('*TCombobox*Listbox.background', entry_bg)
    root.option_add('*TCombobox*Listbox.foreground', fg_color)
    root.option_add('*TCombobox*Listbox.selectBackground', accent_color)
    root.option_add('*TCombobox*Listbox.selectForeground', bg_color)
    root.option_add('*TCombobox*Listbox.font', FONT_LARGE)



