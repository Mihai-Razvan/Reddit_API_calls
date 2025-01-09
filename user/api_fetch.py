from utils import reddit, get_serializable_data

from datetime import datetime


def fetch_user_info(username):
    """
    Extracts user data from Reddit and returns both filtered and full serializable JSON.
    """
    user = reddit.redditor(username)

    # Filtered user data (select specific fields)
    user_info = {
        'id': user.id,
        'username': user.name,
        'icon_img': user.icon_img,
        'created_utc': datetime.utcfromtimestamp(user.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
        'karma': user.link_karma + user.comment_karma,
        'link_karma': user.link_karma,
        'comment_karma': user.comment_karma,
        'is_employee': user.is_employee,
        'is_mod': user.is_mod,
        'is_gold': user.is_gold,
    }

    # Get full JSON (serializable only)
    user_info_full_json = get_serializable_data(user)

    return user_info, user_info_full_json


def fetch_user_posts_batch(user_post_generator, batch_size=5):
    """
    Extracts posts of a given user from Reddit and returns both filtered and full serializable JSON.
    """
    batch_count = 0
    next_user_posts = []
    next_user_posts_full_json = []

    for user_post in user_post_generator:
        filtered_post = {
            'id': user_post.id,
            'title': user_post.title,
            'url': user_post.url,
            'created_utc': datetime.utcfromtimestamp(user_post.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
            'subreddit': user_post.subreddit.display_name,
            'ups': user_post.ups,
            'downs': user_post.downs,
            'score': user_post.score,
            'total_awards_received': user_post.total_awards_received,
        }

        next_user_posts.append(filtered_post)
        next_user_posts_full_json.append(get_serializable_data(user_post))

        batch_count += 1

        if batch_count == batch_size:
            break

    return next_user_posts, next_user_posts_full_json


def fetch_user_comments_batch(comment_generator, batch_size=5):
    """
    Extracts comments of a given user from Reddit and returns both filtered and full serializable JSON.
    """
    batch_count = 0
    next_user_comments = []
    next_user_comments_full_json = []

    for user_comment in comment_generator:
        filtered_comment = {
            'id': user_comment.id,
            'body': user_comment.body,
            'url': user_comment.link_permalink,
            'created_utc': datetime.utcfromtimestamp(user_comment.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
            'subreddit': user_comment.subreddit.display_name,
            'ups': user_comment.ups,
            'downs': user_comment.downs,
            'score': user_comment.score,
            'total_awards_received': user_comment.total_awards_received,
            'parent_id': user_comment.parent_id,
        }

        next_user_comments.append(filtered_comment)
        next_user_comments_full_json.append(get_serializable_data(user_comment))

        batch_count += 1

        if batch_count == batch_size:
            break

    return next_user_comments, next_user_comments_full_json