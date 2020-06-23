
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from random import randint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///topics.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)


class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(300), unique=True, nullable = False)
    category = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return '<Topic %r>' % self.id


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


@app.route('/create-topic', methods=['GET', 'POST'])
def create_topic():
    if request.method == "POST":
        question = request.form['topic']
        category = request.form['category']

        topics = Topic(topic=question, category=category)

        try:
            db.session.add(topics)
            db.session.commit()
            return redirect('/')
        except:
            return "Error: Can not add a new topic!!!"
    else:
        return render_template("create-topic.html")


@app.route('/topics')
def topics():
    data = Topic.query.order_by(Topic.category).all()
    return render_template("topics.html", topics=data)
