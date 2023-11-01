from django import forms

class ChatForm(forms.Form):
    sentence = forms.CharField(label='チャット', widget=forms.Textarea(attrs={'placeholder' :"調べたい問題を入力してください","style":"height:20px"}), required=True)
