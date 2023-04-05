import datetime

from models import Comment
from OAPI_query import OAPI_functions

def attempt_comment_generation(prompt, post):
    try:
        response = OAPI_functions.Query_OAPI(prompt).split(':')

        #remove @ that may be inserted before name and remove leading whitespace
        author = response[0].replace('@', '').lstrip()
        comment = response[1].lstrip()

        created_utc = int((datetime.datetime.now(datetime.timezone.utc)).timestamp())
        final_comment = Comment.Comment(postid=None, id = None, author = author, content = comment, created_utc=created_utc)
        return final_comment
    except Exception as e:
        print('Comment gen attempt failed:')
        print(e)

def generate_comments(post, numcomments):
    comments = []
    comment_query_base = 'Given this post, please write one comment (output like username:comment) \n' + post.content
    max_acceptable_failures = 3
    current_failures = 0

    while((len(comments) < numcomments) and current_failures < max_acceptable_failures):
        if(len(comments)) > 0:
            comment_query = comment_query_base + comments[-1].author + ': ' + comments[-1].content
        else:
            comment_query = comment_query_base

        comment = attempt_comment_generation(comment_query, post)
        if(comment is not None):
            comments.append(comment)
        else:
            current_failures += 1


    return comments