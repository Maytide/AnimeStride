from django import forms


class URLForm(forms.Form):
    url = forms.CharField(max_length=120)