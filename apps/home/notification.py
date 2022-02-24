# -*- encoding: utf-8 -*-
import mysql.connector
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .common import UserData
import json
import requests

@login_required(login_url="/login/")
def single(request, user_id):
    context = {'segment': 'index'}
    url = "https://exp.host/--/api/v2/push/send"
    headers = {
        'Content-Type': 'application/json',
        'accept': 'application/json',
        'accept-encoding': 'gzip, deflate'
    }

    message_body = request.POST.get('message_body')
    message_title = request.POST.get('message_title')
    db = UserData()
    user = db.fetch_with_user_id(user_id)

    context['users'] = db.fetch_all()

    data = {"to":user['push_notif_token'], "title":message_title, "body":message_body}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    db.close()

    context['message'] = "Send Notification Successful!"

    html_template = loader.get_template('home/dashboard.html')
    return HttpResponse(html_template.render(context, request))