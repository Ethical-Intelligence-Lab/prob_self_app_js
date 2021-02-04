import json
import os
import random
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

from .models import Participant

DEV_ENVIROMENT_BOOLEAN = True

if DEV_ENVIROMENT_BOOLEAN:
    AMAZON_HOST = "https://workersandbox.mturk.com/mturk/externalSubmit"
else:
    AMAZON_HOST = "https://www.mturk.com/mturk/externalSubmit"

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
    return redirect_to_less(request, render_data)

# redirect to user to a game that is less played
def redirect_to_less(request, render_data):
    logic_count = Participant.objects.filter(game_type="logic").count()
    contingency_count = Participant.objects.filter(game_type="contingency").count()

    rand = random.randint(0, 1)
    if logic_count == contingency_count:
        if rand == 0:
            return logic(request, render_data)
        else:
            return contingency(request, render_data)
    elif logic_count > contingency_count:
        return contingency(request, render_data)
    else:
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
    data = request.POST.get('data', None)
    worker_id = request.POST.get('workerId', None)
    game_type = request.POST.get("gameType")

    print("game finished, submitting to s3. ID: ", worker_id, " game type: ", game_type)

    from datetime import datetime
    dt = datetime.today().strftime('%Y-%m-%d=%H:%M:%S')

    aws_id = os.environ['AWS_ID']
    aws_secret_key = os.environ['AWS_SECRET_KEY']

    AWS_ACCESS_KEY = aws_id
    AWS_SECRET_KEY = aws_secret_key

    final_data = json.loads(data)

    final_data["self_locs"] = take_transpose(final_data["self_locs"])
    print(final_data["self_locs"])



    filename = game_type + "/" + dt + "_" + worker_id + ".json"

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
        "game_type": request.POST.get("gameType"),
    }

    save_into_db(context)

    return render(request, "game/finished.html", context)


def save_into_db(context):
    data = context["data"]
    assignment_id = context["assignment_id"]
    worker_id = context["worker_id"]
    hit_id = context["hit_id"]
    game_type = context["game_type"]

    participant = Participant(data=data, assignment_id=assignment_id, worker_id=worker_id, hit_id=hit_id, game_type=game_type)
    participant.save()

    print("Participant ", worker_id, " succesfully saved.")




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
