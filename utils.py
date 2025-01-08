import re
import webbrowser
import json
import tkinter as tk

def get_serializable_data(obj):
    """
    Returns a JSON-serializable version of the object's __dict__, excluding non-serializable fields.
    """
    serializable_data = {}
    for key, value in obj.__dict__.items():
        try:
            # Test if value is JSON serializable
            json.dumps(value)
            serializable_data[key] = value
        except (TypeError, OverflowError):
            # Skip non-serializable fields
            continue
    return serializable_data

def make_links_clickable(text_widget, content):
    """
    Identifies URLs in the given content and makes them clickable in the specified Text widget.
    """
    # Regular expression to match URLs, excluding punctuation marks at the end of the URL
    url_pattern = r'(https?://[^\s"\']+)'

    text_widget.tag_config("link", foreground="blue", underline=True)

    # Find all matches for the URL pattern
    for match in re.finditer(url_pattern, content):
        url = match.group(0)
        start_idx = match.start()
        end_idx = match.end()

        # Calculate positions in the Text widget
        start_pos = text_widget.index(f"1.0+{start_idx}c")
        end_pos = text_widget.index(f"1.0+{end_idx}c")

        # Add a tag for the URL
        text_widget.tag_add("link", start_pos, end_pos)

        # Bind the click event to open the URL
        text_widget.tag_bind(
            "link", "<Button-1>", lambda e, u=url: webbrowser.open(u)
        )

def open_json_window(json_text):
    """Open a new window displaying the JSON data."""
    json_window = tk.Toplevel()
    json_window.title("JSON Data")

    json_text_widget = tk.Text(json_window, width=80, height=20, wrap="word")
    json_text_widget.insert(tk.END, json.dumps(json_text, indent=4))
    json_text_widget.config(state="disabled")
    json_text_widget.pack(padx=10, pady=10)