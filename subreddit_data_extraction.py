from datetime import datetime
from reddit_client import reddit

def extract_subreddit_info(subreddit_name):
    subreddit = reddit.subreddit(subreddit_name)
    included_fields = ['active_user_count', 'subscribers', 'emojis_enabled', 'public_description', 'community_icon',  'banner_background_image', 'subreddit_type', 'id',
                       'description', 'over18', 'created_utc', 'title']

    print(f"\033[32mId:\033[0m {subreddit.id}")
    print(f"\033[32mTitle:\033[0m {subreddit.title}")
    print(f"\033[32mDescription:\033[0m {subreddit.description}")
    print(f"\033[32mSubscribers:\033[0m {subreddit.subscribers}")
    print(f"\033[32mCreated:\033[0m {datetime.utcfromtimestamp(subreddit.created_utc).strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\033[32mOver 18:\033[0m {subreddit.over18}")
    print(f"\033[32mIcon URL:\033[0m {subreddit.community_icon}")
    print(f"\033[32mSubreddit type:\033[0m {subreddit.subreddit_type}")

    filtered_subreddit = {key: getattr(subreddit, key, None) for key in included_fields}
    return filtered_subreddit

def extract_subreddit_posts(subreddit_name, batch_size=5):
    subreddit = reddit.subreddit(subreddit_name)
    included_fields = ['title', 'downs', 'ups', 'user_reports', 'category', 'secure_media_embed', 'link_flair_text', 'score', 'approved_by', 'edited', 'content_categories',
                       'mod_note', 'over_18', 'all_awardings', 'awarders', 'removed_by', 'num_reports', 'emoval_reason', 'report_reasons', 'discussion_type', 'author',
                       '_comments_by_id']

    print(f"Fetching posts from r/{subreddit_name}:\n")

    post_generator = subreddit.new(limit=None)
    keep_fetching = True
    filtered_posts = []

    while keep_fetching:
        try:
            batch_count = 0

            for post in post_generator:
                print(f"\033[32mId:\033[0m {post.id}")
                print(f"\033[32mTitle:\033[0m {post.title}")
                print(f"\033[32mURL:\033[0m {post.url}")
                print(f"\033[32mCreated:\033[0m {datetime.utcfromtimestamp(post.created_utc).strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"\033[32mScore:\033[0m {post.score}")
                print(f"\033[32mUp-votes:\033[0m {post.ups}")
                print(f"\033[32mDown-votes:\033[0m {post.downs}")
                print(f"\033[32mNumber of comments:\033[0m {post.num_comments}")
                print(f"\033[32mOver 18:\033[0m {post.over_18}")
                print(f"\033[32mFlair:\033[0m {post.link_flair_text}")
                print(f"\033[32mNumber of awards:\033[0m {post.total_awards_received}")
                print("-" * 40)

                filtered_post = {key: getattr(post, key, None) for key in included_fields}
                filtered_posts.append(filtered_post)

                batch_count += 1

                if batch_count == batch_size:
                    break

            if batch_count < batch_size:
                print("\033[35mNo more posts found.\033[0m")
                break

            user_response = input(f"Do you want to fetch more posts from r/{subreddit_name}? (yes/no): ").strip().lower()
            if user_response not in ["yes", "y"]:
                keep_fetching = False

        except Exception as e:
            print(f"An error occurred: {e}")
            break

    return filtered_posts