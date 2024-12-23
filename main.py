import praw

client_id = 'TO_BE_REPLACED'
client_secret = 'TO_BE_REPLACED'
user_agent = 'api-calls'

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)

username = 'arqf_'
user = reddit.redditor(username)

print(f"User Information for u/{username}:\n")
print(f"Username: {user.name}")
print(f"Created: {user.created_utc}")
print(f"Karma: {user.link_karma + user.comment_karma} (Link: {user.link_karma}, Comment: {user.comment_karma})")
print(f"Is Moderator: {user.is_mod}")
print(f"Is Gold: {user.is_gold}")
print("-" * 40)

print(f"Recent submissions by u/{username}:\n")
for submission in user.submissions.new(limit=5):
    print(f"Title: {submission.title}")
    print(f"Score: {submission.score}")
    print(f"URL: {submission.url}")
    print(f"Subreddit: {submission.subreddit}")
    print("-" * 40)

print(f"Recent comments by u/{username}:\n")
for comment in user.comments.new(limit=5):
    print(f"Comment: {comment.body}")
    print(f"Score: {comment.score}")
    print(f"Subreddit: {comment.subreddit}")
    print(f"Link: {comment.permalink}")
    print("-" * 40)