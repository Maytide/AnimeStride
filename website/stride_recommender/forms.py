from django import forms


class URLForm(forms.Form):
    # url = forms.CharField(max_length=240)
    url = forms.CharField(max_length=240, widget=forms.Textarea(attrs={'cols': 100, 'rows': 1}))

    # def __init__(self, *args, **kwargs):
    #     super(URLForm, self).__init__(*args, **kwargs)
    #     self.fields['url'].widget.attrs['cols'] = 10
