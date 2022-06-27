from django import forms

class ProjectForm(forms.Form):
    name = forms.CharField(label='name', max_length=50)