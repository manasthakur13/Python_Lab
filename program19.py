import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
import os
# Pillow (PIL) is required for robust image handling in Tkinter
from PIL import Image, ImageTk 

class DynamicViewerApp:
    """
    A desktop GUI tool that allows users to interactively locate, open, 
    and view image files or text contents on screen using native modal dialogs.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Dynamic Interactive Image/File Viewer")
        self.root.geometry("600x500")
        
        # Default application state
        self.current_image = None
        self.bg_color = "#f0f0f0"
        self.root.configure(bg=self.bg_color)

        self.create_widgets()
        self.bind_events()

    def create_widgets(self):
        """Sets up the interface including Canvas components and Label properties."""
        # Top instructional label
        self.info_label = tk.Label(
            self.root, 
            text="Press <Return> to open a file. Click the canvas to change background color.",
            bg=self.bg_color,
            font=("Arial", 10, "italic")
        )
        self.info_label.pack(pady=10)

        # Dynamic Label for displaying text file contents or status
        self.text_display = tk.Label(
            self.root, 
            text="No file loaded.",
            bg=self.bg_color,
            wraplength=550,
            justify="left",
            font=("Arial", 12)
        )
        self.text_display.pack(pady=5)

        # Canvas component for displaying images
        self.canvas = tk.Canvas(self.root, width=500, height=350, bg="white", relief="sunken", bd=2)
        self.canvas.pack(pady=10)
        self.canvas_text = self.canvas.create_text(250, 175, text="Image Preview Area", fill="gray")

    def bind_events(self):
        """Binds mouse clicks and keypress events to update application layouts."""
        # Bind the Enter/Return key to trigger the file opening dialog
        self.root.bind("<Return>", self.prompt_open_file)
        
        # Bind left mouse click on the canvas to trigger the color chooser
        self.canvas.bind("<Button-1>", self.prompt_change_color)

    def prompt_open_file(self, event=None):
        """
        Leverages native modal dialogs (filedialog.askopenfilename) to 
        locate and load either a text file or an image file.
        """
        filepath = filedialog.askopenfilename(
            title="Select a File to View",
            filetypes=[
                ("All Supported Files", "*.txt;*.png;*.jpg;*.jpeg;*.gif"),
                ("Text Files", "*.txt"),
                ("Image Files", "*.png;*.jpg;*.jpeg;*.gif"),
                ("All Files", "*.*")
            ]
        )

        if not filepath:
            return # User cancelled the dialog

        ext = os.path.splitext(filepath)[1].lower()

        try:
            if ext == '.txt':
                self.load_text(filepath)
            elif ext in ['.png', '.jpg', '.jpeg', '.gif']:
                self.load_image(filepath)
            else:
                messagebox.showwarning("Unsupported Format", "Please select a text or image file.")
        except Exception as e:
            # Leverage messagebox for error reporting
            messagebox.showerror("Error", f"Failed to open file: {e}")

    def load_text(self, filepath):
        """Reads text contents and updates Label properties dynamically."""
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read(500) # Read up to 500 characters for preview
            if len(content) == 500:
                content += "...\n[Content Truncated]"
                
        # Update components dynamically
        self.text_display.config(text=content)
        self.canvas.delete("all")
        self.canvas_text = self.canvas.create_text(250, 175, text="Viewing Text Document", fill="gray")
        self.current_image = None

    def load_image(self, filepath):
        """Opens an image, resizes it to fit, and updates the canvas component."""
        img = Image.open(filepath)
        img.thumbnail((500, 350)) # Resize maintaining aspect ratio
        self.current_image = ImageTk.PhotoImage(img)
        
        # Update components dynamically
        self.text_display.config(text=f"Viewing Image: {os.path.basename(filepath)}")
        self.canvas.delete("all")
        
        # Center the image on the canvas
        x_center = (500 - self.current_image.width()) // 2
        y_center = (350 - self.current_image.height()) // 2
        self.canvas.create_image(x_center, y_center, anchor=tk.NW, image=self.current_image)

    def prompt_change_color(self, event=None):
        """
        Leverages colorchooser.askcolor to change application colors interactively
        via mouse click bindings on the canvas.
        """
        color_code = colorchooser.askcolor(title="Choose Canvas Background Color")[1]
        
        if color_code:
            # Dynamically update the canvas and root background properties
            self.canvas.config(bg=color_code)
            self.bg_color = color_code
            self.root.configure(bg=self.bg_color)
            self.info_label.config(bg=self.bg_color)
            self.text_display.config(bg=self.bg_color)

def main():
    """Main execution function to initialize and run the GUI application."""
    root = tk.Tk()
    app = DynamicViewerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()