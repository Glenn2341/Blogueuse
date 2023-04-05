import os
import sys
import openai

# Add the parent directory to the Python path
parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_directory)

# Change the current working directory to the parent directory
os.chdir(parent_directory)

from DataAccessLayer import dataaccess
from content_generation import image_generation
from content_generation import comment_generation
from content_generation import post_generation
from content_moderation import comment_moderation

blogueuse_path_images_small = parent_directory + '/static/images/posts_small/'
blogueuse_path_images_wide = parent_directory + '/static/images/posts_large/'

openai.api_key = os.getenv("OPENAI_API_KEY")
stable_diffusion_API_key = os.getenv("STABLE_DIFFUSION_API_KEY")


#generate and save content
def generate_post_and_comments():
    post = post_generation.generate_post()
    if (post is not None):
        comments = comment_generation.generate_comments(post, 2)
        if (comments):
            postid = dataaccess.insert_post(post)
            post.id = postid
            for comment in comments:
                comment.postid = post.id
                dataaccess.insert_comment(comment)
                print(f'saving comment by {comment.author}: {comment.content}')
            return post
    return False


def regen_post_image(command):
    command = command.split(' ')
    target_post_id = int(command[1])

    targetpost = dataaccess.get_posts(target_post_id)
    
    image_generation.generate_images(post=targetpost, api_key=stable_diffusion_API_key, savepath_small=blogueuse_path_images_small, savepath_large=blogueuse_path_images_wide)

    return 'image regenerated'


#Possible arguments:
#regen_image postid
#moderate
def main(args=None):
    # handle command line arguments
    if (args):
        if (args and args.startswith('regen_image')):
            return regen_post_image(args)
        elif(args and args == 'moderate'):
            return comment_moderation.perform_moderation_sweep()
        else:
            return 'command not recognized'
    

    #generate post and images
    newpost = generate_post_and_comments()
    image_generation.generate_images(post=newpost, api_key=stable_diffusion_API_key, savepath_small=blogueuse_path_images_small, savepath_large=blogueuse_path_images_wide)
    return 'generation complete'


#From powershell, 'python gupta.py'
if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(args=' '.join(sys.argv[1:]))
    else:
        main()