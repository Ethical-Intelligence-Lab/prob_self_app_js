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
    return HttpResponse(data)