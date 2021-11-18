from flask import Flask, render_template
from flask_bootstrap import Bootstrap

import requests, json
import random

# create an instance of Flask
app = Flask(__name__) 
bootstrap = Bootstrap(app)
# route decorator binds a function to a URL

key1 = '2751705df8c40b34efbd798cf7bdf9b6'
key2 = '0d1d9d2ae255bb02b8d7fb4c90879192'
keys = [key1,key2]


@app.route('/')
def hello():
    api_key = keys[random.randint(0,1)]
    try:
        r = requests.get('https://gnews.io/api/v4/top-headlines?lang=en&topic=nation&country=us&token='+api_key+'')
        data = r.json()
        top1 = data['articles'][0]
        title = top1['title']
        descrip = top1['description']
        url = top1['url']
        image = top1['image']
    except:
        output = 'failed'
    return render_template('template.html',t = title,d=descrip,u=url,i=image,dat=data)


