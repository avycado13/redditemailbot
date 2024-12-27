import praw
import requests

# Set up Reddit API credentials
reddit = praw.Reddit(
    client_id="your_client_id",
    client_secret="your_client_secret",
    user_agent="your_user_agent",
)

# Set up Mailgun credentials
MAILGUN_API_KEY = "your_mailgun_api_key"
MAILGUN_DOMAIN = "your_mailgun_domain"
MAILGUN_FROM_EMAIL = "Your Name <you@yourdomain.com>"
MAILGUN_TO_EMAIL = "recipient@example.com"

def fetch_top_posts(subreddit_name, limit=5):
    """Fetch top posts from a subreddit."""
    subreddit = reddit.subreddit(subreddit_name)
    top_posts = []

    for post in subreddit.hot(limit=limit):
        post_details = {
            "title": post.title,
            "url": post.url,
            "score": post.score,
            "comments": post.num_comments
        }
        top_posts.append(post_details)

    return top_posts

def send_email(subject, body):
    """Send an email using Mailgun."""
    return requests.post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": MAILGUN_FROM_EMAIL,
            "to": MAILGUN_TO_EMAIL,
            "subject": subject,
            "html": body
        }
    )

def generate_email_body(posts):
    """Generate an HTML email body from posts."""
    body = "<h1>Weekly Top Posts</h1>"
    for post in posts:
        body += f"<h2>{post['title']}</h2>"
        body += f"<p>Score: {post['score']}</p>"
        body += f"<p>Comments: {post['comments']}</p>"
        body += f"<a href='{post['url']}'>Read more</a>"
        body += "<hr>"

    return body

def main():
    subreddit_name = "subreddit_name"  # Replace with the desired subreddit
    top_posts = fetch_top_posts(subreddit_name)

    subject = f"Weekly Top Posts from {subreddit_name}"
    body = generate_email_body(top_posts)

    response = send_email(subject, body)

    if response.status_code == 200:
        print("Email sent successfully!")
    else:
        print(f"Failed to send email: {response.status_code} - {response.text}")

if __name__ == "__main__":
    main()
