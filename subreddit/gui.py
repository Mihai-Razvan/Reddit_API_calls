import tkinter as tk
from tkinter import messagebox, ttk

from utils import reddit, make_links_clickable, open_json_window

from .formatters import format_subreddit_info, format_subreddit_post
from .api_fetch import fetch_subreddit_info, fetch_subreddit_posts_batch

subreddit_posts_generator = None

def get_subreddit_info(subreddit_entry, subreddit_info_text_widget, show_subreddit_info_json_button, canvas_posts, canvas_frame_posts, subreddit_posts, subreddit_posts_full_json):
    """Fetch subreddit data and update the GUI with selected fields."""
    subreddit_name = subreddit_entry.get().strip()
    if not subreddit_name:
        messagebox.showerror("Error", "Subreddit field is empty!")
        return

    try:
        # Fetch and display subreddit info
        subreddit_info, subreddit_info_full_json = fetch_subreddit_info(subreddit_name)
        subreddit_data_str = format_subreddit_info(subreddit_info)
        subreddit_info_text_widget.config(state="normal")
        subreddit_info_text_widget.delete(1.0, tk.END)
        subreddit_info_text_widget.insert(tk.END, subreddit_data_str)
        subreddit_info_text_widget.config(state="disabled")

        make_links_clickable(subreddit_info_text_widget, subreddit_data_str)
        show_subreddit_info_json_button.config(state="normal", command=lambda: open_json_window(subreddit_info_full_json))

        # Automatically load the first batch of posts
        subreddit_posts.clear()
        subreddit_posts_full_json.clear()
        get_subreddit_posts(subreddit_entry, canvas_posts, canvas_frame_posts, subreddit_posts, subreddit_posts_full_json)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch data: {e}")


def get_subreddit_posts(subreddit_entry, canvas, canvas_frame, subreddit_posts, subreddit_posts_full_json):
    global subreddit_posts_generator
    """Fetch and display posts for a given subreddit."""
    subreddit_name = subreddit_entry.get().strip()
    if not subreddit_name:
        messagebox.showerror("Error", "Subreddit field is empty!")
        return

    try:
        if len(subreddit_posts) == 0:  # Fetch posts initially
            subreddit_posts_generator = reddit.subreddit(subreddit_name).new(limit=None)
            next_subreddit_posts, next_subreddit_posts_full_json = fetch_subreddit_posts_batch(subreddit_posts_generator)
            subreddit_posts.extend(next_subreddit_posts)
            subreddit_posts_full_json.extend(next_subreddit_posts_full_json)
        else:  # Load more posts when button is clicked
            next_subreddit_posts, next_subreddit_posts_full_json = fetch_subreddit_posts_batch(subreddit_posts_generator, batch_size=5)
            subreddit_posts.extend(next_subreddit_posts)
            subreddit_posts_full_json.extend(next_subreddit_posts_full_json)

        display_subreddit_posts(subreddit_posts, subreddit_posts_full_json, canvas, canvas_frame)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch posts: {e}")


def display_subreddit_posts(posts, full_posts_json, canvas, canvas_frame):
    """Display the list of posts and their details in the canvas."""
    for widget in canvas_frame.winfo_children():
        widget.destroy()

    for post, full_post_json in zip(posts, full_posts_json):
        post_data = format_subreddit_post(post)
        post_frame = tk.Frame(canvas_frame)
        post_frame.pack(fill="x", padx=10, pady=5)

        post_label_widget = tk.Label(post_frame, text=post_data, justify="left", anchor="w")
        post_label_widget.pack(side="left", fill="x", expand=True)

        show_post_json_button = tk.Button(post_frame, text="View JSON", command=lambda p=full_post_json: open_json_window(p))
        show_post_json_button.pack(side="right", padx=5)

    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))


def setup_gui():
    root = tk.Tk()
    root.title("Reddit Subreddit Data Extractor")
    root.geometry("800x800")

    def check_for_quit(event=None):
        """Allow quitting by pressing 'q', 'Q', or 'ESC'."""
        root.destroy()

    # Rebind the 'q', 'Q', and ESC keys to close the app each time we show the main menu
    root.bind("q", check_for_quit)  # 'q' key to quit
    root.bind("Q", check_for_quit)  # 'Q' key to quit
    root.bind("<Escape>", check_for_quit)  # ESC key to quit

    notebook = ttk.Notebook(root)

    selected_tab = ttk.Frame(notebook)
    posts_tab = ttk.Frame(notebook)

    notebook.add(selected_tab, text="General Info")
    notebook.add(posts_tab, text="Posts")
    notebook.pack(expand=True, fill="both")

    # Subreddit Info Tab
    tk.Label(selected_tab, text="Enter Subreddit Name:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    subreddit_entry = tk.Entry(selected_tab, width=30)
    subreddit_entry.grid(row=0, column=1, padx=10, pady=10)

    subreddit_info_text_widget = tk.Text(selected_tab, width=100, height=40, state="disabled")
    subreddit_info_text_widget.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

    show_subreddit_info_json_button = tk.Button(selected_tab, text="View Full JSON", state="disabled")
    show_subreddit_info_json_button.grid(row=2, column=1, pady=10)

    subreddit_posts = []
    subreddit_posts_full_json = []

    fetch_button = tk.Button(
        selected_tab,
        text="Search",
        command=lambda: get_subreddit_info(
            subreddit_entry,
            subreddit_info_text_widget,
            show_subreddit_info_json_button,
            canvas_posts,
            canvas_frame_posts,
            subreddit_posts,
            subreddit_posts_full_json,
        )
    )
    fetch_button.grid(row=0, column=2, padx=10, pady=10)

    # Subreddit Posts Tab
    posts_canvas_frame = ttk.Frame(posts_tab)
    posts_canvas_frame.pack(padx=10, pady=10, fill="both", expand=True)
    canvas_posts = tk.Canvas(posts_canvas_frame)
    canvas_posts.pack(side="left", fill="both", expand=True)
    scrollbar_posts = tk.Scrollbar(posts_canvas_frame, orient="vertical", command=canvas_posts.yview)
    scrollbar_posts.pack(side="right", fill="y")
    canvas_posts.config(yscrollcommand=scrollbar_posts.set)
    canvas_frame_posts = ttk.Frame(canvas_posts)
    canvas_posts.create_window((0, 0), window=canvas_frame_posts, anchor="nw")

    load_more_posts_button = tk.Button(
        posts_tab,
        text="Load More Posts",
        command=lambda: get_subreddit_posts(
            subreddit_entry,
            canvas_posts,
            canvas_frame_posts,
            subreddit_posts,
            subreddit_posts_full_json
        )
    )
    load_more_posts_button.pack(padx=10, pady=10)

    root.mainloop()


def main_subreddit_osint():
    setup_gui()
