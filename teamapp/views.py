from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .forms import ChatForm

import openai
openai.api_base = 'https://api.openai.iniad.org/api/v1'

# Create your views here.

def home(request):
    """
    チャット画面
    """

    # 応答結果
    chat_results = ""

    if request.method == "POST":
        # ChatGPTボタン押下時

        form = ChatForm(request.POST)
        if form.is_valid():

            sentence = form.cleaned_data['sentence']

            # TODO: APIキーのハードコーディングは避ける
            openai.api_key = "Pm16GE8LCg592kXS6A7p8cQmaWS9IO_2BVpUH62Nfu7Bt8-6dBl5rAClH1mpniKo8DyuiAkrAltw0Y5S5j87VVA"

            # ChatGPT
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "日本語で応答してください"
                    },
                    {
                        "role": "user",
                        "content": sentence
                    },
                ],
            )

            chat_results = response["choices"][0]["message"]["content"]

    else:
        form = ChatForm()

    template = loader.get_template('teamapp/home.html')
    context = {
        'form': form,
        'chat_results': chat_results
    }
    return HttpResponse(template.render(context, request))


#def home(request):
   #return render(request, "teamapp/home.html")

def result(request):
    if request.method == 'POST':
        #API呼び出し、suggestionに結果を代入
        #result = suggestion
        #結果を表示
        result = ""
        subject = request.POST['subject']
        if subject == "-":
            return redirect(home)
    
        context = {
            'result': result,
            'subject': subject
        }
        return render(request, "teamapp/result.html", context)
    
    return redirect(home)