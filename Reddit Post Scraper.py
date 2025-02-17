# Reddit scraper using praw API
# Irving Garcia
# Last modified: 2-17-2025
# Input: Subreddit name and title keyword
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

# Specify the subreddit and keyword to search for
subreddit_name = "chatGPT"
keyword = "therapy"

# Fetches subreddit and searches for posts containing the keyword
subreddit = reddit_read_only.subreddit(subreddit_name)
posts = subreddit.search(keyword, limit=10)  # Adjust limit as needed

# List to store post data
post_data_list = []

# Iterate through the search results
for submission in posts:
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
                "author": str(comment.author),  # Include OP
                "score": comment.score  # Include upvotes
            })
            # Recursively fetch replies (nested comments)
            fetch_comments(comment.replies, level + 1)

    # Start fetching comments from the top-level
    fetch_comments(submission.comments)

    # Create a dictionary to store post data for json file
    post_data = {
        "title": submission.title,  # Post title
        "link": submission.url,  # Post link
        "comments": post_comments  # List of comments with nesting
    }

    # Append the post data to the list
    post_data_list.append(post_data)

# Get the directory where the Python script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the output file path for json file
output_file = os.path.join(script_dir, f"reddit_posts_with_{keyword}.json")

# Export data to a .json file
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(post_data_list, file, indent=4)

print(f"Post data containing '{keyword}' has been exported to {output_file}")