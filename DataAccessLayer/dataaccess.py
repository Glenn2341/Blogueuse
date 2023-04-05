import sqlite3
from models.Post import Post
from models.Comment import Comment
from models.Author import Author
from models.Tag import Tag

dbname = 'blog.db'

# Get author(s) using author id or all authors if no id is provided
def get_authors(author_id=None):
    # Create a cursor
    c = sqlite3.connect(dbname).cursor()

    if author_id:
        # Execute a query to select the row from the Author table with the given author_id
        c.execute("SELECT id, name, role, bio FROM Author WHERE id=?", (author_id,))

        # Fetch the row as a tuple
        row = c.fetchone()

        # Return None if there's no row with the given author_id
        if row is None:
            return None

        # Create an Author object from the row and return it
        return Author(row[0], row[1], row[2], row[3])
    else:
        # Execute a query to select all rows from the Author table
        c.execute("SELECT id, name, role, bio FROM Author")

        # Fetch all rows as a list of tuples
        rows = c.fetchall()

        # Create Author objects from the rows and return them as a list
        return [Author(row[0], row[1], row[2], row[3]) for row in rows]


# Get post(s) using id or all posts if no id is provided
#Front end post object contains comment list, DB post table does not
def get_posts(post_id=None):
    # Create a cursor
    c = sqlite3.connect(dbname).cursor()

    if post_id:
        # Execute a query to select the row from the Post table with the given post_id
        c.execute("SELECT id, authorid, title, preview, content, created_utc FROM Post WHERE id=?", (post_id,))

        # Fetch the row as a tuple
        row = c.fetchone()

        # Return None if there's no row with the given post_id
        if row is None:
            return None

        # Create a Post object from the row and return it
        return Post(id=row[0], authorid=row[1], title=row[2], preview=row[3], content=row[4], created_utc=row[5], tags=None, comments=None, author=None)
    else:
        # Execute a query to select all rows from the Post table
        c.execute("SELECT id, authorid, title, preview, content, created_utc FROM Post")

        # Fetch all rows as a list of tuples
        rows = c.fetchall()

        # Create Post objects from the rows and return them as a list
        return [Post(id=row[0], authorid=row[1], title=row[2], preview=row[3], content=row[4], created_utc=row[5], tags=None, comments=None, author=None) for row in rows]


# Get comment(s) using id or all comments if no id is provided
def get_comments(comment_id=None):
    # Create a cursor
    c = sqlite3.connect(dbname).cursor()

    if comment_id:
        # Execute a query to select the row from the Comment table with the given comment_id
        c.execute("SELECT postid, id, author, content, created_utc FROM Comment WHERE id=?", (comment_id,))

        # Fetch the row as a tuple
        row = c.fetchone()

        # Return None if there's no row with the given comment_id
        if row is None:
            return None

        # Create a Comment object from the row and return it
        return Comment(row[0], row[1], row[2], row[3], row[4])
    else:
        # Execute a query to select all rows from the Comment table
        c.execute("SELECT postid, id, author, content, created_utc FROM Comment")

        # Fetch all rows as a list of tuples
        rows = c.fetchall()

        # Create Comment objects from the rows and return them as a list
        return [Comment(row[0], row[1], row[2], row[3], row[4]) for row in rows]


# Get tag(s) using id or all tags if no id is provided
def get_tags_by_id(tag_id=None):
    # Create a cursor
    c = sqlite3.connect(dbname).cursor()

    if tag_id:
        # Execute a query to select the row from the Tag table with the given tag_id
        c.execute("SELECT id, name FROM Tag WHERE id=?", (tag_id,))

        # Fetch the row as a tuple
        row = c.fetchone()

        # Return None if there's no row with the given tag_id
        if row is None:
            return None

        # Create a Tag object from the row and return it
        return Tag(row[0], row[1])
    else:
        # Execute a query to select all rows from the Tag table
        c.execute("SELECT id, name FROM Tag")

        # Fetch all rows as a list of tuples
        rows = c.fetchall()

        # Create Tag objects from the rows and return them as a list
        return [Tag(row[0], row[1]) for row in rows]
    

