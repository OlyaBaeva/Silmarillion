from django import forms

class Access(forms.Form):
    Password = forms.CharField()

    def __str__(self):
        return str(self.Password)
