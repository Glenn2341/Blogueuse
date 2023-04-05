import re
import random
import time
import datetime

from models import Post
from DataAccessLayer import dataaccess
from OAPI_query import OAPI_functions

test_post = '''Maximizing Your Earnings as a Dog Walker: Tips and Tricks\n\nAs a dog walker, you love spending time with your furry clients and taking them on walks. It\'s a fun and rewarding job, but it can also be challenging to make a good income. In this post, we\'ll share some tips and tricks on how to maximize your earnings as a dog walker.\n\n1. Set Competitive Rates\n\nFirst and foremost, make sure your rates are competitive with other dog walkers in your area. Research what other dog walkers are charging and adjust your rates accordingly. Don\'t undervalue your services, but make sure you\'re not overcharging either. Your pricing should reflect your level of experience, the length of the walks, and the number of dogs you\'re walking at once.\n\n2. Offer Additional Services\n\nOffering additional services can help increase your earnings. You could offer dog grooming, pet sitting, or house-sitting services. Many clients prefer to have one reliable pet care provider, so offering additional services can help build trust and loyalty with your clients.\n\n3. Build a Regular Client Base\n\nBuilding a regular client base is one of the most important ways to maximize your earnings. Regular clients provide consistent income and are more likely to recommend your services to others. Make sure to provide excellent customer service and go above and beyond for your clients.\n\n4. Utilize Technology\n\nUsing technology can streamline your business and make it easier to manage clients and schedules. There are many apps and websites that can help you manage your bookings, payments, and communications with clients.\n\n5. Market Yourself\n\nMarketing is essential to growing your dog walking business. Invest in creating a professional website, business cards, and flyers. Social media is also an excellent tool for marketing your services. Share photos and testimonials from happy clients to show potential clients the quality of your work.\n\nBy following these tips and tricks, you can maximize your earnings as a dog walker and build a successful business. Remember to always provide excellent customer service and go above and beyond for your furry clients. Happy walking!'''

# As an AI language model, I can't submit an article to this blog blah blah
def trim_preface(post):
    pattern = r'(.*?)\n'
    match = re.search(pattern, post)
    if match:
        first_paragraph = match.group(1)
        if(('as an ai language model, i') in first_paragraph.lower()):
            return post.replace(first_paragraph, '').lstrip('\n')
        else:
            return post


#Generate the query used to designate the topic, and send
def get_post_topic_designation(topics, post):
    topic_designation_query = 'Please assign the following article to one of these topics (output like Yoga: reason) '
    for topic in topics:
        topic_designation_query += topic.name + ','
        topic_designation_query = topic_designation_query[:-1]
    topic_designation_query += '\n\n' + post

    max_tries = 3
    current_tries = 0
    while(current_tries < max_tries):
        response = OAPI_functions.Query_OAPI(topic_designation_query)
        #print('response ' + response)
        response_parsed = response.split(":")[0]
        for topic in topics:
            if(topic.name.lower() == response_parsed.lower()):
                return topic
        current_tries += 1 
    return None



def get_first_n_sentences(input_text, n=3):
    # Split the input text into sentences
    sentences = re.split(r'(?<=[.!?])\s+', input_text)

    # Get the first n sentences
    first_n_sentences = sentences[:n]

    # Join the sentences and return the result
    return ' '.join(first_n_sentences)


#Attempt to generate and return a post, return None if generation fails
def generation_attempt():
    # Pick an author at random
    authors = dataaccess.get_authors()
    author_choice = random.choice(authors)
    author_posts = dataaccess.get_posts_by_author_id(author_choice.id)

    #Generate the query used to write the post, and send
    post_write_query = ''
    for post in author_posts:
        post_write_query += post.title + f' by {author_choice.name}\n'
    post_write_query += f"\nPlease pretend you are {author_choice.name} and write their next blog post (start with a title and then write the post)"
    print(post_write_query)

    #Call OAPI to write the post
    post = OAPI_functions.Query_OAPI(post_write_query)
    print('\n================\n' + post + '\n=================\n')
    #post = test_post
    post = trim_preface(post)

    #Get the title
    pattern = r'(.*?)\n'
    match = re.search(pattern, post)
    if match:
        post_title = match.group(1)
        full_title_length = len(post_title)
        if(post_title.startswith('Title: ')):
            post_title = post_title[7:]
        if(post_title.endswith(',')):
            post_title = post_title[:-1]

    post = post[full_title_length:].lstrip()  # Remove the title from the post
    topics = dataaccess.get_tags_by_id()

    #Call OAPI to calssify the post
    topic = get_post_topic_designation(topics, post)
    #topic = topics[0]
    if topic is None or post is None or post_title is None or (len(post) < 256) or (len(post_title) == 0):
        return None

    #Make the preview
    preview = get_first_n_sentences(post, n=3)
    preview = preview.replace('\n', '')

    created_utc = int((datetime.datetime.now(datetime.timezone.utc)).timestamp())
    final_post = Post.Post(authorid = author_choice.id, id = None, title = post_title, author = author_choice.name, tags = [topic], preview = preview, content= post, comments=None, created_utc=created_utc)

    return final_post


def generate_post():
     max_tries = 3
     current_tries = 0
     while(current_tries < max_tries):
         post = generation_attempt()
         if post is not None:
            print('post generation successful')
            return post
         current_tries += 1
         print(f'post generation failed, attempt ({current_tries}/{max_tries})')
     return None