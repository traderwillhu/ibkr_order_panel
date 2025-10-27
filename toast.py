"""
Modern Toast Notification System
Non-blocking toast notifications for the application
"""
import tkinter as tk

class ToastNotification:
    """Modern, non-blocking toast notification"""
    def __init__(self, master):
        self.master = master
        self.notifications = []
        
    def show(self, title, message, msg_type="info", duration=3000):
        """
        Show a toast notification
        msg_type: 'info', 'success', 'warning', 'error'
        duration: milliseconds to display (0 = permanent)
        """
        # Create notification frame
        toast = tk.Frame(self.master, bg="#2E3440", relief="flat", borderwidth=0)
        toast.config(highlightthickness=1)
        
        # Set color based on type
        colors = {
            "info": ("#5E81AC", "#D8DEE9"),
            "success": ("#A3BE8C", "#2E3440"),
            "warning": ("#EBCB8B", "#2E3440"),
            "error": ("#BF616A", "#ECEFF4")
        }
        bg_color, fg_color = colors.get(msg_type, colors["info"])
        toast.config(bg=bg_color, highlightbackground=bg_color)
        
        # Icon based on type
        icons = {
            "info": "ℹ",
            "success": "✓",
            "warning": "⚠",
            "error": "✕"
        }
        icon = icons.get(msg_type, "ℹ")
        
        # Icon label
        icon_label = tk.Label(
            toast,
            text=icon,
            font=("Segoe UI", 16, "bold"),
            bg=bg_color,
            fg=fg_color
        )
        icon_label.pack(side="left", padx=(10, 5), pady=10)
        
        # Message frame
        msg_frame = tk.Frame(toast, bg=bg_color)
        msg_frame.pack(side="left", fill="both", expand=True, padx=(5, 10), pady=10)
        
        # Title
        if title:
            title_label = tk.Label(
                msg_frame,
                text=title,
                font=("Segoe UI", 10, "bold"),
                bg=bg_color,
                fg=fg_color,
                anchor="w"
            )
            title_label.pack(fill="x")
        
        # Message
        msg_label = tk.Label(
            msg_frame,
            text=message,
            font=("Segoe UI", 9),
            bg=bg_color,
            fg=fg_color,
            anchor="w",
            wraplength=300
        )
        msg_label.pack(fill="x")
        
        # Close button
        close_btn = tk.Label(
            toast,
            text="×",
            font=("Segoe UI", 16, "bold"),
            bg=bg_color,
            fg=fg_color,
            cursor="hand2"
        )
        close_btn.pack(side="right", padx=10)
        close_btn.bind("<Button-1>", lambda e: self.close_notification(toast))
        
        # Position notification
        self.notifications.append(toast)
        self.reposition_notifications()
        
        # Auto-close after duration
        if duration > 0:
            self.master.after(duration, lambda: self.close_notification(toast))
        
        # Fade in animation
        toast.lift()
        
    def close_notification(self, toast):
        """Close a notification"""
        if toast in self.notifications:
            self.notifications.remove(toast)
            toast.destroy()
            self.reposition_notifications()
    
    def reposition_notifications(self):
        """Reposition all notifications"""
        y_offset = 10
        for toast in self.notifications:
            toast.place(relx=1.0, x=-10, y=y_offset, anchor="ne")
            y_offset += toast.winfo_reqheight() + 10


