import json
import os
import secrets
import string
from copy import deepcopy
from django.utils import timezone

import boto3
from botocore.exceptions import ClientError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Participant, Demographics
from .forms import DemographicsForm, EnterWorkerIdForm, EnterCompletionCodeForm
from datetime import datetime


def home(request):
    # Check if this user has completed before
    if request.method == 'GET':
        context = {}
        context['form'] = EnterWorkerIdForm()
        return render(request, "game/enter_mturk.html", context)
    if request.method == 'POST':
        worker_id = request.POST.get('worker_id')
        request.session['worker_id'] = worker_id

        if worker_id is None:
            return redirect('cannot_attend')

        # Participant does not exist
        if not Participant.objects.filter(worker_id=worker_id).exists():
            return redirect('cannot_attend')

        # Participant has completed the game before
        p = Participant.objects.get(worker_id=worker_id)
        if p.finished_game:
            return redirect('cannot_attend')

        # based on data, redirect to game type
        return redirect_to_less(request)


def register_participant(request, worker_id):
    try:
        participant = Participant(worker_id=worker_id)
        participant.save()
    except:
        return HttpResponse("False")
    return HttpResponse("True")

def finished_survey(request, worker_id):
    if not Participant.objects.filter(worker_id=worker_id).exists():
        return HttpResponse("False")

    participant = Participant.objects.get(worker_id=worker_id)
    participant.finished_survey = True
    participant.save()
    return HttpResponse("True")

# redirect to user to a game that is less played
def redirect_to_less(request):
    print("in redirect to less, ", request.session.get("worker_id"))
    game_list = ["logic", "contingency", "change_agent"]
    counts = []
    for game in game_list:
        counts.append(Participant.objects.filter(game_type=game).count())

    # index = min(enumerate(counts), key=itemgetter(1))[0]
    # return globals()[game_list[index]](request, render_data)

    # Do logic only for now
    return redirect('contingency')


# Show the consent form
def pre_game(request):
    worker_id = request.session.get('worker_id')
    if worker_id is None:
        return HttpResponse("No worker id")

    if request.method == "GET":
        context = {'worker_id': worker_id}
        return render(request, "game/pre_game.html", context)
    else:
        worker_id = request.POST.get('worker_id')
        if worker_id is None:
            return HttpResponse("No worker id")
        return redirect("logic")


"""
# Demographics
def demographics(request):
    worker_id = request.session.get('worker_id')
    context = {}
    if request.method == "GET":
        context['form'] = DemographicsForm(
            initial={'worker_id': worker_id})

        print("Post game (GET): ------ ---  ", context)
        return render(request, "game/demographics.html", context)
    else:
        context = request.POST.dict()
        print("Post game (POST): ------ ---  ", context)

        # Save demographics
        new_demographics = Demographics(participant=Participant.objects.get(worker_id=context['worker_id']),
                                        ethnicity=context['ethnicity'],
                                        gender=context['gender'],
                                        age=context['age'],
                                        game_exp=context['game_exp'],
                                        edu=context['edu'])
        new_demographics.save()

        participant = Participant.objects.get(worker_id=worker_id)
        participant.submitted_demographics = True
        participant.save()

        print("Demographics saved {}".format(worker_id))

        return redirect("completion")

"""


def completion(request):
    worker_id = request.session.get('worker_id')
    context = {}
    if request.method == "GET":
        context['form'] = EnterCompletionCodeForm()
        print("Post game (GET): ------ ---  ", context)
        return render(request, "game/completion.html", context)
    else:
        completion_code = request.POST.get('completion_code')
        p = Participant.objects.get(worker_id=worker_id)
        p.completion_code = completion_code
        request.session['completion_code'] = completion_code
        p.save()
        return redirect("success")


def success(request):
    worker_id = request.session.get('worker_id')
    completion_code = request.session.get('completion_code')

    return render(request, "game/success.html", {'worker_id': worker_id, 'completion_code': completion_code})


def cannot_attend(request):
    worker_id = request.session.get('worker_id')

    return render(request, "game/cannot_attend.html", {'worker_id': worker_id})


