# -*- encoding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class GroupNames(models.Model):
    group_name = models.CharField(max_length=50, blank=True, default='')


class Groups(models.Model):

    user_id =  models.IntegerField(blank=True, null=True)
    group_id = models.ForeignKey(GroupNames, on_delete=models.CASCADE, null=True)

    def __str__(self):
        strName = "%s" %(
            self.group_id
        )

        return strName

