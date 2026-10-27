import tkinter as tk
from tkinter import messagebox
import json
import os

# --- Model ---
class DashboardModel:
    """Manages the application state and configuration data persistence."""
    def __init__(self):
        self.config_file = "dashboard_config.json"
        self.app_state = {"username": "Guest", "theme": "Light", "notifications": True}
        self.load_config()

    def load_config(self):
        """Loads dashboard configuration data from disk."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    self.app_state.update(json.load(f))
            except Exception:
                pass # Fallback to default state if file is corrupted

    def save_config(self):
        """Saves dashboard configuration data to disk."""
        with open(self.config_file, 'w') as f:
            json.dump(self.app_state, f)


# --- View & Controller (Combined for Tkinter MVC-lite) ---
class DashboardApp:
    """
    A multi-screen, frame-driven application managed via nested Frame widgets, 
    menu bars, and responsive pack/grid layout managers.
    """
    def __init__(self, root, model):
        self.root = root
        self.model = model
        self.root.title("Modular Multi-Frame Graphical Dashboard")
        self.root.geometry("500x400")
        
        # Setup Menu Bar
        self.create_menu()
        
        # Main container for nested frames
        self.main_container = tk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Dictionary to hold different screens (Frames)
        self.frames = {}
        
        # Initialize and store the modular frames
        for F in (HomeFrame, SettingsFrame):
            page_name = F.__name__
            frame = F(parent=self.main_container, controller=self)
            self.frames[page_name] = frame
            # Use grid for responsive stacking of frames in the same location
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        # Show initial frame
        self.show_frame("HomeFrame")

    def create_menu(self):
        """Builds the application menu bar."""
        menubar = tk.Menu(self.root)
        
        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Save Configuration", command=self.save_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Navigation Menu
        nav_menu = tk.Menu(menubar, tearoff=0)
        nav_menu.add_command(label="Home", command=lambda: self.show_frame("HomeFrame"))
        nav_menu.add_command(label="Settings", command=lambda: self.show_frame("SettingsFrame"))
        menubar.add_cascade(label="Navigate", menu=nav_menu)
        
        self.root.config(menu=menubar)

    def show_frame(self, page_name):
        """Brings the requested nested Frame widget to the front."""
        frame = self.frames[page_name]
        frame.update_view() # Update view with latest model data before showing
        frame.tkraise()

    def save_data(self):
        """Captures event to save data and displays warning/success dialogs."""
        try:
            self.model.save_config()
            messagebox.showinfo("Success", "Dashboard configuration saved to disk.")
        except Exception as e:
            messagebox.showwarning("Save Error", f"Could not save configuration: {e}")


class HomeFrame(tk.Frame):
    """The main dashboard screen displaying the current state."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        tk.Label(self, text="Welcome to the Dashboard", font=("Helvetica", 16, "bold")).pack(pady=20)
        
        self.info_label = tk.Label(self, text="", font=("Helvetica", 12))
        self.info_label.pack(pady=10)
        
        tk.Button(self, text="Go to Settings", 
                  command=lambda: controller.show_frame("SettingsFrame")).pack(pady=20)

    def update_view(self):
        """Updates the UI based on the current application state."""
        state = self.controller.model.app_state
        status = f"User: {state['username']}\nTheme: {state['theme']}\nAlerts: {'On' if state['notifications'] else 'Off'}"
        self.info_label.config(text=status)


class SettingsFrame(tk.Frame):
    """A configuration screen for capturing interactive user input events."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        tk.Label(self, text="Dashboard Settings", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=20)
        
        # Input for Username
        tk.Label(self, text="Username:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.user_var = tk.StringVar()
        tk.Entry(self, textvariable=self.user_var).grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        # Apply button to update the model state
        tk.Button(self, text="Update Username", command=self.apply_settings).grid(row=2, column=0, columnspan=2, pady=10)
        
        tk.Button(self, text="Back to Home", 
                  command=lambda: controller.show_frame("HomeFrame")).grid(row=3, column=0, columnspan=2, pady=20)

    def update_view(self):
        """Populates input fields with current model state."""
        self.user_var.set(self.controller.model.app_state["username"])

    def apply_settings(self):
        """Validates and updates the model state based on user input."""
        new_name = self.user_var.get().strip()
        if not new_name:
            messagebox.showwarning("Input Error", "Username cannot be empty.")
            return
            
        self.controller.model.app_state["username"] = new_name
        messagebox.showinfo("Settings Updated", "Username updated successfully. Remember to save via File menu.")


def main():
    """Main application entry point."""
    root = tk.Tk()
    model = DashboardModel()
    app = DashboardApp(root, model)
    root.mainloop()

if __name__ == "__main__":
    main()