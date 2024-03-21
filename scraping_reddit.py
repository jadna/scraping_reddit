import os
from dotenv import load_dotenv
import json
import praw
from praw.models import MoreComments
from datetime import datetime


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

def get_reddit(subreddit, query, sort, syntax, period, limit):


    posts = reddit.subreddit(subreddit).search(query=query, sort=sort, syntax=syntax, time_filter=period, limit=limit)
    print(f"SubReddit: {subreddit} - Query: {query}")
    print("=========================================================")
    
    for index,post in enumerate(posts):
        
        posts_dict = {}

        # Subreddit
        posts_dict["Subreddit"] = subreddit
        # Query research
        posts_dict["Query"] = query
        # Number of post
        posts_dict["Post number"] = index+1
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

        # print(f"id: {post.id} - Title: {post.title} - Total Comments: {post.num_comments}")
        # print(f"URL: {post.url}")
        # print(f"{post.selftext}")
        print(f"Post {index+1}")

        # Get comments
        posts_dict["Comments"] = []
        submission = reddit.submission(id=post.id)
        #replace = submission.comments.replace_more()

        for index, comment in enumerate(submission.comments):
            posts_dict["Comments"].append({
                "Comment number": index+1,
                "Comment ID": comment.id,
                "Comment": comment.body if "body" in submission.comments else "" 
            })

            if type(comment) == MoreComments:
                continue

            # print(f"Comment {index} id: {comment.id} -  {comment.body}")
            print(f"    Comment {index+1}")
        
        posts_list.append(posts_dict)
        #print("=========================================================")
    
    # with open("data.json", "a") as outfile: 
    #     json.dump({"posts":posts_list}, outfile)

    return posts_list


if __name__ == '__main__':

    day = datetime.now()
    name_data = "scraping_reddit/data"+str(day).replace(":","_").replace(".","_").replace(" ","_").replace("-","_")+".json"

    subreddit = "porto" # "fcporto", "portugal"
    query = ["Autocarro", "SCTP", "Anda", "Metrobus", "Metro", "Onibus", "Trotinete"]
    sort = "relevance"
    syntax = "cloudsearch"
    period = "all"
    limit = 100
    
    total = []

    for q in query:
        total += get_reddit(subreddit, q, sort, syntax, period, limit)

    with open(name_data, "w") as outfile: 
        json.dump({"posts":total}, outfile)