
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from random import randint

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



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        t_category = request.form['category']
        if t_category != "Random":
            data = Topic.query.filter_by(category=t_category).all()
        else:
            data = Topic.query.all()
        return render_template("index.html", topic=data[randint(0, len(data)-1)].topic)
    else:
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

