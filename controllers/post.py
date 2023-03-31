from flask import Flask, abort, render_template, request, redirect, url_for, Blueprint
from bleach import clean
from models.Post import Post
from models.Comment import Comment
from models.Author import Author
from models.Tag import Tag
from forms import CommentForm
from forms import SearchForm
from controllers.home import get_spotlight_posts
import BusinessLogicLayer.businesslogic
import random


post_blueprint = Blueprint('post', __name__)

@post_blueprint.route('/posts/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    form = CommentForm()
    form.post_id.data = post_id

    # get sidebar resources
    searchform = SearchForm()
    spotlight = get_spotlight_posts()

    # Retrieve the post with the given ID
    selectedpost = BusinessLogicLayer.businesslogic.getposts(post_id)

    if not selectedpost:
        abort(404, "Sorry, we couldn't find the post you requested.")

    comments = BusinessLogicLayer.businesslogic.get_comments_by_post_id(post_id)
    selectedpost.addcomments(comments)

    if request.method == 'POST':
        if form.validate_on_submit():
            comment = clean(form.comment.data)
            name = clean(form.name.data)

            newComment = Comment(postid=post_id, id=None, author=name, content=comment, created_utc=None)
            BusinessLogicLayer.businesslogic.save_comment(newComment)

            # Redirect the user back to the post page
            return redirect(url_for('post.show_post', post_id=post_id))

    # Render the full post template with the retrieved post data
    return render_template('/postdetail.html', post=selectedpost, form=form, spotlight_topic = spotlight['topic'].name, spotlight_posts = spotlight['posts'],  searchform = searchform)


















# # show a post with a given ID
# @post_blueprint.route('/posts/<int:post_id>')
# def show_post(post_id):
#     form = CommentForm()
#     form.post_id.data = post_id  

#     # Retrieve the post with the given ID 
#     selectedpost = BusinessLogicLayer.businesslogic.getposts(post_id)

#     if not selectedpost:
#         abort(404, "Sorry, we couldn't find the post you requested.")

#     comments = BusinessLogicLayer.businesslogic.get_comments_by_post_id(post_id)
#     selectedpost.addcomments(comments)

#     # Render the full post template with the retrieved post data
#     return render_template('/postdetail.html', post=selectedpost, form=form)


# @post_blueprint.route('/submit_comment', methods=['POST'])
# def submit_comment():  

#     form = CommentForm(request.form)
#     #form.comment.data = 'aaaaaaaaaaaaaaaaaaaaaaaaaa'

#     #validate and clean input
#     if form.validate():
#         post_id = int(request.form['post_id'])
#         comment = clean(form.comment.data)
#         name = clean(form.name.data)
    
#         newComment = Comment(postid = post_id, id=None, author=name, content=comment, created_utc=None)
#         BusinessLogicLayer.businesslogic.save_comment(newComment)

#         # Redirect the user back to the post page
#         return redirect(url_for('post.show_post', post_id=post_id))
#     else:
#         # If the form is not valid, render the comment form again with the validation errors
#         return render_template('post.show_post', form=form)

def process_comment(a, b, v):
    return True






@post_blueprint.route('/comment')
def comment():
    form = CommentForm()
    form.post_id.data = 1  # Set the post_id value
    return render_template('commentbox.html', form=form)

@post_blueprint.route('/submit_comment_basic', methods=['POST'])
def submit_comment_basic():
    form = CommentForm(request.form)
    form.comment.data = 'aaaaaaaaaaaaaaaaaaaaaaaaaa'
    #form.name.data = 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbb'

    if form.validate():
        # If the form is valid, process the comment
        process_comment(form.post_id.data, form.comment.data, form.name.data)
        return redirect(url_for('post.comment'))
    # If the form is not valid, render the comment form again with the validation errors
    return render_template('commentbox.html', form=form)





@post_blueprint.route('/posts')
def list_posts():
    # Retrieve the list of posts from the database
    posts = BusinessLogicLayer.businesslogic.getposts()

    # Pass the list of posts to the view for rendering
    return render_template('/posts.html', posts=posts)