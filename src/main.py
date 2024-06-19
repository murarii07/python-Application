from flask import Flask,render_template,request
import requests
import datetime
app = Flask(__name__)

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
    headers = { 'x-api-key': "b2674062e26834c1fff13d8d8db474fa09bec81d2973c0ba994e48293a11181d4037a33ac32f8930dd5d3f9f7d2803a9"
               })
    if (r.ok):
        with open('./src/static/df.png','wb') as fp:
            fp.write(r.content)
    else:
        r.raise_for_status()
    return render_template('api.html',image='./src/df.png')

@app.route('/news', methods=['GET'])
def news():
    return render_template('news.html')

@app.route('/news/ans',methods=['POST'])
def news_ans():
   API_KEY='561704f71a4043e5afd063d95f7486bb'
   data=request.get_json()
   print(data)
   q=data['image']
   today=datetime.datetime.now()
   todays=today.strftime("%Y-%m-%d")
   
   # Calculate yesterday's date by subtracting one day
   fromdate= today - datetime.timedelta(days=3)
   
   fromdate = fromdate.strftime("%Y-%m-%d")
   print(fromdate)
   r=requests.get(f'https://newsapi.org/v2/everything?q={q}&language=en&from={fromdate}&to={todays}&apiKey={API_KEY}')
   obj=r.json()
   artci=obj['articles']
   def func(x):
           return x['url']!='https://removed.com'

   artci=list(filter(func,artci))
   return {'status':200,"value":artci}