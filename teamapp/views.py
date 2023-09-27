from django.shortcuts import render, redirect

# Create your views here.

def home(request):
    return render(request, "teamapp/home.html")

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