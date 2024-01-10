import re
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .forms import ChatForm

import openai
import os
from sqlalchemy import text, create_engine
#from langchain import SQLDatabase, PromptTemplate, OpenAI
from langchain_experimental.sql import SQLDatabaseChain
from django.shortcuts import render, redirect
from .forms import ChatForm, SearchDBForm
from langchain.utilities import SQLDatabase
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from .forms import SearchDBForm
from .models import SavedResult
openai.api_base = 'https://api.openai.iniad.org/api/v1'



def home(request):
    """
    チャット画面
    """

    # SQL_Resultをセッションから取得
    sql_result = request.session.get('SQL_Result', '')

    # ChatGPTの応答結果
    chat_results = request.session.get('Chat_Results', '')

    if sql_result:
        # SQL_Resultがある場合、ChatGPTにかけて解説を取得
        openai.api_key = "HTxvwG9NHlr26VOiR8tmCcQxu6nfHFnMbx4kNq_CTCv04E-HwFlhH2Q6xou8agVdzkfmX07sirQl2FIIgp4o6hw"

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "問題の答えと解説を一問ずつ詳しくお願いします"
                },
                {
                    "role": "user",
                    "content": sql_result
                },
            ],
        )

        chat_results = response["choices"][0]["message"]["content"]

    # ChatFormのインスタンスを作成
    form = ChatForm()

    # テンプレートに渡すコンテキストを定義
    context = {
        'form': form,
        'SQL_Result': sql_result,
        'chat_results': chat_results,
    }
    
   

    # テンプレートを描画してHTTPレスポンスを返す
    template = loader.get_template('teamapp/home.html')
    return HttpResponse(template.render(context, request))



#def home(request):
   #return render(request, "teamapp/home.html")

def result(request):
    if request.method == 'POST':
        #API呼び出し、suggestionに結果を代入
        #result = suggestion
        #結果を表示
        result = ""
        input = request.POST['input']
        if input == "":
            return redirect(home)
        
        #ChatGPTの処理
        output = [{"question":"1+1=","answer":"2"},{"question":"How are you","answer":"I'm fine"}]
    
        context = {
            'result': result,
            'input': output
        }
        return render(request, "teamapp/result.html", context)
    
    return redirect(home)








# API認証情報
openai.api_base = 'https://api.openai.iniad.org/api/v1'
SECRET_KEY = "HTxvwG9NHlr26VOiR8tmCcQxu6nfHFnMbx4kNq_CTCv04E-HwFlhH2Q6xou8agVdzkfmX07sirQl2FIIgp4o6hw"
os.environ["OPENAI_API_KEY"] = SECRET_KEY

# データベースの接続設定
db_name = "test.db"
sql_url = "sqlite:///" + db_name
tables = ["my_table"]

# SQLDatabaseオブジェクト
sql_database = SQLDatabase.from_uri(
    sql_url,
    include_tables=tables,
)

# LLM作成
llm_chain = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0,
    verbose=False,
)

# Prompt Templateを作成
template = """
Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
Use the following format:
    Question:   "Question here"
    SQLQuery:   "SQL Query to run"
    SQLResult:  "Result of the SQLQuery"
    Answer:     "Final answer here"
Only use the following tables: {table_info}\n
Question: {input}
"""

template = template.replace('    ', '    \n')

# SQLDatabaseChainに用いるプロンプトの定義
prompt = PromptTemplate(
    input_variables=["input", "table_info", "dialect"],
    template=template,
)

# SQLDatabaseChainを作成
db_chain = SQLDatabaseChain.from_llm(
    llm=llm_chain,
    db=sql_database,
    prompt=prompt,
    verbose=True,
    return_intermediate_steps=True,
)

# データベースの参照結果を出力する関数
def search_db(request):
    text = ""  # text変数を初期化
    result = None  # result変数を初期化
    form = SearchDBForm()
    
    if request.method == 'POST':
        # POSTリクエストの場合

        # リクエストから質問を取得
        text = request.POST.get('input_text')
    
    
    if text:
    # db_chainを実行
        try:
            result = db_chain(text)
            #print("Langchain Result:", result)
        
        except Exception as e:
            print("Error:", e)
            return render(request, 'teamapp/search_db.html')

    if result is not None and "query" in result and "intermediate_steps" in result:
        question = result["query"]
        sql_queries = []
        sql_results = []

        for step in result["intermediate_steps"]:
            if "input" in step:
                input_text = step["input"]
                if "SQLQuery:" in input_text and "SQLResult:" in input_text:
                    sql_query = input_text.split("SQLQuery:")[1].split("SQLResult:")[0].replace("  ", " ").replace("\n", "")
                    sql_result = input_text.split("SQLResult:")[1].split("Answer:")[0].replace("  ", " ").replace("\n", "")

                    sql_queries.append(sql_query)
                    sql_results.append(sql_result)

        answer = result['result']
        

        # データを辞書に格納
        dictionary = {
            'form': form,
            'Question': question,
            'SQL_Query': sql_query,
            'SQL_Result': sql_result,
            'Answer': answer,
        }
        
        
        for sql_result in sql_results:
                saved_result = SavedResult.objects.create(sql_result=sql_result)
                saved_result.save()
                
        reg = re.compile(r"\), \(")
        test = re.split(reg,sql_result[3:-2])       
        dictionary["SQL_Result"] = test
        
        
        return render(request, 'teamapp/search_db.html', dictionary)
    
    context = {'form': form}

    # POSTリクエストでない場合、エラーまたはリダイレクトを処理
    return render(request, 'teamapp/search_db.html')





def new(request):
    context = {
        "saved_results" : SavedResult.objects.all()
    }
    

        # new.html を表示する際に saved_results を渡す
    return render(request, 'teamapp/new.html', context)

    # POSTリクエストでない場合、エラーまたはリダイレクトを処理
    #saved_results = SavedResult.objects.all()
    #return render(request, 'teamapp/new.html', {'saved_results': saved_results})
    
    
from django.views.decorators.http import require_POST
from .models import SavedResult  # Replace with the actual model name

@require_POST  # Ensure that this view only accepts POST requests
# 削除機能
def delete_sql_result(request, id):
    # Get the object you want to delete
    saved_result = SavedResult.objects.get(pk=id)
    
    # Delete the object
    saved_result.delete()
    
    # Redirect to a success page or back to the page with the list
    return redirect('new')  # Specify the name of the view to redirect to



def history(request):
    sort = request.GET.get('sort', 'asc')  # ソートパラメータを取得、指定がなければ昇順とする
    if sort == 'desc':
        saved_results = SavedResult.objects.all().order_by('-id')  # 降順にソート
    else:
        saved_results = SavedResult.objects.all().order_by('id')   # 昇順にソート（デフォルト）

    context = {
        'saved_results': saved_results,
    }
    return render(request, 'teamapp/new.html', context)

