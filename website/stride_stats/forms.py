from django import forms


class URLForm(forms.Form):
    search_string = forms.CharField(max_length=240, widget=forms.Textarea(attrs={'cols': 100, 'rows': 1}))
    genre_obj = forms.CharField(max_length=1000)