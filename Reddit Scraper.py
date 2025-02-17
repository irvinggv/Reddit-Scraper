# Reddit scraper using praw API
# Irving Garcia
# Last modified: 2-16-2025
# Input: Reddit post URL
# Output: .json file

import praw
import pandas as pd
import os
import json
from praw.models import MoreComments


# You're going to need a reddit developer account for this. Once you have that copy in the following info provided in your account
reddit_read_only = praw.Reddit(client_id="",         # your client id
                               client_secret="",      # your client secret
                               user_agent="")    # your user agent

# *** The following is code to post the top 5 post from a subreddit. Its commented out as it was only for a test but may be useful***

# Inputs name of the Subreddit
# subreddit = reddit_read_only.subreddit("chatGPT")

# Display the name of the Subreddit
#print("Display Name:", subreddit.display_name)
 
# Display the title of the Subreddit
#print("Title:", subreddit.title)
 
# Display the description of the Subreddit
#print("Description:", subreddit.description)

# Prints top 5 posts of the subreddit
#print("top 5 post on r/chatGPT")

#for post in subreddit.hot(limit=5):

#    print(post.title)
#    print()


# URL of post you are wanting to scrape
url = "https://www.reddit.com/r/ChatGPT/comments/1far8or/i_made_the_mistake_of_using_chatgpt_as_my/"

# Fetch the submission
submission = reddit_read_only.submission(url=url)

# Fetch all comments, including nested ones
submission.comments.replace_more(limit=None)

# List to store all comments and their nesting levels
post_comments = []

# Function to recursively fetch comments and their nesting level
def fetch_comments(comments, level=0):
    for comment in comments:
        if isinstance(comment, MoreComments):
            continue
        # Append the comment and its nesting level
        post_comments.append({
            "comment": comment.body,
            "nesting_level": level,
            "author": str(comment.author),  # Include comment author
            "score": comment.score  # Include comment score
        })
        # Recursively fetch replies (nested comments)
        fetch_comments(comment.replies, level + 1)

# Start fetching comments from the top-level
fetch_comments(submission.comments)

# Create a dictionary to store post data
post_data = {
    "title": submission.title,  # Post title
    "link": submission.url,  # Post link
    "comments": post_comments  # List of comments with nesting
}

# Get the directory where the Python script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the output file path
output_file = os.path.join(script_dir, "reddit_post_data.json")

# Export data to a .json file
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(post_data, file, indent=4)  # Use indent for pretty-printing

print(f"Post data has been exported to {output_file}")