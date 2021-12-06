from logging import PlaceHolder
from flask import Flask, render_template
from flask_bootstrap import Bootstrap

import requests, json
import random

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms.validators import ValidationError

from geopy.geocoders import Nominatim

# create an instance of Flask
app = Flask(__name__) 
bootstrap = Bootstrap(app)
# route decorator binds a function to a URL

import os
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

key1 = '2751705df8c40b34efbd798cf7bdf9b6' 
key2 = '0d1d9d2ae255bb02b8d7fb4c90879192'
key3 = '400fd856dc9ba0c37b98e7463c2dd433'
keys = [key1,key2,key3] #three API keys 

API_KEY = 'AIzaSyBliiCLzc0cqvJ-uqc6yf9OFrf4jg0Oyk0'

def validator(self, cityname):
        excluded_chars = ","
        for char in self.name.data:
            print(char)
            if char in excluded_chars:
                raise ValidationError('please remove comma')

class Location(FlaskForm):
    name = StringField('City', validators=[DataRequired(),validator])

@app.route('/',methods=('GET', 'POST'))
def hello():        
    form = Location()
    city = "United States"
    if form.validate_on_submit():
        city = form.name.data
        city = " ".join(city.split()) #strip lead and trailing spaces

    api_key = keys[random.randint(0,2)] #randomly pick an api key
    try:
        loc = requests.get('http://ip-api.com/json/') #documentation here: https://ip-api.com/docs
        loc_data = loc.json()
        city_weather = loc_data['city']
        
        if city=="United States": #default
            r = requests.get('https://gnews.io/api/v4/top-headlines?lang=en&topic=nation&country=us&token='+api_key+'')
            url = 'http://api.openweathermap.org/data/2.5/weather?q='+city_weather+'&units=imperial&appid=271d1234d3f497eed5b1d80a07b3fcd1'
            w = requests.get(url)
            w_data = w.json()
            w_data['main']['temp'] = round(w_data['main']['temp'])
            w_data['main']['feels_like'] = round(w_data['main']['feels_like'])
            w_data['main']['temp_max']=round(w_data['main']['temp_max'])
            w_data['main']['temp_min'] = round(w_data['main']['temp_min'])
            city_id = w_data['sys']['id']
        else: #search term
            r = requests.get('https://gnews.io/api/v4/search?q='+city+'&lang=en&country=us&token='+api_key+'')
            w_data = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+city+'&units=imperial&appid=271d1234d3f497eed5b1d80a07b3fcd1').json()
            w_data['main']['temp'] = round(w_data['main']['temp'])
            w_data['main']['feels_like'] = round(w_data['main']['feels_like'])
            w_data['main']['temp_max']=round(w_data['main']['temp_max'])
            w_data['main']['temp_min'] = round(w_data['main']['temp_min'])
            city_id = w_data['sys']['id']
        data = r.json()

        longitude = getLong(city)
        latitude = getLat(city)
        print(latitude)
        print(longitude)
    except:
        output = 'failed'
    try:
        test = data['articles']
    except:
        return ('we seem to be encountering an error please try again')
    return render_template('template.html',data=data,form=form,cit=city,loc_data=loc_data,w_data=w_data,longitude=longitude,latitude = latitude)

def getLong(address):
    params = {
        'key': API_KEY,
        'address': address.replace(' ', '+')
    }
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    response = requests.get(base_url, params=params)
    data = response.json()
    if data['status'] == 'OK':
        result = data['results'][0]
        location = result['geometry']['location']
        return location['lng']
    else:
        return
        
def getLat(address):
    params = {
        'key': API_KEY,
        'address': address.replace(' ', '+')
    }

    base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    response = requests.get(base_url, params=params)
    data = response.json()
    if data['status'] == 'OK':
        result = data['results'][0]
        location = result['geometry']['location']
        return location['lat']
    else:
        return

#<center>
#<div>
#<form method="POST" action="/">
#    {{ form.csrf_token }}
#    {{ form.name.label }} {{ form.name(size=20) }}
#    <input type="submit" value="Go">
#</form>
#</div>
#</center>

  
#<img src={{data['articles'][1]['image']}} width="250">
#<p>{{data['articles'][1]['title']}}</p>
#<p>{{data['articles'][1]['description']}}</p>
#<p>{{data['articles'][1]['url']}}</p>
