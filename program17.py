import tkinter as tk

class DesktopCalculator:
    """
    A fully interactive desktop calculator built using tkinter.
    It processes mathematical operations and updates results dynamically
    inside a unified Entry display field using the grid geometry manager.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Functional Graphical Desktop Calculator")
        self.root.geometry("300x400")
        self.root.resizable(False, False)

        # Unified Entry display field for dynamic updates
        self.display_var = tk.StringVar()
        self.display = tk.Entry(
            root, textvariable=self.display_var, font=("Arial", 20),
            bg="#eee", bd=10, justify="right"
        )
        self.display.grid(row=0, column=0, columnspan=4, ipadx=8, ipady=20, pady=10)

        # Wire the graphical Button widgets to internal processing engines
        self.create_buttons()

    def create_buttons(self):
        """Organizes and wires graphical Button widgets via the grid geometry manager."""
        button_layout = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('C', 4, 0), ('0', 4, 1), ('=', 4, 2), ('+', 4, 3)
        ]

        for (text, row, col) in button_layout:
            button = tk.Button(
                self.root, text=text, font=("Arial", 16, "bold"),
                command=lambda t=text: self.on_button_click(t)
            )
            button.grid(row=row, column=col, sticky="nsew", padx=5, pady=5, ipadx=10, ipady=10)

        # Configure row and column weights so buttons expand evenly
        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)
        for i in range(1, 5):
            self.root.grid_rowconfigure(i, weight=1)

    def on_button_click(self, char):
        """
        Internal mathematical processing engine that captures user mouse clicks 
        and updates the dynamic Entry display field.
        """
        if char == 'C':
            # Clear the display field
            self.display_var.set("")
        elif char == '=':
            try:
                # Evaluate the mathematical expression safely
                current_expression = self.display_var.get()
                result = str(eval(current_expression))
                self.display_var.set(result)
            except ZeroDivisionError:
                self.display_var.set("Error: Div by 0")
            except Exception:
                self.display_var.set("Error")
        else:
            # Append the clicked button character to the current expression
            current_text = self.display_var.get()
            
            # Reset display if it currently shows an error message
            if "Error" in current_text:
                current_text = ""
                
            self.display_var.set(current_text + char)

def main():
    """Main execution function to launch the tkinter GUI."""
    root = tk.Tk()
    app = DesktopCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()