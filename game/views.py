import json
import os

import boto3
from botocore.exceptions import ClientError
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def logic(request):
    context = {}
    return render(request, "game/logic_game.html", context)

def contingency(request):
    context = {}
    return render(request, "game/contingency_game.html", context)

def game_finished(request):
    data = request.POST.get('data', None)

    from datetime import datetime
    dt = datetime.today().strftime('%Y-%m-%d=%H:%M:%S')

    aws_id = os.environ['AWS_ID']
    aws_secret_key = os.environ['AWS_SECRET_KEY']

    AWS_ACCESS_KEY = aws_id
    AWS_SECRET_KEY = aws_secret_key

    final_data = json.loads(data)

    filename = dt + ".json"
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

    return HttpResponse(data)
