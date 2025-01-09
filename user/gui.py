import tkinter as tk
from tkinter import messagebox, ttk

from utils import reddit, make_links_clickable, open_json_window

from .formatters import format_user_info, format_user_post, format_user_comment
from .api_fetch import fetch_user_info, fetch_user_posts_batch, fetch_user_comments_batch

user_posts_generator = None
user_comments_generator = None

def get_user_info(username_entry, user_info_text_widget, show_user_info_json_button):
    """Fetch user data and update the GUI with selected fields."""
    username = username_entry.get().strip()
    if not username:
        messagebox.showerror("Error", "Username field is empty!")
        return

    try:
        user_info, user_info_full_json = fetch_user_info(username)
        user_data_str = format_user_info(user_info)
        user_info_text_widget.config(state="normal")
        user_info_text_widget.delete(1.0, tk.END)
        user_info_text_widget.insert(tk.END, user_data_str)
        user_info_text_widget.config(state="disabled")

        make_links_clickable(user_info_text_widget, user_data_str)
        show_user_info_json_button.config(state="normal", command=lambda: open_json_window(user_info_full_json))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch data: {e}")

def get_user_posts(username_entry, canvas, canvas_frame, user_posts, user_posts_full_json):
    global user_posts_generator
    """Fetch and display posts for a given username."""
    username = username_entry.get().strip()
    if not username:
        messagebox.showerror("Error", "Username field is empty!")
        return

    try:
        if len(user_posts) == 0:  # Fetch posts initially
            user_posts_generator = reddit.redditor(username).submissions.new(limit=None)
            next_user_posts, next_user_posts_full_json = fetch_user_posts_batch(user_posts_generator)
            user_posts.extend(next_user_posts)
            user_posts_full_json.extend(next_user_posts_full_json)
            display_user_posts(user_posts, user_posts_full_json, canvas, canvas_frame)
        else:  # Load more posts when button is clicked
            next_user_posts, next_user_posts_full_json = fetch_user_posts_batch(user_posts_generator, batch_size=5)
            user_posts.extend(next_user_posts)
            user_posts_full_json.extend(next_user_posts_full_json)
            display_user_posts(user_posts, user_posts_full_json, canvas, canvas_frame)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch posts: {e}")

def get_user_comments(username_entry, canvas, canvas_frame, user_comments, user_comments_full_json):
    global user_comments_generator
    """Fetch and display comments for a given username."""
    username = username_entry.get().strip()
    if not username:
        messagebox.showerror("Error", "Username field is empty!")
        return

    try:
        if len(user_comments) == 0:  # Fetch comments initially
            user_comments_generator = reddit.redditor(username).comments.new(limit=None)
            next_user_comments, next_user_comments_full_json = fetch_user_comments_batch(user_comments_generator)
            user_comments.extend(next_user_comments)
            user_comments_full_json.extend(next_user_comments_full_json)
            display_user_comments(user_comments, user_comments_full_json, canvas, canvas_frame)
        else:  # Load more comments when button is clicked
            next_user_comments, next_user_comments_full_json = fetch_user_comments_batch(user_comments_generator, batch_size=5)
            user_comments.extend(next_user_comments)
            user_comments_full_json.extend(next_user_comments_full_json)
            display_user_comments(user_comments, user_comments_full_json, canvas, canvas_frame)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch comments: {e}")

def display_user_posts(posts, full_posts_json, canvas, canvas_frame):
    """Display the list of posts and their details in the canvas."""
    for widget in canvas_frame.winfo_children():
        widget.destroy()

    for post, full_post_json in zip(posts, full_posts_json):
        post_data = format_user_post(post)
        post_frame = tk.Frame(canvas_frame)
        post_frame.pack(fill="x", padx=10, pady=5)

        post_label_widget = tk.Label(post_frame, text=post_data, justify="left", anchor="w")
        post_label_widget.pack(side="left", fill="x", expand=True)

        show_user_post_json_button = tk.Button(post_frame, text="View JSON", command=lambda p=full_post_json: open_json_window(p))
        show_user_post_json_button.pack(side="right", padx=5)

    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

