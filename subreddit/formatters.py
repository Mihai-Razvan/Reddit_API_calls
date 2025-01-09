import textwrap


def format_subreddit_info(subreddit_info):
    """Format subreddit data into a string."""

    # Wrap long text at 100 characters for specific fields
    title = subreddit_info.get('description', 'N/A')
    wrapped_description = '\n'.join(textwrap.wrap(title, width=90))

    return (
        f"Id: {subreddit_info.get('id', 'N/A')}\n"
        f"Title: {subreddit_info.get('title', 'N/A')}\n"
        f"Description: {wrapped_description}\n"
        f"Subscribers: {subreddit_info.get('subscribers', 'N/A')}\n"
        f"Created: {subreddit_info.get('created_utc', 'N/A')}\n"
        f"Over 18: {subreddit_info.get('over18', 'N/A')}\n"
        f"Community Icon: {subreddit_info.get('community_icon', 'N/A')}\n"
        f"Subreddit Type: {subreddit_info.get('subreddit_type', 'N/A')}\n"
    )


def format_subreddit_post(subreddit_post):
    """Format subreddit post data into a string with wrapped text after 100 characters."""

    # Wrap long text at 100 characters for specific fields
    title = subreddit_post.get('title', 'N/A')
    wrapped_title = '\n'.join(textwrap.wrap(title, width=90))

    url = subreddit_post.get('url', 'N/A')
    wrapped_url = '\n'.join(textwrap.wrap(url, width=90))

    return (
        f"ID: {subreddit_post.get('id', 'N/A')}\n"
        f"Title: {wrapped_title}\n"  # Wrapped title after 100 characters
        f"URL: {wrapped_url}\n"  # Wrapped URL after 100 characters
        f"Created: {subreddit_post.get('created_utc', 'N/A')}\n"
        f"Score: {subreddit_post.get('score', 'N/A')}\n"
        f"Upvotes: {subreddit_post.get('ups', 'N/A')}\n"
        f"Downvotes: {subreddit_post.get('downs', 'N/A')}\n"
        f"Number of Comments: {subreddit_post.get('num_comments', 'N/A')}\n"
        f"Over 18: {subreddit_post.get('over_18', 'N/A')}\n"
        f"Flair: {subreddit_post.get('link_flair_text', 'N/A')}\n"
        f"Total Awards Received: {subreddit_post.get('total_awards_received', 'N/A')}\n"
        f"{'-' * 40}"
    )
