
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from random import randint
import os

app = Flask(__name__)

#database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///topics.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)

#database table for Debate Topic Generator
class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(300), unique=True, nullable = False)
    category = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return '<Topic %r>' % self.id

#database table for Role PLay Game
class Situation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    situation = db.Column(db.String(300), unique=True, nullable=False)

    def __repr__(self):
        return '<Situation %r>' % self.id


class Abbreviation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    abbreviation = db.Column(db.String(30), nullable=False)
    meaning = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return '<Abbreviation %r>' % self.id


class Idiom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idiom = db.Column(db.String(100), unique=True, nullable=False)
    meaning = db.Column(db.String(400), nullable=False)

    def __repr__(self):
        return '<Idiom %r>' %self.id


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/debate-topic', methods=['GET', 'POST'])
def debate_topic():
    if request.method == "POST":
        #determinate what button in form was pressed
        if request.form['submit_button'] == 'Add':
            return redirect('/create-topic')
        elif request.form['submit_button'] == 'Show':
            return redirect('/topics')
        elif request.form['submit_button'] == 'Generate':
            t_category = request.form['category']
            if t_category != "Random":
                data = Topic.query.filter_by(category=t_category).all()
            else:
                data = Topic.query.all()
            #choose random topic
            return render_template("debate-topic.html", topic=data[randint(0, len(data) - 1)].topic)
    else:
        return render_template("debate-topic.html")


@app.route('/create-topic', methods=['GET', 'POST'])
def create_topic():
    if request.method == "POST":
        #get information from a form
        question = request.form['topic']
        category = request.form['category']

        #create a topic
        topics = Topic(topic=question, category=category)

        #add new topic to a database table and if correct then redirect to main page
        try:
            db.session.add(topics)
            db.session.commit()

            return redirect('/')
        except:
            return "Error: Can not add new topic! Maybe we already have your topic in our list!!!"
    else:
        return render_template("create-topic.html")


@app.route('/topics')
def topics():
    data = Topic.query.order_by(Topic.category).all()
    return render_template("topics.html", topics=data)


@app.route('/role-play', methods=['GET', 'POST'])
def role_play():
    if request.method == "POST":
        #determinate what button was pressed in a form
        if request.form['submit_button'] == 'Add':
            #add new situation to the database table
            situation = Situation(situation=request.form['new-situation'])

            try:
                db.session.add(situation)
                db.session.commit()
                return redirect('/')
            except:
                return "Error: Can not add new situation! Maybe we already have your situation in our list!!!"
        elif request.form['submit_button'] == 'Generate':   #choose random situation
            data = Situation.query.all()
            return render_template("role-play.html", situation=data[randint(0,len(data)-1)].situation)
        elif request.form['submit_button'] == 'Show':   #show a situations list
            data = Situation.query.all()
            return render_template("role-play.html", situations=data)
    else:
        return render_template('role-play.html')



@app.route('/box-of-lies', methods=['GET','POST'])
def box_of_lies():
    if request.method == "POST":
        directory = '/home/zlenglish/mysite/static/images/box-of-lies'
        #directory = 'static/images/box-of-lies'
        files = os.listdir(directory)
        return render_template('box-of-lies.html', image=files[randint(0, len(files)-1)])
    else:
        return render_template('box-of-lies.html')


@app.route('/abbreviations', methods=['GET', 'POST'])
def abbreviations():
    if request.method == "POST":
        if request.form['subbmit_button'] == "Add":
            new_abbreviation = request.form['new-abbreviation']
            meaning = request.form['abbreviation-meaning']
            abbreviation = Abbreviation(abbreviation=new_abbreviation, meaning=meaning)

            try:
                db.session.add(abbreviation)
                db.session.commit()
                return redirect('/')
            except:
                return "Error: Can not add new abbreviation! Maybe we already have your meaning in our list!!!"
        elif request.form['subbmit_button'] == "Generate":
            data = Abbreviation.query.all()
            return render_template('abbreviations.html', random_abbreviation=data[randint(0, len(data)-1)].abbreviation)
        elif request.form['subbmit_button'] == "Meaning":
            abbr = request.form['random_abb']
            abb = Abbreviation.query.filter_by(abbreviation=request.form['random_abb']).first()
            return render_template('abbreviations.html', random_abbreviation=abb.abbreviation, meaning=abb.meaning)
        elif request.form['subbmit_button'] == "Show":
            data = Abbreviation.query.all()
            return render_template('abbreviations.html', abbreviations=data)
    else:
        return render_template('abbreviations.html')


@app.route('/abbreviations-edit', methods=['GET', 'POST'])
def abbreviations_edit():
    if request.method == "POST":
        if request.form['subbmit_button'] == "Add":
            new_abbreviation = request.form['new-abbreviation']
            meaning = request.form['abbreviation-meaning']
            abbreviation = Abbreviation(abbreviation=new_abbreviation, meaning=meaning)

            try:
                db.session.add(abbreviation)
                db.session.commit()
                return redirect('/')
            except:
                return "Error: Can not add new abbreviation! Maybe we already have your meaning in our list!!!"
        elif request.form['subbmit_button'] == "Generate":
            data = Abbreviation.query.all()
            return render_template('abbreviations.html', random_abbreviation=data[randint(0, len(data)-1)].abbreviation)
        elif request.form['subbmit_button'] == "Meaning":
            abbr = request.form['random_abb']
            abb = Abbreviation.query.filter_by(abbreviation=request.form['random_abb']).first()
            return render_template('abbreviations.html', random_abbreviation=abb.abbreviation, meaning=abb.meaning)
        elif request.form['subbmit_button'] == "Show":
            data = Abbreviation.query.all()
            return render_template('abbreviations-edit.html', abbreviations=data)
    else:
        return render_template('abbreviations-edit.html')



@app.route('/abbreviations-delete/<int:id>')
def abbreviation_delete(id):
    abbreviation = Abbreviation.query.get_or_404(id)

    try:
        db.session.delete(abbreviation)
        db.session.commit()
        return redirect('/abbreviations-edit')
    except:
        return "Can not delete abbreviation"



@app.route('/idioms', methods=['GET', 'POST'])
def idioms():
    if request.method == "POST":
        if request.form['subbmit_button'] == "Add":
            new_idiom = request.form['new-idiom']
            meaning = request.form['idiom-meaning']
            idiom = Idiom(idiom=new_idiom, meaning=meaning)

            try:
                db.session.add(idiom)
                db.session.commit()
                return redirect('/')
            except:
                return "Error: Can not add new idiom! Maybe we already have your idiom in our list or this is another error!!!"
        elif request.form['subbmit_button'] == "Generate":
            data = Idiom.query.all()
            return render_template('idioms.html', random_idiom=data[randint(0, len(data)-1)].idiom)
        elif request.form['subbmit_button'] == "Meaning":
            random_idiom = request.form['random_idiom']
            idiom = Idiom.query.filter_by(idiom=request.form['random_idiom']).first()
            return render_template('idioms.html', random_idiom=idiom.idiom, meaning=idiom.meaning)
        elif request.form['subbmit_button'] == "Show":
            data = Idiom.query.all()
            return render_template('idioms.html', idioms=data)
    else:
        return render_template('idioms.html')