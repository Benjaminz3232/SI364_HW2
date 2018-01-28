## SI 364
## Winter 2018
## HW 2 - Part 1

## This homework has 3 parts, all of which should be completed inside this file
# (and a little bit inside the /templates directory).

## Add view functions and any other necessary code to this Flask application c
# ode below so that the routes described in the README exist and render the
# templates they are supposed to (all templates provided are inside the
# templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates
# (new .html files) to the templates directory.


#Sadie Staudacher
#############################
##### IMPORT STATEMENTS #####
#############################
from flask import Flask, request, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required

import requests
import json

#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'

####################
###### FORMS #######
####################

class AlbumEntryForm(FlaskForm): #creating a class of a form
    album_name = StringField('Enter the name of an album:', validators=[Required()]) #asking the name and making it a required field #use stringmethod to verify that there is a string
    like_options = RadioField('How much do you like this album? (1 low, 3 high)', choices=[('1','1'),('2','2'),('3','3')],validators=[Required()])
    submit = SubmitField('Submit')



####################
###### ROUTES ######
####################

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user/<name>')
def hello_user(name):
    return '<h1>Hello {0}<h1>'.format(name)

####################
####################


@app.route('/artistform')
def artist_form():
    return render_template('artistform.html')

@app.route('/artistinfo', methods = ['GET', 'POST'])
def artist_info():
    artist = request.args.get('artist',"")
    param_dict = {'term': artist, 'entity' : 'musicTrack'}
    baseurl = "https://itunes.apple.com/search?"
    response = requests.get(baseurl, params = param_dict).json()['results']
    print(str(response[0]))
    tracks = []
    for song in response:
        tracks.append(song)
    return render_template('artist_info.html',objects=tracks)

@app.route('/artistlinks')
def artist_links():
    return render_template('artist_links.html')

@app.route('/specific/song/<artist_name>', methods = ['GET', 'POST'])
def specific_artist(artist_name):
    param_dict = {'term': artist_name, 'entity' : 'musicTrack'}
    baseurl = "https://itunes.apple.com/search?"
    response = requests.get(baseurl, params = param_dict).json()['results']
    return render_template('specific_artist.html', results = response)

@app.route('/album_entry')
def album_entry():
    simpleForm = AlbumEntryForm()
    return render_template('album_entry.html', form=simpleForm)

@app.route('/album_result', methods = ['GET', 'POST'])
def album_result():
    form = AlbumEntryForm(request.form)
    # return render_template('album_data.html', form=simpleForm) #we are using post method, this is why we are using request.form
    if request.method == 'POST' and form.validate_on_submit(): #we are trying to validate everything on the click of submit button
        album_name = form.album_name.data #retrieving data from that variable
        like_options = form.like_options.data
        return render_template('album_data.html', album_name = album_name, like_options = like_options)
    flash('All fields are required!') #if the code returned didnt work, it would send a message saying that all fields are required
    return redirect(url_for('/album_entry'))




















if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)
