import json
import os
import random
import secrets
import string
from copy import deepcopy

import boto3
from botocore.exceptions import ClientError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Participant, Demographics
from .forms import DemographicsForm
from datetime import datetime

DEV_ENVIROMENT_BOOLEAN = True

if DEV_ENVIROMENT_BOOLEAN:
    AMAZON_HOST = "https://workersandbox.mturk.com/mturk/externalSubmit"
else:
    AMAZON_HOST = "https://www.mturk.com/mturk/externalSubmit"


@csrf_exempt
def home(request):
    # Check if this user has completed before
    if Participant.objects.filter(worker_id=request.GET.get("workerId")).exists():
        return HttpResponse("You cannot attend this experiment more than once.")

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
#    else:
#       return HttpResponse("404")

    '''
    We're creating a dict with which we'll render our template page.html
    Note we are grabbing GET Parameters
    In this case, I'm using someInfoToPass as a sample parameter to pass information
    '''

    r = random.randint(0, 99999)

    render_data = {
        "worker_id": request.GET.get("workerId") if request.GET.get("workerId") is not None else r,
        "assignment_id": request.GET.get("assignmentId") if request.GET.get("assignmentId") is not None else r,
        "amazon_host": AMAZON_HOST,
        "hit_id": request.GET.get("hitId") if request.GET.get("assignmentId") is not None else r,
    }

    participant = Participant(assignment_id=render_data['assignment_id'], worker_id=render_data['worker_id'],
                              hit_id=render_data['hit_id'], )
    participant.save()
    print("render data: ", render_data)

    # This is particularly nasty gotcha.
    # Without this header, your iFrame will not render in Amazon
    # resp.headers['x-frame-options'] = 'this_can_be_anything'

    # based on data, redirect to game type
    return redirect_to_less(request, render_data)


# redirect to user to a game that is less played
def redirect_to_less(request, render_data):
    game_list = ["logic", "contingency", "change_agent"]
    counts = []
    for game in game_list:
        counts.append(Participant.objects.filter(game_type=game).count())

    # index = min(enumerate(counts), key=itemgetter(1))[0]
    # return globals()[game_list[index]](request, render_data)

    # Do logic only for now
    return pre_game(request, render_data)


# Show the consent form
@csrf_exempt
def pre_game(request, context):
    print("in pre game: ", context)
    return render(request, "game/pre_game.html", context)


# Demographics
@csrf_exempt
def post_game(request, worker_id, assignment_id, hit_id):
    print("In post game")
    context = {}
    if request.method == "GET":
        context['form'] = DemographicsForm(
            initial={'worker_id': worker_id, 'assignment_id': assignment_id,
                     'hit_id': hit_id})

        print("Post game (GET): ------ ---  ", context)
        return render(request, "game/post_game.html", context)
    else:
        context = request.POST.dict()
        print("Post game (POST): ------ ---  ", context)
        context = request.POST.dict()

        # Save demographics
        new_demographics = Demographics(participant=Participant.objects.get(worker_id=context['worker_id']),
                                        ethnicity=context['ethnicity'],
                                        gender=context['gender'],
                                        age=context['age'],
                                        game_exp=context['game_exp'],
                                        edu=context['edu'])
        new_demographics.save()

        print("Demographics saved!")

        return render(request, "game/finished.html", context)


@csrf_exempt
def logic(request):
    context = request.GET.dict()
    print("in logic game: ", context)
    return render(request, "game/logic_game.html", context)


@csrf_exempt
def contingency(request, context):
    return render(request, "game/contingency_game.html", context)


@csrf_exempt
def change_agent(request, context):
    return render(request, "game/change_agent_game.html", context)


def generate_id():
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(20))  # Form a 20-character password
    return password


@csrf_exempt
def game_finished(request):
    data = request.POST.get('data', None)
    worker_id = request.POST.get('workerId', None)
    game_type = request.POST.get("gameType")

    print("in game finished: ", request.POST)

    print("Game finished, submitting to s3. ID: ", worker_id, " - Game type: ", game_type)

    dt = datetime.today().strftime('%Y-%m-%d=%H:%M:%S')

    AWS_ACCESS_KEY = os.environ['AWS_ID']
    AWS_SECRET_KEY = os.environ['AWS_SECRET_KEY']

    final_data = json.loads(data)

    final_data["data"]["self_locs"] = take_transpose(final_data["data"]["self_locs"])
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

    print(context)

    save_into_db(context)

    # Show demographics
    return redirect('/post_game/{}/{}/{}/'.format(context['worker_id'], context['assignment_id'], context['hit_id']), permanent=True)


def save_into_db(context):
    data = context["data"]
    worker_id = context["worker_id"]
    game_type = context["game_type"]

    participant = Participant.objects.get(worker_id=worker_id)
    participant.data = data
    participant.game_type = game_type
    participant.finished_game = True
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
