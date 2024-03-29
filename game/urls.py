"""
prob_self_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

from django.conf.urls.static import static
from django.conf import settings

from django.contrib.auth import views as auth_views

from django.contrib.auth.decorators import login_required

urlpatterns = [

    path('', views.home, name='home'),
    path('logic/', views.logic, name='logic'),
    path('contingency/', views.contingency, name='contingency'),
    path('game_page_cp/', views.contingency_perturbed, name='contingency_perturbed'),
    path('game_page_cap/', views.change_agent_perturbed, name='change_agent_perturbed'),
    path('game_page_lp/', views.logic_perturbed, name='logic_perturbed'),
    path('contingency_click/', views.contingency_click, name='contingency_click'),
    path('game_page_skc/', views.shuffle_keys_click, name='shuffle_keys_click'),
    path('game_page_cac/', views.change_agent_click, name='change_agent_click'),
    path('game_page_sa/', views.change_agent, name='change_agent'),
    path('game_page_cap/', views.change_agent_perturbed, name='change_agent_perturbed'),
    path('game_page_sk/', views.shuffle_keys, name='shuffle_keys'),
    path('game_finished/', views.game_finished, name='game_finished'),
    path('pre_game/', views.pre_game, name='pre_game'),
    path('success/', views.success, name='success'),
    path('cannot_attend/', views.cannot_attend, name='cannot_attend'),
    path('KmCFoxsrVcjPqaHqxqat/<str:worker_id>', views.register_participant, name='register_participant'),
    path('finished_survey/<str:worker_id>', views.finished_survey, name='finished_survey')

]