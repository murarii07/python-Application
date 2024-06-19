import os,requests,datetime,dotenv
from flask import Flask,render_template,request,redirect,session
from src.models import init_app,register_user,find_user
dotenv.load_dotenv()
app = Flask(__name__)
app.config['MONGO_URI']=os.getenv('MONGO_URI')

#to connect with mongo
init_app(app)
#to add session variables we need to add secretkey
app.secret_key=os.getenv('KEY')
@app.route("/")
def hello_world():  
    return render_template('index.html')

@app.route("/api")
def about():
    return render_template('api.html')

@app.route("/api/ans", methods=["POST"])
def abut():
    r = requests.post('https://clipdrop-api.co/text-to-image/v1',
    files = {
        'prompt': (None, request.form.get('image'), 'text/plain')
    },
    headers = { 'x-api-key': os.getenv('X_API_KEY')
               })
    if (r.ok):
        with open('./src/static/df.png','wb') as fp:
            fp.write(r.content)
    else:
        r.raise_for_status()
    return render_template('api.html',image='./src/df.png')

@app.route('/news', methods=['GET'])
def news():
    if 'username'  in  session:
        print(session['username'])
        return render_template('news.html',username=session["username"])
    else:
        return render_template('news.html',)

@app.route('/news/ans',methods=['POST'])
def news_ans():
   API_KEY=os.getenv("NEWS_API_KEY")
   data=request.get_json()
   q=data['image']
   today=datetime.datetime.now()
   todays=today.strftime("%Y-%m-%d")
   
   # Calculate yesterday's date by subtracting one day
   fromdate= today - datetime.timedelta(days=3)
   fromdate = fromdate.strftime("%Y-%m-%d")
#    print(fromdate)
   r=requests.get(f'https://newsapi.org/v2/everything?q={q}&language=en&from={fromdate}&to={todays}&apiKey={API_KEY}')
   obj=r.json()
   artci=obj['articles']
   def func(x):
           return x['url']!='https://removed.com'
   artci=list(filter(func,artci))
   return {'status':200,"value":artci}
@app.route('/login')
def login():
    if request.method == 'GET':
        return render_template('login.html')
@app.route('/login',methods=['POST'])
def logged():
    username,password = request.form.get('username'),request.form.get('password')
    res=find_user(username,password)
    print(res)
    if(res):
        session['username'] = username
        return redirect("/news")
    else:
        return f" username or passowrd is not valid"

@app.route("/register" ,methods=['POST','GET'])
def register():
    if request.method == 'POST':
        username,password = request.form.get('username'),request.form.get('password')
        res=register_user(username,password)
        if(res):
            return redirect("/login")
        else:
            return f" username or passowrd is not valid"
    else:
        return render_template('register.html')
    
