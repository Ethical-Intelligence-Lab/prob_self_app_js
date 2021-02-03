import os
import boto3
from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion
from boto.mturk.qualification import Qualifications, PercentAssignmentsApprovedRequirement, NumberHitsApprovedRequirement
from boto.mturk.price import Price

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
    # 5 cents per HIT
    amount = 0.05

    # frame_height in pixels
    frame_height = 800

    # Here, I create two sample qualifications
    qualifications = Qualifications()
    qualifications.add(PercentAssignmentsApprovedRequirement(comparator="GreaterThan", integer_value="90"))
    qualifications.add(NumberHitsApprovedRequirement(comparator="GreaterThan", integer_value="100"))

    # This url will be the url of your application, with appropriate GET parameters
    url = "https://prob-self-mturk.herokuapp.com/"
    questionform = ExternalQuestion(url, frame_height)
    create_hit_result = client.create_hit(
        title="Prob Self",
        description="This is a description",
        keywords=["add", "some", "keywords"],
        # duration is in seconds
        duration= 60 * 60,
        # max_assignments will set the amount of independent copies of the task (turkers can only see one)
        max_assignments=1,
        question=questionform,
        reward=Price(amount=amount),
        # Determines information returned by method in API, not super important
        response_groups=('Minimal', 'HITDetail'),
        qualifications=qualifications,
    )

create_task(connect_mturk())