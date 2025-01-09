import tkinter as tk
from user import main_user_osint
from subreddit import main_subreddit_osint


def setup_choice_gui():
    """Create a simple interface to choose between User OSINT and Subreddit OSINT."""
    root = tk.Tk()
    root.title("Choose OSINT Type")
    root.geometry("300x300")

    tk.Label(root, text="Select an option:", font=("Helvetica", 14)).pack(pady=20)

    user_button_widget = tk.Button(root, text="User OSINT", font=("Helvetica", 12), width=15,
                            command=lambda: launch_osint(root, main_user_osint))
    user_button_widget.pack(pady=10)

    subreddit_button_widget = tk.Button(root, text="Subreddit OSINT", font=("Helvetica", 12), width=15,
                                 command=lambda: launch_osint(root, main_subreddit_osint))
    subreddit_button_widget.pack(pady=10)

    root.mainloop()


def launch_osint(root, osint_function):
    """Close the choice window and launch the selected OSINT function."""
    root.destroy()  # Close the selection window
    osint_function()  # Launch the selected OSINT interface


if __name__ == "__main__":
    setup_choice_gui()