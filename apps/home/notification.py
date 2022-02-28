# -*- encoding: utf-8 -*-
import mysql.connector
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .common import UserData, Notifier
import json
import requests

from.models import GroupNames, Groups
from.forms import GroupsForm, GroupNamesForm


# This is the handler for single target notification.
@login_required(login_url="/login/")
def single(request, user_id):
    """ 
    Fetch data from externl mysql DB and get the expo token.
    """
    context = {'segment': 'index'}
    data = []

    message_body = request.POST.get('message_body')
    message_title = request.POST.get('message_title')
    db = UserData()
    user = db.fetch_with_user_id(user_id)

    sched = request.POST.get('schedule_date')
    ds = sched.split('T')

    data.append({"to":user['push_notif_token'], "title":message_title, "body":message_body})

    # notifier = Notifier()
    # notifier.send_notification(data)

    db.close()

    context['message'] = "Send Notification Successful!"

    html_template = loader.get_template('home/single-notification.html')
    return HttpResponse(html_template.render(context, request))


# This is the 
@login_required(login_url="/login/")
def group_notification(request):
    """ 
    Select a group and send notification to the members of the selected group.
    """
    context = {'segment': 'multiple'}
    data = []

    print (request.POST)
    groups = GroupNames.objects.all()

    if request.method == 'POST':
        if request.POST.get('send_notification') != None:

            selected_group_id = request.POST.get('selected_group')
            group_obj = Groups.objects.filter(group_id=selected_group_id)
            msg_title = request.POST.get('message_title')
            msg_body = request.POST.get('message_body')
            print ('send notification hre')
            # Send The epxo notifiction here.
            db = UserData()
            users = db.fetch_all()
            for group in group_obj:
                for user in users:
                    if group.user_id == user['user_id']:
                        data.append({"to":user['push_notif_token'], "title":msg_title, "body":msg_body})

            notifier = Notifier()
            notifier.send_notification(data)

    context={'groups': groups}    

    html_template = loader.get_template('home/group-notification.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def group_management(request):
    """ 
    Add a new groupname and add members to that particular group.
    """
    context = {'segment': 'group-management'}

    group_ids = []
    group_name = ''

    db_group_names = GroupNames.objects.all()
    context['db_group_names'] = db_group_names

    if request.method == 'POST':
        if request.POST.get('add_group_name') != None:
            group_name = request.POST.get('group_name')

            # Add group name to Database here.
            gform = GroupNamesForm(request.POST, instance=GroupNames())

            if gform.is_valid():
                gform_instance = gform.save(commit=False)
                gform_instance.group_name = group_name
                gform_instance.save()
            else:
                print ('form is not valid!')

        if request.POST.get('selectedUsers[]') != None:
            group_ids = request.POST.getlist('selectedUsers[]')

            # Add users to Group here.
            if request.POST.get('group_name_id') != '':
                group_name_id = request.POST.get('group_name_id')
                group_name_obj = GroupNames.objects.get(id=group_name_id)

                print ('group_name_obj: ', group_name_obj.group_name)

                for ids in group_ids:
                    g_ins = Groups(user_id=ids, group_id=group_name_obj)
                    g_ins.save()

    db = UserData()

    context['users'] = db.fetch_all()
    db.close()

    html_template = loader.get_template('home/group-management.html')
    return HttpResponse(html_template.render(context, request))

