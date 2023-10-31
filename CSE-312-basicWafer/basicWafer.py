import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Checkbox Example")

# Create a BooleanVar to control the checkbox state
checkbox_state = tk.BooleanVar(value=True)

# Create a Checkbutton with the BooleanVar
checkbox = tk.Checkbutton(root, text="Check Me", variable=checkbox_state)
checkbox.pack()

# Start the tkinter main loop
root.mainloop()