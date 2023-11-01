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




import openai
import os
from sqlalchemy import text, create_engine
from langchain import SQLDatabase, PromptTemplate, OpenAI
from langchain_experimental.sql import SQLDatabaseChain
from django.shortcuts import render, redirect
from .forms import ChatForm, SearchDBForm

# API認証情報
openai.api_base = 'https://api.openai.iniad.org/api/v1'
SECRET_KEY = "Pm16GE8LCg592kXS6A7p8cQmaWS9IO_2BVpUH62Nfu7Bt8-6dBl5rAClH1mpniKo8DyuiAkrAltw0Y5S5j87VVA"
os.environ["OPENAI_API_KEY"] = SECRET_KEY

# データベースの接続設定
db_name = "sqlite-sakila.db"
sql_url = "sqlite:///" + db_name
tables = ["customer", "store", "staff"]

# SQLDatabaseオブジェクト
sql_database = SQLDatabase.from_uri(
    sql_url,
    include_tables=tables,
)

# LLM作成
llm = OpenAI(
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
Only use the following tables: {table_info}
Question: {input}
"""

# SQLDatabaseChainに用いるプロンプトの定義
prompt = PromptTemplate(
    input_variables=["input", "table_info", "dialect"],
    template=template,
)

# SQLDatabaseChainを作成
db_chain = SQLDatabaseChain(
    llm=llm,
    database=sql_database,
    prompt=prompt,
    verbose=True,
    return_intermediate_steps=True,
)

# データベースの参照結果を出力する関数
def search_db(request):
    text = ""  # text変数を初期化
    result = None  # result変数を初期化
    if request.method == 'POST':
        # POSTリクエストの場合

        # リクエストから質問を取得
        text = request.POST.get('input_text')
    
    
    if text:
    # db_chainを実行
      result = db_chain(text)

    if result is not None and "query" in result and "intermediate_steps" in result:
        # 出力結果を加工
        question = result["query"]
        sql_query = ""
        sql_result = ""

        # intermediate_stepsからSQLQueryとSQLResultを抽出
        if result["intermediate_steps"]:
            first_step = result["intermediate_steps"][0]
            if "input" in first_step:
                input_text = first_step["input"]
                
                
                
                #"SQLQuery:" と "SQLResult:" の位置を確認
                if "SQLQuery:" in input_text and "SQLResult:" in input_text:
                    sql_query = input_text.split("SQLQuery:")[1].split("SQLResult:")[0].replace("  ", " ").replace("\n", "")
                    sql_result = input_text.split("SQLResult:")[1].split("Answer:")[0].replace("  ", " ").replace("\n", "")

        answer = result["result"]

        # データを辞書に格納
        dictionary = {
            'Question': question,
            'SQL_Query': sql_query,
            'SQL_Result': sql_result,
            'Answer': answer,
        }
        
        
        
        return render(request, 'teamapp/search_db.html', dictionary)

    # POSTリクエストでない場合、エラーまたはリダイレクトを処理
    return render(request, 'teamapp/search_db.html')


#result = search_db(text)
#print('aaaaa',result)









