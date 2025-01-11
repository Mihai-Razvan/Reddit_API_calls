import tkinter as tk
from user import main_user_osint
from subreddit import main_subreddit_osint


def setup_choice_gui():
    """Create a simple interface to choose between User OSINT and Subreddit OSINT."""
    root = tk.Tk()
    root.title("Choose OSINT Type")
    root.geometry("300x300")

    def check_for_quit(event=None):
        """Allow quitting by pressing 'q', 'Q', or 'ESC'."""
        root.destroy()

    # Rebind the 'q', 'Q', and ESC keys to close the app each time we show the main menu
    root.bind("q", check_for_quit)  # 'q' key to quit
    root.bind("Q", check_for_quit)  # 'Q' key to quit
    root.bind("<Escape>", check_for_quit)  # ESC key to quit

    tk.Label(root, text="Select an option:", font=("Helvetica", 14)).pack(pady=20)

    user_button_widget = tk.Button(root, text="User OSINT", font=("Helvetica", 12), width=15,
                                   command=lambda: launch_osint(root, main_user_osint))
    user_button_widget.pack(pady=10)

    subreddit_button_widget = tk.Button(root, text="Subreddit OSINT", font=("Helvetica", 12), width=15,
                                       command=lambda: launch_osint(root, main_subreddit_osint))
    subreddit_button_widget.pack(pady=10)

    # Add the label with the instructions to close the app
    close_label = tk.Label(root, text="Press q/Q or ESC to close", font=("Helvetica", 10))
    close_label.pack(pady=20)

    root.mainloop()


def launch_osint(root, osint_function):
    """Close the choice window and launch the selected OSINT function."""
    root.destroy()  # Close the selection window
    osint_function()  # Launch the selected OSINT interface
    setup_choice_gui()  # After OSINT function finishes, return to the choice window


if __name__ == "__main__":
    setup_choice_gui()
