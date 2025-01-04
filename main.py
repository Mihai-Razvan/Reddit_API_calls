import praw
from datetime import datetime


client_id = 'TO_BE_REPLACED'
client_secret = 'TO_BE_REPLACED'
user_agent = 'api-calls'

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)


def extract_data_about_user(username):
    user = reddit.redditor(username)
    included_fields = ['name', 'is_employee', 'subreddit', 'snoovatar_size', 'awardee_karma', 'id', 'verified', 'is_gold', 'is_mod', 'awarder_karma', 'has_verified_email',
                       'icon_img', 'hide_from_robots', 'link_karma', 'total_karma', 'created_utc', 'comment_karma']

    print(f"\033[32mId:\033[0m {user.id}")
    print(f"\033[32mUsername:\033[0m {user.name}")
    print(f"\033[32mAvatar URL:\033[0m {user.icon_img}")
    print(f"\033[32mCreated:\033[0m {datetime.utcfromtimestamp(user.created_utc).strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\033[32mKarma:\033[0m {user.link_karma + user.comment_karma} (Link: {user.link_karma}, Comment: {user.comment_karma})")
    print(f"\033[32mIs Employee:\033[0m {user.is_employee}")
    print(f"\033[32mIs Moderator:\033[0m {user.is_mod}")
    print(f"\033[32mIs Gold:\033[0m {user.is_gold}")

    filtered_user= {key: value for key, value in user.__dict__.items() if key in included_fields}
    return filtered_user


def extract_posts_of_user(username, batch_size=5):
    user = reddit.redditor(username)
    filtered_submissions = []
    included_fields = ['subreddit', 'title', 'downs', 'ups', 'total_awards_received', 'media_embed', 'user_reports', 'category',
                       'score', 'approved_by', 'thumbnail', 'edited', 'content_categories', 'removed_by', 'over_18',
                       'all_awardings', 'awarders', 'num_reports', 'removal_reason', 'num_comments', 'created_utc']

    print(f"Fetching submissions by u/{username}:\n")

    submission_generator = user.submissions.new(limit=None)
    keep_fetching = True

    while keep_fetching:
        try:
            batch_count = 0

            for submission in submission_generator:
                print(f"\033[32mId:\033[0m {submission.id}")
                print(f"\033[32mTitle:\033[0m {submission.title}")
                print(f"\033[32mURL:\033[0m {submission.url}")
                print(f"\033[32mCreated:\033[0m {datetime.utcfromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"\033[32mSubreddit:\033[0m {submission.subreddit}")
                print(f"\033[32mThumbnail URL:\033[0m {submission.thumbnail}")
                print(f"\033[32mNumber of comments:\033[0m {submission.num_comments}")
                print(f"\033[32mScore:\033[0m {submission.score}")
                print(f"\033[32mUp-votes:\033[0m {submission.ups}")
                print(f"\033[32mDown-votes:\033[0m {submission.downs}")
                print(f"\033[32mNumber of awards:\033[0m {submission.total_awards_received}")
                print("-" * 40)

                filtered_submission = {key: getattr(submission, key, None) for key in included_fields}
                filtered_submissions.append(filtered_submission)

                batch_count += 1

                if batch_count == batch_size:
                    break

            if batch_count < batch_size:
                print("\033[35m\nNo more posts found.\n\033[0m")
                break

            user_response = input("Do you want to fetch more submissions? (yes/no): ").strip().lower()
            if user_response not in ["yes", "y"]:
                keep_fetching = False

        except Exception as e:
            print(f"An error occurred: {e}")
            break

    return filtered_submissions


def extract_comments_of_user(username, batch_size=5):
    user = reddit.redditor(username)
    filtered_comments = []
    included_fields = ['ups', 'num_reports', 'total_awards_received', 'subreddit', 'id', 'num_comments', 'parent_id', 'score',
                       'over_18', 'removal_reason', 'approved_by', 'body', 'edited', 'downs', 'link_permalink', 'created_utc']

    print(f"Fetching comments by u/{username}:\n")

    comment_generator = user.comments.new(limit=None)
    keep_fetching = True

    while keep_fetching:
        try:
            batch_count = 0

            for comment in comment_generator:
                print(f"\033[32mId:\033[0m {comment.id}")
                print(f"\033[32mComment:\033[0m {comment.body}")
                print(f"\033[32mURL:\033[0m {comment.link_permalink}")
                print(f"\033[32mCreated:\033[0m {datetime.utcfromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"\033[32mSubreddit:\033[0m {comment.subreddit}")
                print(f"\033[32mScore:\033[0m {comment.score}")
                print(f"\033[32mUp-votes:\033[0m {comment.ups}")
                print(f"\033[32mDown-votes:\033[0m {comment.downs}")
                print("-" * 40)

                filtered_comment = {key: getattr(comment, key, None) for key in included_fields}
                filtered_comments.append(filtered_comment)

                batch_count += 1

                if batch_count == batch_size:
                    break

            if batch_count < batch_size:
                print("\033[35m\nNo more comments found.\n\033[0m")
                break

            user_response = input("Do you want to fetch more comments? (yes/no): ").strip().lower()
            if user_response not in ["yes", "y"]:
                keep_fetching = False

        except Exception as e:
            print(f"An error occurred: {e}")
            break

    return filtered_comments


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


####################     MAIN     ####################

#user_data = extract_data_about_user("TheGreatLateElmo")
#print(user_data)

# posts_of_user = extract_posts_of_user("FrostyDiscipline7558")
# print(posts_of_user)

#comments_of_user = extract_comments_of_user("TheTwelveYearOld")
#print(comments_of_user)

#subreddit_info = extract_subreddit_info("cybersecurity")
#print(subreddit_info)

posts_from_subreddit = extract_subreddit_posts("cybersecurity")
print(posts_from_subreddit)