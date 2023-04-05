from datetime import datetime, timedelta, timezone

from DataAccessLayer import dataaccess
from OAPI_query import OAPI_functions
import csv

moderation_record_file = 'moderation_record.csv'

#Attempt to get a moderation decision on a comment 
def attempt_moderation_decision(prompt):
    try:
        response = OAPI_functions.Query_OAPI(prompt)

        #get the decision after the colon and remove leading whitespace
        decision = response.split(':')[0].lstrip().lower()

        if(decision == 'toxic'):
            return 'toxic'
        elif(decision == 'spam'):
            return 'spam'
        elif(decision == 'acceptable'):
            return 'acceptable'
        print('failed to parse decision from ' + response)
        return None
    except Exception as e:
        print('Comment moderation attempt failed:')
        print(e)


#Delete unacceptable comments
def moderate_recent_comments(max_decisions):
    current_decisions = 0

    # Read the record CSV file
    with open(moderation_record_file, mode='r', newline='') as file:
        reader = csv.reader(file)

        # Read all the rows into a list
        rows = list(reader)

    # Get the last row
    last_moderation_check = int(rows[-1][0])
    dt_object = datetime.fromtimestamp(last_moderation_check)
    date = dt_object.date()

    comments = dataaccess.get_comments_since_date(last_moderation_check)
    print(f'last moderation sweep was {last_moderation_check} ({date}), {len(comments)} new comments' )

    moderation_query = 'Please diagnose this post as toxic, spam, or acceptable (output like acceptable:reason)\n\n'

    for comment in comments:
        decision = attempt_moderation_decision(moderation_query + comment.content)
        print(f'{decision}: {comment.content}\n')
        if(decision.lower() == 'toxic' or decision.lower() == 'spam'):
            dataaccess.remove_comment_by_id(comment.id)
        current_decisions += 1
        if(current_decisions >= max_decisions):          
            break

    current_time = int(datetime.now(timezone.utc).timestamp())
    # Open the record CSV file in append mode ('a') and write the data
    with open(moderation_record_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerow([current_time])

    return current_decisions


def perform_moderation_sweep(max_decisions = 256):
    result = moderate_recent_comments(max_decisions)
    if(result >= max_decisions):
        return 'moderation decision cap reached'
    else:
        return 'moderation complete'