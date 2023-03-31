from models.Post import Post
from models.Comment import Comment
from models.Author import Author
from models.Tag import Tag
import json
import sqlite3

postfile = 'seeddata/posts.json'
authorfile = 'seeddata/authors.json'
commentfile = 'seeddata/comments.json'
tagsfile = 'seeddata/tags.json'
posttagsfile = 'seeddata/posttags.json'

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

# A function to get authors from seed file
def get_authors():
    with open(authorfile, 'r') as file:
        author_dicts = json.load(file)
    return [Author.from_dict(author_dict) for author_dict in author_dicts]

# A function to generate a list of comment objects from a seed file
def get_comments():
    #Read the data back
    with open(commentfile, 'r') as file:
        comments_data = json.load(file)
    comments = [Comment(comment_data['postid'], comment_data['id'], comment_data['author'], comment_data['content'], comment_data['created_utc']) for comment_data in comments_data]
    return comments

def get_tags():
    #Read the data 
    with open(tagsfile, 'r') as file:
        tags_data = json.load(file)

    # Convert json to object
# Convert the list of tags back to tag
    alltagslist = []
    for tag_data in tags_data:
        tag = Tag(tag_data['id'], tag_data['name'])
        alltagslist.append(tag)
    return alltagslist

def insert_author(conn, author):
    c = conn.cursor()
    c.execute("INSERT INTO Author (id, name, role, bio) VALUES (?, ?, ?, ?)",
              (author.id, author.name, author.role, author.bio))
    conn.commit()

def insert_post(conn, post):
    c = conn.cursor()
    c.execute("INSERT INTO Post (id, authorid, title, preview, content, created_utc) VALUES (?, ?, ?, ?, ?, ?)",
              (post.id, post.authorid, post.title, post.preview, post.content, post.created_utc))
    conn.commit()

def insert_comment(conn, comment):
    c = conn.cursor()
    c.execute("INSERT INTO Comment (id, postid, author, content, created_utc) VALUES (?, ?, ?, ?, ?)",
              (comment.id, comment.postid, comment.author, comment.content, comment.created_utc))
    conn.commit()

def insert_tag(conn, tag):
    c = conn.cursor()
    c.execute("INSERT INTO Tag (id, name) VALUES (?, ?)", (tag.id, tag.name))
    conn.commit()

def insert_post_tag(conn, postid, tagid):
    c = conn.cursor()
    c.execute("INSERT INTO PostTag (postid, tagid) VALUES (?, ?)", (postid, tagid))
    conn.commit()


#Front end post object contains comment list, DB post table does not
def injectseeddata(dbname):
    posts = get_posts()
    authors = get_authors()
    comments = get_comments()
    tags = get_tags()

    conn = sqlite3.connect(dbname)

    # Create a cursor object
    c = conn.cursor()

    # Create the authors table
    c.execute("""
    CREATE TABLE IF NOT EXISTS Author (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        role TEXT,
        bio TEXT
    );
    """)

    # Create the posts table
    c.execute("""
    CREATE TABLE IF NOT EXISTS Post (
        id INTEGER PRIMARY KEY,
        authorid INTEGER,
        title TEXT NOT NULL,
        preview TEXT,
        content TEXT NOT NULL,
        created_utc INTEGER NOT NULL,
        FOREIGN KEY (authorid) REFERENCES Author (id)
    );
    """)

        # Create the comments table
    c.execute("""
    CREATE TABLE IF NOT EXISTS Comment (
        id INTEGER PRIMARY KEY,
        postid INTEGER,
        author TEXT NOT NULL,
        content TEXT NOT NULL,
        created_utc INTEGER NOT NULL,
        FOREIGN KEY (postid) REFERENCES Post (id)
    );
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS Tag (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE
    );
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS PostTag (
        postid INTEGER,
        tagid INTEGER,
        PRIMARY KEY (postid, tagid),
        FOREIGN KEY (postid) REFERENCES Post (id),
        FOREIGN KEY (tagid) REFERENCES Tag (id)
    );
    """)

    # Insert authors, posts, and comments
    for author in authors:
        insert_author(conn, author)

    for post in posts:
        insert_post(conn, post)

    for comment in comments:
        insert_comment(conn, comment)

    for tag in tags:
        insert_tag(conn, tag)

    #Read and insert posttags
    with open(posttagsfile, 'r') as file:
        posttags_data = json.load(file)
    for posttag_data in posttags_data:
        insert_post_tag(conn, posttag_data['postid'], posttag_data['tagid'])

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    return True