# -*- encoding: utf-8 -*-
import mysql.connector
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .common import UserData

@login_required(login_url="/login/")
def single(request, user_id):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))