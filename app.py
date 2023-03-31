#http://localhost:5000/

from flask import Flask, abort, render_template, request, redirect, url_for
from random import randint
from models.Post import Post
from models.Comment import Comment
from models.Author import Author
from models.Tag import Tag
import json
import random
import os
import sqlite3
import seeddatainjection
import BusinessLogicLayer.businesslogic
from controllers.home import home_blueprint
from controllers.search import search_blueprint
from controllers.post import post_blueprint

app = Flask(__name__)
app.debug = True
app.register_blueprint(home_blueprint)
app.register_blueprint(search_blueprint)
app.register_blueprint(post_blueprint)

app.secret_key = 'your_secret_key_here'

# Define a variable for the path to the images folder
app.config['IMAGE_FOLDER'] = 'images'
postfile = 'seeddata/posts.json'
authorfile = 'seeddata/authors.json'


# A function to generate a list of Post objects with random titles and content
def get_posts():
    with open(postfile, 'r') as file:
         posts_data = json.load(file)

    #Deserialize the JSON string to a list of dictionaries
    #posts_data = json.loads(data)

    # Convert the list of dictionaries back to Post and Comment objects
# Convert the list of dictionaries back to Post and Comment objects
    posts = []
    for post_data in posts_data:
        comments = [Comment(comment_data['postid'], comment_data['id'], comment_data['author'], comment_data['content'], comment_data['created_utc']) for comment_data in post_data['comments']]
        post = Post(post_data['authorid'], post_data['id'], post_data['title'], post_data['author'], post_data['tags'], post_data['preview'], post_data['content'], comments, post_data['created_utc'])
        posts.append(post)

    return posts








# A function to generate a list of Post objects with random titles and content
def get_authors():
    with open(authorfile, 'r') as file:
        author_dicts = json.load(file)
    return [Author.from_dict(author_dict) for author_dict in author_dicts]


def get_random_topic(postlist):
    alltags = get_all_topics(postlist)
    topic = random.sample(list(alltags), 1)[0]
    return topic

#Get posts for a random topic
def get_topic_selection(topic, postlist):

    topicposts = [post for post in postlist if topic in post.tags]

    if(len(topicposts) > 3):
        topicposts = random.sample(topicposts, 3)

    return topicposts

def get_all_topics(postlist):
    alltags = set()
    for post in postlist:
        for tag in post.tags:
            alltags.add(tag)
    return alltags

def post_search(querystring, postlist):
    #Get all authors and tags
    allauthors = set()
    alltags = set()
    for post in postlist:
        allauthors.add(post.author)
        for tag in post.tags:
            alltags.add(tag)
            
    #Get the authors and tags being searched for
    authorsearch = set()
    tagsearch = set()
    
    for author in allauthors:
        if(author in querystring):
            authorsearch.add(author)
            querystring = querystring.replace(author, '')
    querytagtokens = querystring.split(' ')
    
    
    for tag in alltags:
        if(tag in querytagtokens):
            tagsearch.add(tag)
    
    if((len(authorsearch) == 0) and (len(tagsearch) == 0)):
        return []
    
    #print(f'authors: {authorsearch}')
    #print(f'tags: {tagsearch}\n')
    
    #Filter the posts down first by author, then by tag
    filteredposts = set()
    
    if(len(authorsearch) > 0):
        for post in postlist:
            if(post.author in authorsearch):
                filteredposts.add(post)
    else:
        filteredposts = postlist
    
    if(len(tagsearch) > 0):
        filteredposts = [post for post in filteredposts if set(post.tags).intersection(tagsearch)]
        
    return filteredposts

def main():
    db_name = 'blog.db'

    # Check if the database file exists
    if os.path.exists(db_name):
        # Delete the database file
        os.remove(db_name)
        print(f"{db_name} has been deleted.")

    # Create a new SQLite3 database with the same name
    conn = sqlite3.connect(db_name)
    print(f"{db_name} has been created.")

    # Read seed data from json and inject to db
    seeddatainjection.injectseeddata(db_name)

    posts = BusinessLogicLayer.businesslogic.getposts(1)
    postsbytag = BusinessLogicLayer.businesslogic.get_posts_by_tag(6)

    results1 = BusinessLogicLayer.businesslogic.post_search('Sarah Lane')
    results2 = BusinessLogicLayer.businesslogic.post_search('Sarah Lane Yoga')
    results3 = BusinessLogicLayer.businesslogic.post_search('Sarah Lane Scott Dyker')
    results4 = BusinessLogicLayer.businesslogic.post_search('Spiritual')
    results5 = BusinessLogicLayer.businesslogic.post_search('Yoga Games')
    results6 = BusinessLogicLayer.businesslogic.post_search('')
    results7 = BusinessLogicLayer.businesslogic.post_search('Hunting')
    results8 = BusinessLogicLayer.businesslogic.post_search('Hunting Yoga')

    #comment1 = Comment(postid=1, id=12345, author='test', content='Testing Comment', created_utc=1679796000)
    #BusinessLogicLayer.businesslogic.save_comment(comment=comment1)

    return 0

main()  # Call the main function here, otherwise VScode debugger will skip it

if __name__ == '__main__':
    main()
    app.run()
