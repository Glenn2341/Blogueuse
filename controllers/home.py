from flask import Flask, abort, render_template, request, redirect, url_for, Blueprint
from models.Post import Post
from models.Comment import Comment
from models.Author import Author
from models.Tag import Tag
from forms import EmailForm
from forms import SearchForm
import BusinessLogicLayer.businesslogic
import random
import bleach


home_blueprint = Blueprint('home', __name__)

def get_spotlight_posts():
    topics = BusinessLogicLayer.businesslogic.gettags()
    topic_names = [topic.name for topic in topics]
    spotlight = random.sample(topics, 1)[0]
    spotlightposts = BusinessLogicLayer.businesslogic.get_posts_by_tag(spotlight.id)

    if(len(spotlightposts) > 3):
        spotlightposts = random.sample(spotlightposts, 3)

    return {'topic': spotlight, 'posts': spotlightposts}                        


@home_blueprint.route('/index')
def index():
    searchform = SearchForm()

    # Retrieve the list of posts from the database
    posts = BusinessLogicLayer.businesslogic.getposts()

    topics = BusinessLogicLayer.businesslogic.gettags()
    topic_names = [topic.name for topic in topics]
    spotlight = random.sample(topics, 1)[0]
    spotlightposts = BusinessLogicLayer.businesslogic.get_posts_by_tag(spotlight.id)

    if(len(spotlightposts) > 3):
        spotlightposts = random.sample(spotlightposts, 3)

    # Pass the list of posts to the view for rendering
    return render_template('/index.html', posts=posts, topic_selection = topic_names, spotlight_posts = spotlightposts, spotlight_topic = spotlight.name, searchform=searchform)


@home_blueprint.route('/about')
def about():
    authors = BusinessLogicLayer.businesslogic.getauthors()

    searchform = SearchForm()
    spotlight = get_spotlight_posts()

    # Pass the list of posts to the view for rendering
    return render_template('/about.html', authors=authors, spotlight_topic = spotlight['topic'].name, spotlight_posts = spotlight['posts'],  searchform = searchform)


@home_blueprint.route('/mailinglist', methods=['GET', 'POST'])
def mailinglist():
    form = EmailForm()

    searchform = SearchForm()
    spotlight = get_spotlight_posts()

    if form.validate_on_submit():
        # Clean the email input
        email = bleach.clean(form.email.data)

        # Process the email here (e.g., add it to the mailing list)

        # Redirect to a success page or the mailing list page
        return redirect(url_for('home.mailinglist'))

    return render_template('/mailinglist.html', form=form, spotlight_topic = spotlight['topic'].name, spotlight_posts = spotlight['posts'],  searchform = searchform)



# @home_blueprint.route('/emailsubmit', methods=['GET', 'POST'])
# def email_submit():
#     form = EmailForm()

#     if form.validate_on_submit():
#         # Clean the email input
#         email = bleach.clean(form.email.data)

#         # Process the email here (e.g., add it to the mailing list)

#         # Redirect to a success page or the mailing list page
#         return redirect(url_for('home.mailing_list'))
    
#     # Render the form with validation errors if the form is not valid
#     return render_template('/email_form.html', form=form)


@home_blueprint.route('/generic')
def generic():

    return render_template('/generic.html')

# @home_blueprint.route('/')
# def index():
#     return 'Hello, world! Blogueuse'