def logic(request):
    worker_id = request.session.get('worker_id')
    if worker_id is None:
        return render(request, "game/cannot_attend.html", {'worker_id': worker_id})

    # Participant does not exist
    if not Participant.objects.filter(worker_id=worker_id).exists():
        return redirect('cannot_attend')

    p = Participant.objects.get(worker_id=worker_id)
    if p.finished_game:
        return render(request, "game/cannot_attend.html", {'worker_id': worker_id})

    context = {'worker_id': worker_id}
    print("in logic game: ", context)
    return render(request, "game/logic_game.html", context)


def contingency(request):
    worker_id = request.session.get('worker_id')
    if worker_id is None:
        return render(request, "game/cannot_attend.html", {'worker_id': worker_id})

    # Participant does not exist
    if not Participant.objects.filter(worker_id=worker_id).exists():
        return redirect('cannot_attend')

    p = Participant.objects.get(worker_id=worker_id)
    if p.finished_game:
        return render(request, "game/cannot_attend.html", {'worker_id': worker_id})

    context = {'worker_id': worker_id}
    print("in contingency game: ", context)
    return render(request, "game/contingency_game.html", context)

def change_agent(request):
    worker_id = request.session.get('worker_id')
    if worker_id is None:
        return render(request, "game/cannot_attend.html", {'worker_id': worker_id})

    # Participant does not exist
    if not Participant.objects.filter(worker_id=worker_id).exists():
        return redirect('cannot_attend')

    p = Participant.objects.get(worker_id=worker_id)
    if p.finished_game:
        return render(request, "game/cannot_attend.html", {'worker_id': worker_id})

    context = {'worker_id': worker_id}
    print("in change_agent game: ", context)
    return render(request, "game/change_agent_game.html", context)

def shuffle_keys(request):
    worker_id = request.session.get('worker_id')
    if worker_id is None:
        return render(request, "game/cannot_attend.html", {'worker_id': worker_id})

    # Participant does not exist
    if not Participant.objects.filter(worker_id=worker_id).exists():
        return redirect('cannot_attend')

    p = Participant.objects.get(worker_id=worker_id)
    if p.finished_game:
        return render(request, "game/cannot_attend.html", {'worker_id': worker_id})

    context = {'worker_id': worker_id}
    print("in shuffle_keys game: ", context)
    return render(request, "game/shuffle_keys_game.html", context)


def generate_id():
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(20))  # Form a 20-character password
    return password


# Save the game data and send to completion input page
def game_finished(request):
    data = request.POST.get('data', None)
    worker_id = request.POST.get('worker_id', None)
    game_type = request.POST.get("gameType")

    print("in game finished: ", request.POST)
    print("Game finished, submitting to s3. ID: ", worker_id, " - Game type: ", game_type)

    dt = datetime.today().strftime('%Y-%m-%d=%H:%M:%S')

    AWS_ACCESS_KEY = os.environ['AWS_ID']
    AWS_SECRET_KEY = os.environ['AWS_SECRET_KEY']

    final_data = json.loads(data)

    final_data["data"]["self_locs"] = take_transpose(final_data["data"]["self_locs"])
    filename = game_type + "/" + worker_id + "_" + dt + ".json"

    # print("writing ", filename)
    # with open(worker_id + "_" + dt + ".json", 'w+') as outfile:
    #    json.dump(final_data, outfile)

    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY
        )

        body = json.dumps(final_data).encode()
        s3.put_object(Body=body, Bucket='probself-data-raw', Key=filename)

    except ClientError as e:
        print("Client error.")
        # with open(filename, 'w') as f:
        #    json.dump(final_data, f)

    context = {
        "data": request.POST.get("data"),
        "worker_id": request.POST.get("worker_id"),
        "game_type": request.POST.get("gameType"),
    }

    save_into_db(context)

    # Go to completion
    return redirect('/completion/', permanent=True)


def save_into_db(context):
    data = context["data"]
    worker_id = context["worker_id"]
    game_type = context["game_type"]

    participant = Participant.objects.get(worker_id=worker_id)
    participant.data = data
    participant.game_type = game_type
    participant.finished_game = True
    participant.finish_dt = timezone.now()
    participant.elapsed_sec = (participant.finish_dt - participant.accept_dt).total_seconds()
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
