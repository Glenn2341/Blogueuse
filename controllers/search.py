from flask import Flask, abort, render_template, request, redirect, url_for, Blueprint
from models.Post import Post
from models.Comment import Comment
from models.Author import Author
from models.Tag import Tag
from forms import SearchForm
from controllers.home import get_spotlight_posts
import BusinessLogicLayer.businesslogic
import random

search_blueprint = Blueprint('search', __name__)


@search_blueprint.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()

    # get sidebar resources
    sidebar_searchform = SearchForm()
    spotlight = get_spotlight_posts()

    search_query = form.query.data
    if(search_query is None):
        search_query = ''

    if form.validate_on_submit():

        # Find a list of posts relevant to the search
        filteredposts = BusinessLogicLayer.businesslogic.post_search(search_query)

        return render_template('/postsearch.html', posts=filteredposts, originalsearch=search_query, form=form, spotlight_topic = spotlight['topic'].name, spotlight_posts = spotlight['posts'],  searchform = sidebar_searchform)

    return render_template('/postsearch.html', posts=[], originalsearch=search_query, form=form, spotlight_topic = spotlight['topic'].name, spotlight_posts = spotlight['posts'],  searchform = sidebar_searchform)





# @search_blueprint.route('/search')
# def search():
#     # Retrieve the search query from the URL parameters
#     search_query = request.args.get('query', '')

#     #Find a list of posts releveant to the search
#     filteredposts = BusinessLogicLayer.businesslogic.post_search(search_query)

#     return render_template('/postsearch.html', posts=filteredposts, originalsearch = search_query)
