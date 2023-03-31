from models.Post import Post
from models.Comment import Comment
from models.Author import Author
from models.Tag import Tag
import DataAccessLayer.dataaccess
import datetime
import time

def populate_post_tags_and_author(post):
    tags = []
    posttags = DataAccessLayer.dataaccess.get_post_tags_by_postid(post.id)
    for posttag in posttags:
        tagid = int(posttag['tagid'])
        tag = DataAccessLayer.dataaccess.get_tags_by_id(tagid)
        tags.append(tag)
    post.addtags(tags)

    author = DataAccessLayer.dataaccess.get_authors(post.authorid)
    post.addauthor(author)


# get posts and insert relevant tags and authors
def getposts(id=None):
    posts = DataAccessLayer.dataaccess.get_posts(id)

    if(id):
        populate_post_tags_and_author(posts)   
    else:
        for post in posts:
            populate_post_tags_and_author(post)
  
    return posts


def get_posts_by_tag(tagid):
    posttags = DataAccessLayer.dataaccess.get_post_tags_by_tagid(tagid)
    posts = []

    for posttag in posttags:
        postid = int(posttag['postid'])
        post = getposts(postid)
        posts.append(post)

    return posts


def getauthors(id=None):
    return DataAccessLayer.dataaccess.get_authors(id)


def get_comments_by_post_id(post_id):
    comments = DataAccessLayer.dataaccess.get_comments_by_post_id(post_id)

    #sort by time
    sorted_comments = sorted(comments, key=lambda c: c.created_utc, reverse=True)

    return sorted_comments


def gettags(tagid=None):
    return DataAccessLayer.dataaccess.get_tags_by_id(tagid)


def save_comment(comment):
    if((comment.author is None) or len(comment.author) == 0):
        comment.addname('Anonymous')

    # get the current date and time in UTC
    now = datetime.datetime.now(datetime.timezone.utc)

    # convert the datetime object to a Unix timestamp
    unix_time = int(now.timestamp())

    comment.created_utc = unix_time

    DataAccessLayer.dataaccess.insert_comment(comment)


#todo- calling populate_post_tags_and_author shouldn't be necessary here
def post_search(querystring):
    #Get all authors and tags
    allauthors = [author for author in getauthors()]
    alltags = [tag for tag in gettags()]

    #Get the authors and tags being searched for
    authorsearch = set()
    tagsearch = set()

    for author in allauthors:
        if(author.name in querystring):
            authorsearch.add(author)
            querystring = querystring.replace(author.name, '')
    querytagtokens = querystring.split(' ')

    for tag in alltags:
        if(tag.name in querytagtokens):
            tagsearch.add(tag)

    # if no author or tags found, return empty
    if((len(authorsearch) == 0) and (len(tagsearch) == 0)):
        return []
    
    # if author is found
    # find articles by the given authors, then filter based on tag
    if(len(authorsearch) > 0):
        postlist = []
        for author in authorsearch:
            authorposts = DataAccessLayer.dataaccess.get_posts_by_author_id(author.id)
            postlist.extend(authorposts)

        #populate the posts with tags and author
        for post in postlist:
            populate_post_tags_and_author(post)

        if(len(tagsearch) > 0):
            tagfilteredposts = []
            tagsearchnames = [tag.name for tag in tagsearch]
            for post in postlist:
                for tag in post.tags:
                    if(tag.name in tagsearchnames):
                        tagfilteredposts.append(post)
                        break
            postlist = tagfilteredposts

        
        return postlist
    
    #if tags were given but no author, get post IDs from posttag table
    # post tag and author population is done by get_posts_by_tag
    postlist = []
    post_id_list = []
    tag_id_list = [tag.id for tag in tagsearch]
    for tag_id in tag_id_list:
        posts = get_posts_by_tag(tag_id)
        for post in posts:
            if(post.id not in post_id_list):
                post_id_list.append(post.id)
                postlist.append(post)
    return postlist

