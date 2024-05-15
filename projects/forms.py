from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from projects.models import *
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter project name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter project description'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control col-md-4'
        self.fields['description'].widget.attrs['class'] = 'form-control col-md-4'



class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['project', 'title', 'descriptions', 'deadline', 'status', 'assigned_to']

        widgets = {
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = UserProfile.objects.all() 




class CreateUserForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'name', 'password1', 'password2' ,'email' ,'role']  

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True 

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['name', 'description']

class RoleAssignmentForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['role']