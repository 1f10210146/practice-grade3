from django import forms

class ChatForm(forms.Form):

    sentence = forms.CharField(label='チャット', widget=forms.Textarea(), required=True)
    

class SearchDBForm(forms.Form):
    question = forms.CharField(label='質問', max_length=100)

