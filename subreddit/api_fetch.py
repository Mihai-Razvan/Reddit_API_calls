from utils import reddit, get_serializable_data

from datetime import datetime


def fetch_subreddit_info(subreddit_name):
    """
    Extracts subreddit data from Reddit and returns both filtered and full serializable JSON.
    """
    subreddit = reddit.subreddit(subreddit_name)

    # Filtered subreddit data (select specific fields)
    subreddit_info = {
        'id': subreddit.id,
        'title': subreddit.title,
        'description': subreddit.description,
        'subscribers': subreddit.subscribers,
        'created_utc': datetime.utcfromtimestamp(subreddit.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
        'over18': subreddit.over18,
        'community_icon': subreddit.community_icon,
        'subreddit_type': subreddit.subreddit_type,
    }

    # Get full JSON (serializable only)
    subreddit_info_full_json = get_serializable_data(subreddit)

    return subreddit_info, subreddit_info_full_json


def fetch_subreddit_posts_batch(subreddit_post_generator, batch_size=5):
    """
    Extracts posts from a subreddit and returns both filtered and full serializable JSON.
    """
    batch_count = 0
    next_subreddit_posts = []
    next_subreddit_posts_full_json = []

    for post in subreddit_post_generator:
        filtered_post = {
            'id': post.id,
            'title': post.title,
            'url': post.url,
            'created_utc': datetime.utcfromtimestamp(post.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
            'score': post.score,
            'ups': post.ups,
            'downs': post.downs,
            'num_comments': post.num_comments,
            'over_18': post.over_18,
            'link_flair_text': post.link_flair_text,
            'total_awards_received': post.total_awards_received,
        }

        next_subreddit_posts.append(filtered_post)
        next_subreddit_posts_full_json.append(get_serializable_data(post))

        batch_count += 1

        if batch_count == batch_size:
            break

    return next_subreddit_posts, next_subreddit_posts_full_json