from django import forms

class LinkForm(forms.Form):
    port_a_id = forms.CharField(label='port_a_id', max_length=500)
    port_b_id = forms.CharField(label='port_b_id', max_length=500)
