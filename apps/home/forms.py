from django.forms import ModelForm

from .models import Groups, GroupNames

class GroupsForm(ModelForm):
    class Meta:
        model = Groups
        fields = [
            'group_id'
        ]

class GroupNamesForm(ModelForm):
    class Meta:
        model = GroupNames
        fields = [
            'group_name'
        ]