def get_comments_by_post_id(post_id):
    # Create a cursor
    c = sqlite3.connect(dbname).cursor()

    # Execute a query to select all rows from the Comment table with the given post_id
    c.execute("SELECT postid, id, author, content, created_utc FROM Comment WHERE postid=?", (post_id,))

    # Fetch all rows as a list of tuples
    rows = c.fetchall()

    # Create Comment objects from the rows and return them as a list
    return [Comment(row[0], row[1], row[2], row[3], row[4]) for row in rows]


def get_post_tags_by_tagid(tagid):
    # Create a cursor
    c = sqlite3.connect(dbname).cursor()

    # Execute a query to select all rows from the PostTag table with the given tagid
    c.execute("SELECT postid, tagid FROM PostTag WHERE tagid = ?", (tagid,))

    # Fetch all rows as a list of tuples
    rows = c.fetchall()

    # Create a dictionary with postid as the key and tagid as the value
    post_tags = [{'postid': row[0], 'tagid': row[1]} for row in rows]

    return post_tags


def get_post_tags_by_postid(postid):
    # Create a cursor
    c = sqlite3.connect(dbname).cursor()

    # Execute a query to select all rows from the PostTag table with the given postid
    c.execute("SELECT postid, tagid FROM PostTag WHERE postid = ?", (postid,))

    # Fetch all rows as a list of tuples
    rows = c.fetchall()

    # Create a dictionary with postid as the key and tagid as the value
    post_tags = [{'postid': row[0], 'tagid': row[1]} for row in rows]

    return post_tags


def get_posts_by_author_id(author_id):
    # Create a cursor
    c = sqlite3.connect(dbname).cursor()

    # Execute a query to select all rows from the Post table with the given author_id
    c.execute("SELECT id, authorid, title, preview, content, created_utc FROM Post WHERE authorid=?", (author_id,))

    # Fetch all rows as a list of tuples
    rows = c.fetchall()

    # Create Post objects from the rows and return them as a list
    return [Post(id=row[0], authorid=row[1], title=row[2], preview=row[3], content=row[4], created_utc=row[5], tags=None, comments=None, author=None) for row in rows]


def insert_comment(comment):
    # Create a connection and cursor
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    # Prepare the SQL query to insert the Comment object into the table
    query = '''
    INSERT INTO Comment (postid, author, content, created_utc) VALUES (?, ?, ?, ?)
    '''

    # Execute the query with the Comment object's attributes
    c.execute(query, (comment.postid, comment.author, comment.content, comment.created_utc))

    # Commit the transaction
    conn.commit()

    # Close the connection
    conn.close()


def remove_comment_by_id(comment_id):
    # Create a connection and cursor
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    # Execute the query to delete the comment with the given id
    c.execute("""
        DELETE FROM Comment
        WHERE id = ?
    """, (comment_id,))

    # Commit the changes to the database
    conn.commit()  # Call commit() on the connection object



def get_comments_since_date(timestamp):
    # Create a connection and cursor
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    # Query to get all comments made after the given date
    c.execute("SELECT * FROM Comment WHERE created_utc > ?", (timestamp,))

    # Fetch all rows from the result
    result = c.fetchall()

     # Convert the results into Comment objects
    comments = [Comment(postid=row[1], id=row[0], author=row[2], content=row[3], created_utc=row[4]) for row in result]

    return comments


def insert_post(post):
    # Connect to the database
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    # Insert post into the database
    c.execute("""
        INSERT INTO Post (authorid, title, preview, content, created_utc)
        VALUES (?, ?, ?, ?, ?);
    """, (post.authorid, post.title, post.preview, post.content, post.created_utc))

    # Get the ID of the post that was just created
    post_id = c.lastrowid

    # Commit the changes and close the connection
    conn.commit()

    # Return the post ID
    return post_id