import os,requests,datetime,dotenv
from flask import Flask,render_template,request
dotenv.load_dotenv()
app = Flask(__name__)
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