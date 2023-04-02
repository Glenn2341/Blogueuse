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


# Route for displaying a specific post and its comments
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

    # If the request is a POST, handle the comment form submission
    if request.method == 'POST':
        if form.validate_on_submit():
            comment = clean(form.comment.data)
            name = clean(form.name.data)

            newComment = Comment(postid=post_id, id=None, author=name, content=comment, created_utc=None)
            BusinessLogicLayer.businesslogic.save_comment(newComment)

            # Redirect the user back to the post page
            return redirect(url_for('post.show_post', post_id=post_id) + '#comment-form')

    # Render the full post template with the retrieved post data
    return render_template('/postdetail.html', post=selectedpost, form=form, spotlight_topic = spotlight['topic'].name, spotlight_posts = spotlight['posts'],  searchform = searchform)