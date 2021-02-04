import json
import os
import secrets
import string
from copy import deepcopy

import boto3
import numpy as np
from botocore.exceptions import ClientError
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from game.mturk import connect_mturk

DEV_ENVIROMENT_BOOLEAN = True

if DEV_ENVIROMENT_BOOLEAN:
    AMAZON_HOST = "https://workersandbox.mturk.com/mturk/externalSubmit"
else:
    AMAZON_HOST = "https://www.mturk.com/mturk/externalSubmit"

"""
@csrf_exempt
def approve_assignment(request):

    worker_id = request.POST.get("workerId")
    assignment_id = request.POST.get("assignmentId")
    amazon_host = AMAZON_HOST
    hit_id = request.POST.get("hitId")

    client = connect_mturk()
    response = client.approve_assignment(
        AssignmentId=assignment_id,
        RequesterFeedback='Submitted',
        #OverrideRejection=True | False
    )

    return render(HttpResponse("Your results are submitted. Thank you for your contribution!"))
"""



@csrf_exempt
def home(request):

    # The following code segment can be used to check if the turker has accepted the task yet
    if request.GET.get("assignmentId") == "ASSIGNMENT_ID_NOT_AVAILABLE":
        # Our worker hasn't accepted the HIT (task) yet
        pass
        print("You should accept the task to see the game")
        return HttpResponse("You should accept the task to see the game")
    elif request.GET.get("assignmentId") is not None:
        # Our worker accepted the task
        print("Task accepted")
        pass
    else:
        return HttpResponse("404")

    '''
    We're creating a dict with which we'll render our template page.html
    Note we are grabbing GET Parameters
    In this case, I'm using someInfoToPass as a sample parameter to pass information
    '''
    render_data = {
        "worker_id": request.GET.get("workerId"),
        "assignment_id": request.GET.get("assignmentId"),
        "amazon_host": AMAZON_HOST,
        "hit_id": request.GET.get("hitId"),
        "some_info_to_pass": request.GET.get("someInfoToPass")
    }

    print("render data: ", render_data)

    # This is particularly nasty gotcha.
    # Without this header, your iFrame will not render in Amazon
    #resp.headers['x-frame-options'] = 'this_can_be_anything'

    # based on data, redirect to game type
    return logic(request, render_data)

# Create your views here.
@csrf_exempt
def logic(request, context):
    #context = {}
    return render(request, "game/logic_game.html", context)

@csrf_exempt
def contingency(request, context):
    #context = {}
    return render(request, "game/contingency_game.html", context)

def generate_id():
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(20))  # Form a 20-character password
    return password

@csrf_exempt
def game_finished(request):
    print("game finished, submitting to s3")
    data = request.POST.get('data', None)
    worker_id = request.POST.get('workerId', None)

    from datetime import datetime
    dt = datetime.today().strftime('%Y-%m-%d=%H:%M:%S')

    aws_id = os.environ['AWS_ID']
    aws_secret_key = os.environ['AWS_SECRET_KEY']

    AWS_ACCESS_KEY = aws_id
    AWS_SECRET_KEY = aws_secret_key

    final_data = json.loads(data)

    final_data["self_locs"] = take_transpose(final_data["self_locs"])
    print(final_data["self_locs"])

    filename = dt + "_" + worker_id + ".json"

    print("writing ", filename)

    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY
        )

        body = json.dumps(final_data).encode()
        s3.put_object(Body=body, Bucket='prob-self-data-us', Key=filename)

    except ClientError as e:
        print("Client error.")
        # with open(filename, 'w') as f:
        #    json.dump(final_data, f)


    context = {
        "data": request.POST.get("data"),
        "assignment_id": request.POST.get("assignmentId"),
        "worker_id": request.POST.get("workerId"),
        "hit_id": request.POST.get("hitId"),

    }
    return render(request, "game/finished.html", context)

def take_transpose(list):
    levels = []
    for i in range(len(list)):  # each level
        x = []
        y = []
        for j in range(len(list[i])):  # each state
            x.append(list[i][j][0])
            y.append(list[i][j][1])

        level = [deepcopy(x), deepcopy(y)]
        levels.append(deepcopy(level))
    return levels