def display_user_comments(comments, full_comments_json, canvas, canvas_frame):
    """Display the list of comments and their details in the canvas."""
    for widget in canvas_frame.winfo_children():
        widget.destroy()

    for comment, full_comment_json in zip(comments, full_comments_json):
        comment_data = format_user_comment(comment)
        comment_frame = tk.Frame(canvas_frame)
        comment_frame.pack(fill="x", padx=10, pady=5)

        comment_label_widget = tk.Label(comment_frame, text=comment_data, justify="left", anchor="w")
        comment_label_widget.pack(side="left", fill="x", expand=True)

        show_user_comment_json_button = tk.Button(comment_frame, text="View JSON", command=lambda c=full_comment_json: open_json_window(c))
        show_user_comment_json_button.pack(side="right", padx=5)

    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

def setup_gui():
    root = tk.Tk()
    root.title("Reddit User Data Extractor")
    root.geometry("800x800")
    notebook = ttk.Notebook(root)

    selected_tab = ttk.Frame(notebook)
    posts_tab = ttk.Frame(notebook)
    comments_tab = ttk.Frame(notebook)

    notebook.add(selected_tab, text="General Info")
    notebook.add(posts_tab, text="Posts")
    notebook.add(comments_tab, text="Comments")
    notebook.pack(expand=True, fill="both")

    tk.Label(selected_tab, text="Enter Reddit Username:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    username_entry = tk.Entry(selected_tab, width=30)
    username_entry.grid(row=0, column=1, padx=10, pady=10)

    user_info_text_widget = tk.Text(selected_tab, width=100, height=40, state="disabled")
    user_info_text_widget.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

    show_user_info_json_button = tk.Button(selected_tab, text="View Full JSON", state="disabled")
    show_user_info_json_button.grid(row=2, column=1, pady=10)

    fetch_button = tk.Button(selected_tab, text="Fetch Data", command=lambda: get_user_info(username_entry, user_info_text_widget, show_user_info_json_button))
    fetch_button.grid(row=0, column=2, padx=10, pady=10)

    # User Posts Tab
    posts_canvas_frame = ttk.Frame(posts_tab)

    posts_canvas_frame.pack(padx=10, pady=10, fill="both", expand=True)
    canvas_posts = tk.Canvas(posts_canvas_frame)
    canvas_posts.pack(side="left", fill="both", expand=True)
    scrollbar_posts = tk.Scrollbar(posts_canvas_frame, orient="vertical", command=canvas_posts.yview)
    scrollbar_posts.pack(side="right", fill="y")
    canvas_posts.config(yscrollcommand=scrollbar_posts.set)
    canvas_frame_posts = ttk.Frame(canvas_posts)
    canvas_posts.create_window((0, 0), window=canvas_frame_posts, anchor="nw")
    user_posts = []
    user_posts_full_json = []
    load_more_posts_button = tk.Button(posts_tab, text="Load More Posts", command=lambda: get_user_posts(username_entry, canvas_posts, canvas_frame_posts, user_posts, user_posts_full_json))
    load_more_posts_button.pack(padx=10, pady=10)

    # User Comments Tab
    comments_canvas_frame = ttk.Frame(comments_tab)
    comments_canvas_frame.pack(padx=10, pady=10, fill="both", expand=True)
    canvas_comments = tk.Canvas(comments_canvas_frame)
    canvas_comments.pack(side="left", fill="both", expand=True)
    scrollbar_comments = tk.Scrollbar(comments_canvas_frame, orient="vertical", command=canvas_comments.yview)
    scrollbar_comments.pack(side="right", fill="y")
    canvas_comments.config(yscrollcommand=scrollbar_comments.set)
    canvas_frame_comments = ttk.Frame(canvas_comments)
    canvas_comments.create_window((0, 0), window=canvas_frame_comments, anchor="nw")
    user_comments = []
    user_comments_full_json = []
    load_more_comments_button = tk.Button(comments_tab, text="Load More Comments", command=lambda: get_user_comments(username_entry, canvas_comments, canvas_frame_comments, user_comments, user_comments_full_json))
    load_more_comments_button.pack(padx=10, pady=10)

    root.mainloop()

def main_user_osint():
    setup_gui()
