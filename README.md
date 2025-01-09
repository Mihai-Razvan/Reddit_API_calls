# Reddit API Calls - Desktop Application

This project is a Python desktop application built with Tkinter that interacts with the Reddit API. It allows you to authenticate with your Reddit account and retrieve information about users and subreddits through a user-friendly graphical interface.

## Overview

The application provides a simple way to interact with Reddit programmatically. It currently supports the following functionalities:

1.  **Retrieve User Information:** View information about a Reddit user, including their username. You can also browse their posts and comments.
2.  **Retrieve Subreddit Information:** View information about a Reddit subreddit, including its name. You can also browse its posts.
3.  **Navigation:** A main GUI window allows you to choose between viewing user information or subreddit information.
4.  **JSON View:** For each retrieved piece of information, you have the option to see the raw response received from the Reddit API, formatted as a pretty-printed JSON.

## Installation

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/Mihai-Razvan/Reddit_API_calls.git
    cd Reddit_API_calls
    ```

2.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    This will install the required libraries:
    *   `python-dotenv`: To load environment variables from a `.env` file.
    *   `praw`: The Python Reddit API Wrapper.
    *   `tkinter`: Python's standard GUI toolkit (usually comes pre-installed with Python, but it's good to ensure it's installed).

3.  **Set up a Reddit App:**

    *   Go to [Reddit App Preferences](https://www.reddit.com/prefs/apps/).
    *   Click "create another app..." at the bottom of the page.
    *   Choose "script" type.
    *   Give it a name and a description.
    *   Click "create app".
    *   Copy the client ID (the text below the app name) and the client secret.

4.  **Create a .env File:**

    *   **Manually create a file named `.env` at the root of the project directory (in the same directory as your Python script).**
    *   Add the following lines to the `.env` file, replacing the placeholders with the actual values you copied from the Reddit App settings:

        ```
        CLIENT_ID=your_client_id
        CLIENT_SECRET=your_client_secret
        ```

## Usage

1.  **Run the Application:**

    ```bash
    python main.py
    ```

2.  **Navigate:**

    *   Use the main window to choose between "User" and "Subreddit" views.
    *   Enter the desired username or subreddit name in the respective input fields.
    *   Click the appropriate buttons to fetch information, view posts, comments (for users), or the raw JSON response.

## GUI Functionality (Updated)

The application's graphical user interface is now centered around retrieving and displaying user and subreddit information.

### Main Window

*   **Functionality:** This is the starting point where you select whether to work with users or subreddits.
*   **Actions:**
    *   **User Button:** Opens the User Information window.
    *   **Subreddit Button:** Opens the Subreddit Information window.

### User Information Window

*   **Functionality:** Retrieves and displays information about a specified Reddit user.
*   **Interface Elements:**
    *   **Username Input:** Enter the username of the Reddit user you want to look up.
    *   **Get User Info Button:** Fetches basic user information (e.g., username, karma).
    *   **View Posts Button:** Retrieves and displays the user's posts.
    *   **View Comments Button:** Retrieves and displays the user's comments.
    *   **View JSON Button:** Shows the raw JSON response from the Reddit API for the user.

### Subreddit Information Window

*   **Functionality:** Retrieves and displays information about a specified subreddit.
*   **Interface Elements:**
    *   **Subreddit Name Input:** Enter the name of the subreddit you want to look up.
    *   **Get Subreddit Info Button:** Fetches basic subreddit information (e.g., name, description, subscriber count).
    *   **View Posts Button:** Retrieves and displays the subreddit's posts.
    *   **View JSON Button:** Shows the raw JSON response from the Reddit API for the subreddit.

## Notes

*   The application relies on the `.env` file for storing your Reddit API credentials. Make sure this file is created correctly and is not accidentally committed to version control (add `.env` to your `.gitignore` file).
*   Error handling is likely still basic. Consider adding more robust error handling for various API errors, network issues, and invalid user/subreddit inputs.