import os
from dotenv import load_dotenv
import pandas as pd
import json
import praw
from praw.models import MoreComments

load_dotenv()

reddit = praw.Reddit(
                        client_id=os.environ['CLIENT_ID'],  # your client id
                        client_secret=os.environ['CLIENT_SECRET'], # your client secret
                        user_agent=os.environ['USER_AGENT'], # your user agent
                        username=os.environ['USERNAME'],
                        password=os.environ['PASSWORD']
                    )  
reddit.read_only = True      

posts_list = []

def get_reddit(subreddit, query, sort, period, limit):


    posts = reddit.subreddit(subreddit).search(query=query, sort=sort, syntax='lucene', time_filter=period, limit=limit)
    print(f"Query: {query} - Quantidade Reddit: {0}")
    print("=========================================================")
    
    for post in posts:
        
        posts_dict = {}

        # Title of each post
        posts_dict["Title"] = post.title
        # Text inside a post
        posts_dict["Post Text"] = post.selftext
        # Unique ID of each post
        posts_dict["ID"] = post.id   
        # The score of a post
        posts_dict["Score"] = post.score      
        # Total number of comments inside the post
        posts_dict["Total Comments"] = post.num_comments       
        # URL of each post
        posts_dict["Post URL"] = post.url
        # Time the subreddit was created, represented in Unix Time
        posts_dict["Created at"] = post.created_utc

        print(f"id: {post.id} - Title: {post.title} - Total Comments: {post.num_comments}")
        print(f"URL: {post.url}")
        print(f"{post.selftext}")

        # Get comments
        posts_dict["Comments"] = []
        submission = reddit.submission(id=post.id)
        #replace = submission.comments.replace_more()

        for index, comment in enumerate(submission.comments):
            posts_dict["Comments"].append({
                "Comment ID":comment.id,
                "Comment":comment.body
            })

            if type(comment) == MoreComments:
                continue

            print(f"Comment {index} id: {comment.id} -  {comment.body}")
        
        posts_list.append(posts_dict)
        #print("=========================================================")
    
    with open("data.json", "w") as outfile: 
        json.dump({"posts":posts_list}, outfile)



if __name__ == '__main__':

    subreddit = "porto"
    query = ["autocarro", "SCTP", "Anda", "Metrobus", "Metro"]
    sort = "relevance"
    period = "all"
    limit = 100
    
    for q in query:
        get_reddit(subreddit, q, sort, period, limit)