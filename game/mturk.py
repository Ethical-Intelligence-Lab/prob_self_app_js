import os
from datetime import datetime

import boto3

from boto.mturk.question import ExternalQuestion

def connect_mturk():
    region_name = 'us-east-1'
    aws_access_key_id = "AKIAQRC5SDWI2LGSKC46" #os.environ['AWS_MTURK_ID']
    aws_secret_access_key = "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" #os.environ['AWS_MTURK_KEY']

    endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

    # Uncomment this line to use in production
    # endpoint_url = 'https://mturk-requester.us-east-1.amazonaws.com'


    client = boto3.client(
        'mturk',
        endpoint_url=endpoint_url,
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    # This will return $10,000.00 in the MTurk Developer Sandbox
    print(client.get_account_balance()['AvailableBalance'])
    return client


def create_task(client):
    question = ExternalQuestion("https://prob-self-mturk.herokuapp.com/", frame_height=600)
    new_hit = client.create_hit(
        Title='Finish the game.',
        Description='Move with WASD or arrow keys.',
        Keywords='question, answer, research, game',
        Reward='0.15',
        MaxAssignments=1,
        LifetimeInSeconds=172800,
        AssignmentDurationInSeconds=1200,
        AutoApprovalDelayInSeconds=14400,
        Question=question.get_as_xml(),  # <--- this does the trick
    )
    print( "HITID = " + new_hit['HIT']['HITId'] )

def delete_hits(mturk):
    # Delete HITs
    for item in mturk.list_hits()['HITs']:
        hit_id = item['HITId']
        print('HITId:', hit_id)

        # Get HIT status
        status = mturk.get_hit(HITId=hit_id)['HIT']['HITStatus']
        print('HITStatus:', status)

        # If HIT is active then set it to expire immediately
        if status == 'Assignable':
            response = mturk.update_expiration_for_hit(
                HITId=hit_id,
                ExpireAt=datetime(2015, 1, 1)
            )

            # Delete the HIT
        try:
            mturk.delete_hit(HITId=hit_id)
        except:
            print('Not deleted')
        else:
            print('Deleted')

create_task(connect_mturk())
#delete_hits(connect_mturk())