import textwrap

def format_user_info(user_info):
    """Format user data into a string."""
    return (
        f"Id: {user_info.get('id', 'N/A')}\n"
        f"Username: {user_info.get('username', 'N/A')}\n"
        f"Avatar URL: {user_info.get('icon_img', 'N/A')}\n"
        f"Created: {user_info.get('created_utc', 'N/A')}\n"
        f"Karma: {user_info.get('karma', 'N/A')} "
        f"(Link: {user_info.get('link_karma', 'N/A')}, Comment: {user_info.get('comment_karma', 'N/A')})\n"
        f"Is Employee: {user_info.get('is_employee', 'N/A')}\n"
        f"Is Moderator: {user_info.get('is_mod', 'N/A')}\n"
        f"Is Gold: {user_info.get('is_gold', 'N/A')}"
    )


def format_user_post(user_post):
    """Format post data into a string with wrapped text after 100 characters."""

    # Wrap long text at 100 characters for specific fields
    title = user_post.get('title', 'N/A')
    wrapped_title = '\n'.join(textwrap.wrap(title, width=100))

    url = user_post.get('url', 'N/A')
    wrapped_url = '\n'.join(textwrap.wrap(url, width=100))

    return (
        f"ID: {user_post.get('id', 'N/A')}\n"
        f"Title: {wrapped_title}\n"  # Wrapped title after 100 characters
        f"Subreddit: {user_post.get('subreddit', 'N/A')}\n"
        f"URL: {wrapped_url}\n"  # Wrapped URL after 100 characters
        f"Created: {user_post.get('created_utc', 'N/A')}\n"
        f"Upvotes: {user_post.get('ups', 'N/A')}\n"
        f"Downvotes: {user_post.get('downs', 'N/A')}\n"
        f"Score: {user_post.get('score', 'N/A')}\n"
        f"Total Award Received: {user_post.get('total_awards_received', 'N/A')}\n"
        f"{'-' * 40}"
    )


def format_user_comment(user_comment):
    """Format post data into a string with wrapped text after 100 characters."""

    # Wrap long text at 100 characters for specific fields
    body = user_comment.get('body', 'N/A')
    wrapped_body = textwrap.fill(body, width=100)

    url = user_comment.get('url', 'N/A')
    wrapped_url = '\n'.join(textwrap.wrap(url, width=100))

    return (
        f"ID: {user_comment.get('id', 'N/A')}\n"
        f"Body: {wrapped_body}\n"  # Add the wrapped body text here
        f"Subreddit: {user_comment.get('subreddit', 'N/A')}\n"
        f"URL: {wrapped_url}\n"
        f"Created: {user_comment.get('created_utc', 'N/A')}\n"
        f"Upvotes: {user_comment.get('ups', 'N/A')}\n"
        f"Downvotes: {user_comment.get('downs', 'N/A')}\n"
        f"Score: {user_comment.get('score', 'N/A')}\n"
        f"Total Award Received: {user_comment.get('total_awards_received', 'N/A')}\n"
        f"Parent ID: {user_comment.get('parent_id', 'N/A')}\n"
        f"{'-' * 40}"
    )
