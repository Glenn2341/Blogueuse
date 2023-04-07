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
#app.secret_key = os.getenv("BLOGUEUSE_SECRET_KEY")
app.secret_key = 'secret'
print("Secret Key: ", app.secret_key)
app.register_blueprint(home_blueprint)
app.register_blueprint(search_blueprint)
app.register_blueprint(post_blueprint)



# Define a variable for the path to the images folder
app.config['RECAPTCHA_PUBLIC_KEY'] = os.getenv("RECAPTCHA_PUBLIC_KEY")
app.config['RECAPTCHA_PRIVATE_KEY'] = os.getenv("RECAPTCHA_PRIVATE_KEY")
app.config['IMAGE_FOLDER'] = 'images'
postfile = 'seeddata/posts.json'
authorfile = 'seeddata/authors.json'
db_name = 'blog.db'

def seed_database():
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

def main(reseed = False):
    if(reseed):
        seed_database()
    
if __name__ == '__main__':
    main()
    app.run()

main()  # Call the main function here if you want VScode debugger to not skip it
